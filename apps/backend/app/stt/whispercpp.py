# Placeholder for whisper.cpp wrapper. Replace with actual binding/shell call.
import pathlib

async def transcribe_wav(path: str, model: str = "ggml-base.en.bin") -> str:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    # TODO: Implement whisper.cpp CLI call and parse output
    return "transcript placeholder"
