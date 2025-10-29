import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import AdminDashboard from "./pages/admin/AdminDashboard";
import DeveloperDashboard from "./pages/developer/DeveloperDashboard";
import TeamLeaderDashboard from "./pages/team_leader/TeamLeaderDashboard";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/admin" element={<AdminDashboard />} />
      <Route path="/developer" element={<DeveloperDashboard />} />
      <Route path="/team_leader" element={<TeamLeaderDashboard />} />
    </Routes>
  );
}

export default App;

