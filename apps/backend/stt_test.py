import requests, os

file_path = os.path.expandvars(r"%USERPROFILE%\Downloads\test.wav")
url = "http://127.0.0.1:8080/api/v1/stt/transcribe"

if not os.path.exists(file_path):
    print("File not found:", file_path)
    raise SystemExit(1)

with open(file_path, "rb") as f:
    files = {"file": ("test.wav", f, "audio/wav")}
    r = requests.post(url, files=files, timeout=120)

print("Status:", r.status_code)
print("Response:", r.text)
