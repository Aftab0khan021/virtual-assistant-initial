import { useEffect, useRef, useState } from "react";
import { connectChatWS } from "../lib/ws";
import { sessionId } from "../lib/id";

type Msg = { role: "user" | "assistant"; content: string };

export default function Chat() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [autoSpeak, setAutoSpeak] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  // --- NEW FOR REAL-TIME MIC ---
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  // -----------------------------

  useEffect(() => {
    const sid = sessionId();
    fetch(`/api/v1/messages?session_id=${encodeURIComponent(sid)}`)
      .then(r => r.json()).then((rows: any[]) =>
        setMessages(rows.map(r => ({ role: r.role, content: r.content })))
      ).catch(()=>{});
  }, []);

  useEffect(() => {
    const ws = connectChatWS((t) => {
      setMessages((m) => [...m, { role: "assistant", content: t }]);
      if (autoSpeak) speakText(t);
    });
    wsRef.current = ws;
    return () => ws.close();
  }, [autoSpeak]);

  // --- MODIFIED send ---
  // Now accepts an optional text argument to send directly
  function send(textToSend?: string) {
    const text = (textToSend || input).trim(); // Use provided text or text from state
    if (!text || !wsRef.current) return;
    wsRef.current.send(text);
    setMessages((m) => [...m, { role: "user", content: text }]);
    setInput(""); // Clear input after sending
  }

  // --- MODIFIED uploadAudio ---
  // Now accepts an 'autoSend' flag
  async function uploadAudio(file: File, autoSend: boolean = false) {
    const fd = new FormData();
    fd.append("file", file);
    // Calls the backend STT endpoint
    const res = await fetch("/api/v1/stt/transcribe", { method: "POST", body: fd });
    const json = await res.json();
    if (json?.text) {
      setInput(json.text); // Put transcribed text in input box
      if (autoSend) {
        send(json.text); // And automatically send it as a chat message
      }
    }
  }

  async function speakText(text: string) {
    // Calls the backend TTS endpoint
    const res = await fetch("/api/v1/tts/speak", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const blob = await res.blob();
    new Audio(URL.createObjectURL(blob)).play();
  }

  // --- NEW startRecording ---
  async function startRecording() {
    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" }); // Use webm format
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      // Store audio data as it comes in
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      // When recording stops...
      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        const audioFile = new File([audioBlob], "recording.webm", { type: "audio/webm" });
        
        // ...send the file to our existing uploadAudio function
        // and set autoSend to true
        uploadAudio(audioFile, true); 
        
        // Clean up microphone stream
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error starting recording:", err);
      alert("Microphone access denied. Please allow microphone access in your browser settings.");
    }
  }

  // --- NEW stopRecording ---
  function stopRecording() {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }

  return (
    <div className="min-h-screen p-6 max-w-3xl mx-auto flex flex-col gap-4">
      <h1 className="text-2xl font-semibold">Chat</h1>

      <div className="flex items-center gap-3">
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={autoSpeak} onChange={(e)=>setAutoSpeak(e.target.checked)} />
          Auto-speak replies
        </label>
        <button onClick={()=>messages.length && speakText(messages[messages.length-1].content)}
          className="px-3 py-2 rounded-lg border">🔊 Speak last reply</button>
      </div>

      <div className="flex-1 border rounded-xl p-4 overflow-auto">
        {messages.map((m,i)=>(
          <div key={i} className={`mb-2 ${m.role==="user"?"text-right":"text-left"}`}>
            <span className={`inline-block px-3 py-2 rounded-lg ${m.role==="user"?"bg-blue-600 text-white":"bg-gray-200"}`}>
              {m.content}
            </span>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input value={input} onChange={(e)=>setInput(e.target.value)}
          onKeyDown={(e)=>e.key==="Enter"&&send()} className="flex-1 border rounded-lg px-3 py-2"
          placeholder="Type a message" />
        <button onClick={() => send()} className="px-4 py-2 rounded-lg bg-black text-white">Send</button>
        
        {/* --- REPLACED BUTTON --- */}
        {/* This is the new "Hold to Speak" button */}
        <button
          onMouseDown={startRecording}   // Start on click
          onMouseUp={stopRecording}      // Stop on release
          onTouchStart={startRecording}  // For mobile
          onTouchEnd={stopRecording}     // For mobile
          className={`px-4 py-2 rounded-lg ${isRecording ? 'bg-red-600 text-white animate-pulse' : 'bg-gray-200'}`}
        >
          {isRecording ? 'Listening...' : 'Hold to Speak'}
        </button>
        {/* --- END OF REPLACEMENT --- */}

      </div>
    </div>
  );
}