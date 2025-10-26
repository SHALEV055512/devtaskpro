import "./login.css";
import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Link } from "react-router-dom"; // אייקונים מודרניים

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);

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

        <div className="email-wrapper">
        <input
            type="email"
            placeholder="Email"
            className="input-field"
           />
       </div>

        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            className="input-field"
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

        <div className="forgot-password">Forgot your password?</div>

        <button className="login-button">Sign in</button>
      </div>
    </div>
  );
}

export default LoginPage;



