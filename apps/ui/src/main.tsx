// apps/ui/src/main.tsx
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App"; // <-- Import your main App

// Render the main <App /> component
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);