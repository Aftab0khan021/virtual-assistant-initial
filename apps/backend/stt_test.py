import os, requests
p = os.path.expandvars(r"%USERPROFILE%\Downloads\test.wav")
if not os.path.exists(p):
    print("File not found:", p); raise SystemExit(1)
with open(p, "rb") as f:
    r = requests.post(
        "http://127.0.0.1:8080/api/v1/stt/transcribe",
        files={"file": ("test.wav", f, "audio/wav")},
        timeout=120,
    )
print("Status:", r.status_code)
print("Body:", r.text)
