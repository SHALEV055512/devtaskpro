import "./login.css";
import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  

  const navigate = useNavigate();

  // ✅ הפונקציה שתופעל בלחיצה על הכפתור
  const handleSubmit = async (e) => {
    e.preventDefault(); // לא לרענן את הדף
    setError("");

    try {
      const res = await fetch("http://localhost:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      console.log("🔥 Response from backend:", data);



      // ✅ ניתוב לפי role שהתקבל מהבקאנד
if (data.msg || data.role?.msg) {
  setError(data.msg || data.role.msg);
  return;
}
const rawRole = data.role?.role || data.role;
const role = typeof rawRole === "string" ? rawRole.trim().toLowerCase() : "";
console.log("🎯 Parsed role:", role);

if (role === "admin") navigate("/admin");
else if (role === "developer") navigate("/developer");
else if (role === "team_leader") navigate("/team_leader");
else setError("Unknown role");
    } catch (err) {
      console.error(err);
      setError("Network error");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Sign in</h1>
        <p>
          Don't have an account?{" "}
          <Link to="/register">
            <strong>Sign up</strong>
          </Link>
        </p>
 <form onSubmit={handleSubmit}>
  <div className="email-wrapper">
    <input
      type="email"
      placeholder="Email"
      className="input-field"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      required
    />
  </div>

  <div className="password-wrapper">
    <input
      type={showPassword ? "text" : "password"}
      placeholder="Password"
      className="input-field"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      required
    />
    {showPassword ? (
      <EyeOff
        size={25}
        className="eye-icon"
        onClick={() => setShowPassword(false)}
      />
    ) : (
      <Eye
        size={25}
        className="eye-icon"
        onClick={() => setShowPassword(true)}
      />
    )}
  </div>

  {error && <p style={{ color: "red" }}>{error}</p>}

  <Link to="/forgot_password" className="forgot-password">
  Forgot your password?
  </Link>

  <button type="submit" className="login-button">Sign in</button>
</form>

       
 </div>
  </div>

  );
}

export default LoginPage;



