import React, { useRef, useState } from "react";
import type { Msg } from "./ChatPane";

const API = "http://localhost:8080";

export default function MicButton({ onMessage }:{ onMessage:(m:Msg)=>void }){
  const [recording, setRec] = useState(false);
  const mediaRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  async function start(){
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    mediaRef.current = rec;
    chunksRef.current = [];
    rec.ondataavailable = (e) => { if (e.data.size) chunksRef.current.push(e.data); };
    rec.onstop = async () => {
      try {
        // send audio to backend (placeholder transcribe returns "hello world")
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const fd = new FormData();
        fd.append("audio", blob, "clip.webm");

        const tRes = await fetch(`${API}/api/v1/voice/transcribe`, { method: "POST", body: fd });
        const tJson = await tRes.json();
        const text = tJson.text || "hello world";
        onMessage({ role: "user", text });

        // understand -> reply
        const uRes = await fetch(`${API}/api/v1/voice/understand`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, locale: "en-IN" })
        });
        const uJson = await uRes.json();
        const reply = uJson.reply ?? `Intent: ${uJson.intent}`;
        onMessage({ role: "assistant", text: reply });

        // speak the reply on Windows via backend
        await fetch(`${API}/api/v1/tts/speak`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: reply })
        });
      } catch (err) {
        console.error(err);
        onMessage({ role: "assistant", text: "Sorry, I hit an error talking to the API." });
      }
    };
    rec.start();
    setRec(true);
  }

  function stop(){
    mediaRef.current?.stop();
    mediaRef.current?.stream.getTracks().forEach(t => t.stop());
    setRec(false);
  }

  return (
    <button
      onMouseDown={start}
      onMouseUp={stop}
      onTouchStart={start}
      onTouchEnd={stop}
      style={{ padding:"12px 20px", borderRadius: 16, border: "1px solid #ccc", cursor:"pointer"}}
    >
      {recording ? "Listening… release to stop" : "Hold to Speak"}
    </button>
  );
}
