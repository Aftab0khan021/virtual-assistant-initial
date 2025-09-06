import React from "react";
export type Msg = { role: "user" | "assistant"; text: string };

export default function ChatPane({ messages }: { messages: Msg[] }) {
  return (
    <div style={{border:"1px solid #eee", borderRadius:12, padding:16, marginTop:16, maxWidth:720}}>
      {messages.length === 0 ? <div style={{opacity:0.6}}>Say something…</div> : null}
      {messages.map((m, i) => (
        <div key={i} style={{marginBottom:12}}>
          <b>{m.role === "user" ? "You" : "Assistant"}:</b> {m.text}
        </div>
      ))}
    </div>
  );
}
