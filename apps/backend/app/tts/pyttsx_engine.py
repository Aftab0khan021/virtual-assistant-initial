import pyttsx3, threading

# Serialize all TTS calls so only one runs at a time.
_engine_lock = threading.Lock()

def _pick_voice(e: pyttsx3.Engine):
    try:
        for v in e.getProperty("voices"):
            if any(k in v.name for k in ("Zira", "Aria", "Heera")):
                e.setProperty("voice", v.id)
                break
    except Exception:
        pass

def speak(text: str):
    # Create a fresh engine for each call to avoid stale run loops.
    with _engine_lock:
        e = pyttsx3.init()
        _pick_voice(e)
        e.setProperty("volume", 1.0)
        e.setProperty("rate", 180)
        e.say(text)
        e.runAndWait()
        e.stop()
