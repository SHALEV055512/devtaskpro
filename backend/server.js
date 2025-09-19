import express from "express";
import cors from "cors";

const app = express();
const PORT = process.env.PORT || 5000;
app.use(cors());

app.get("/api/health", (req, res) => {
  res.json({ status: "backend is up 🚀" });
});

app.listen(PORT, () => {
  console.log(`✅ Backend running on http://localhost:${PORT}`);
});
