import { useEffect, useRef, useState } from "react";
import { connectChatWS } from "../lib/ws";
import { sessionId } from "../lib/id";

type Msg = { role: "user" | "assistant"; content: string };

export default function Chat() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const wsRef = useRef<WebSocket | null>(null);

  // load history once
  useEffect(() => {
    const sid = sessionId();
    fetch(`/api/v1/messages?session_id=${encodeURIComponent(sid)}`)
      .then(r => r.json())
      .then((rows: any[]) => {
        setMessages(rows.map(r => ({ role: r.role, content: r.content })));
      })
      .catch(() => {});
  }, []);

  // open WS
  useEffect(() => {
    const ws = connectChatWS((t) => {
      setMessages((m) => [...m, { role: "assistant", content: t }]);
      if (autoSpeak) speakText(t);
    });
    wsRef.current = ws;
    return () => ws.close();
  }, []);

  const [autoSpeak, setAutoSpeak] = useState(false);

  function send() {
    const text = input.trim();
    if (!text || !wsRef.current) return;
    wsRef.current.send(text);
    setMessages((m) => [...m, { role: "user", content: text }]);
    setInput("");
  }

  async function uploadAudio(file: File) {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch("/api/v1/stt/transcribe", { method: "POST", body: fd });
    const json = await res.json();
    const text = json?.text || "";
    if (text) setInput(text);
  }

  async function speakText(text: string) {
    const res = await fetch("/api/v1/tts/speak", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
  }

  return (
    <div className="min-h-screen p-6 max-w-3xl mx-auto flex flex-col gap-4">
      <h1 className="text-2xl font-semibold">Chat</h1>

      <div className="flex items-center gap-3">
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={autoSpeak} onChange={(e) => setAutoSpeak(e.target.checked)} />
          Auto-speak replies
        </label>
        <button
          onClick={() => messages.length && speakText(messages[messages.length - 1].content)}
          className="px-3 py-2 rounded-lg border"
        >
          🔊 Speak last reply
        </button>
      </div>

      <div className="flex-1 border rounded-xl p-4 overflow-auto">
        {messages.map((m, i) => (
          <div key={i} className={`mb-2 ${m.role === "user" ? "text-right" : "text-left"}`}>
            <span className={`inline-block px-3 py-2 rounded-lg ${m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-200"}`}>
              {m.content}
            </span>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          className="flex-1 border rounded-lg px-3 py-2"
          placeholder="Type a message"
        />
        <button onClick={send} className="px-4 py-2 rounded-lg bg-black text-white">Send</button>

        <label className="px-3 py-2 border rounded-lg cursor-pointer">
          Mic (upload .wav/.mp3)
          <input
            type="file"
            accept="audio/*"
            hidden
            onChange={(e) => e.target.files && e.target.files[0] && uploadAudio(e.target.files[0])}
          />
        </label>
      </div>
    </div>
  );
}
