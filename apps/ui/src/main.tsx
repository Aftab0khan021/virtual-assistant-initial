// apps/ui/src/main.tsx
import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function App() {
  const [text, setText] = useState("Hello from the UI!");
  const [status, setStatus] = useState("");

  async function speak() {
    setStatus("Calling /tts/speak …");
    try {
      const res = await fetch("http://127.0.0.1:8080/api/v1/tts/speak", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ text })
      });
      const j = await res.json();
      setStatus(j.ok ? "Spoken ✅" : "Failed ❌");
    } catch (e) {
      console.error(e);
      setStatus("Error ❌ — see console");
    }
  }

  return (
    <div style={{fontFamily:"Inter, system-ui", padding:24, maxWidth:720}}>
      <h1>Virtual Assistant — Speak Test</h1>
      <p>Type something and click Speak. You should hear it from your PC.</p>
      <div style={{display:"flex", gap:8}}>
        <input
          value={text}
          onChange={e=>setText(e.target.value)}
          style={{flex:1, padding:8, border:"1px solid #ccc", borderRadius:8}}
        />
        <button onClick={speak} style={{padding:"8px 16px", borderRadius:8, border:"1px solid #999", cursor:"pointer"}}>
          Speak
        </button>
      </div>
      <div style={{marginTop:12, opacity:0.7}}>{status}</div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
