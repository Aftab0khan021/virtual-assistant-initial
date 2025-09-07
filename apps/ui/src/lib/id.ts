export function sessionId(): string {
  let id = localStorage.getItem("va_session_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("va_session_id", id);
  }
  return id!;
}
