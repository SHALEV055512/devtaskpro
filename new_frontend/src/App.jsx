import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import AdminDashboard from "./pages/admin/AdminDashboard";
import DeveloperDashboard from "./pages/developer/DeveloperDashboard";
import TeamLeaderDashboard from "./pages/team_leader/TeamLeaderDashboard";
import VerifyEmailPage from "./pages/email/VerifyEmailPage";
import ForgotPassword from "./pages/email/ForgotPassword";
import ResetPasswordPage from "./pages/email/ResetPasswordPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/admin" element={<AdminDashboard />} />
      <Route path="/developer" element={<DeveloperDashboard />} />
      <Route path="/team_leader" element={<TeamLeaderDashboard />} />
      <Route path="/verify" element={<VerifyEmailPage />} />
      <Route path="/forgot_password" element={<ForgotPassword />} />
      <Route path="/reset_password" element={<ResetPasswordPage />} />

    </Routes>
  );
}

export default App;

