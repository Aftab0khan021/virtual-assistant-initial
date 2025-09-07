try:
    import fastapi, uvicorn, multipart, faster_whisper, pyttsx3, sqlmodel, sqlalchemy, requests
    print("? all imports succeeded")
except Exception as e:
    print("? import failed:", e)
