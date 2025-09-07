import { sessionId } from "./id";

export function connectChatWS(onMessage: (t: string) => void) {
  const sid = sessionId();
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${proto}://${location.host}/ws/chat?session_id=${encodeURIComponent(sid)}`);
  ws.onmessage = (e) => onMessage(String(e.data || ""));
  return ws;
}
