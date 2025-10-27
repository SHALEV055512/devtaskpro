const isProduction = window.location.hostname !== "localhost";
export const API_BASE_URL = isProduction
  ? "http://51.20.185.146:5000"
  : "http://localhost:5000";
