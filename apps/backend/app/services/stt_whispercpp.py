# apps/backend/app/services/stt_whispercpp.py
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Optional

# Defaults; can be overridden by environment variables
WHISPER_CPP_EXE = Path(os.getenv("WHISPER_CPP_EXE", "apps/backend/whispercpp/main.exe"))
WHISPER_MODEL_PATH = Path(os.getenv("WHISPER_MODEL_PATH", "apps/backend/models/ggml-base.en.gguf"))

# If ffmpeg is not in PATH, set absolute path here (or install and add to PATH)
FFMPEG_BIN = os.getenv("FFMPEG_BIN", "ffmpeg")

def _ensure_paths():
    if not WHISPER_CPP_EXE.exists():
        raise FileNotFoundError(f"whisper.cpp main.exe not found at: {WHISPER_CPP_EXE}")
    if not WHISPER_MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at: {WHISPER_MODEL_PATH}")
    if shutil.which(FFMPEG_BIN) is None:
        raise EnvironmentError("ffmpeg not found in PATH. Please install ffmpeg and add it to PATH.")

def _to_wav_mono16k(input_path: Path) -> Path:
    """
    Convert any input audio to 16 kHz mono WAV using ffmpeg.
    """
    out_path = input_path.with_suffix(".norm.wav")
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-i", str(input_path),
        "-ac", "1",
        "-ar", "16000",
        "-f", "wav",
        str(out_path),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"ffmpeg convert failed: {proc.stderr}")
    return out_path

def transcribe_file(input_audio_bytes: bytes, language: Optional[str] = "en") -> str:
    """
    Transcribe an audio file (bytes) via whisper.cpp CLI. Returns plain text transcript.
    """
    _ensure_paths()

    # Use a temporary working dir per request
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        in_ext = ".tmp"  # we'll let ffmpeg sniff
        raw_in = workdir / f"{uuid.uuid4().hex}{in_ext}"
        raw_in.write_bytes(input_audio_bytes)

        wav_path = _to_wav_mono16k(raw_in)

        # We'll ask whisper.cpp to write output text to a file to avoid stdout parsing differences.
        out_prefix = workdir / "out"
        out_txt = workdir / "out.txt"

        # whisper.cpp CLI (main.exe) typical flags:
        # -m model_path, -f audio, -l language, -otxt (write TXT), -of prefix (output prefix)
        # Add -nt (no timestamps) for cleaner plain text, optional.
        cmd = [
            str(WHISPER_CPP_EXE),
            "-m", str(WHISPER_MODEL_PATH),
            "-f", str(wav_path),
            "-l", language if language else "auto",
            "-otxt",
            "-of", str(out_prefix),
            "-nt",
        ]

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"whisper.cpp failed (code {proc.returncode}).\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}")

        if not out_txt.exists():
            # Fallback: some builds write to stdout only; try to extract the last non-empty line.
            # (Usually not needed when -otxt is present.)
            lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
            return lines[-1] if lines else ""

        return out_txt.read_text(encoding="utf-8").strip()
