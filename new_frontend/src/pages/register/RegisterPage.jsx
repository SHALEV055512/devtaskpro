import { useState, useEffect } from "react";
import { Eye, EyeOff } from "lucide-react";
import "./register.css";
import { registerUser } from "../../api";
import { useNavigate } from "react-router-dom";

function RegisterPage() {
  // -------------------------------------------------------
  // 1. STATE MANAGEMENT
  // -------------------------------------------------------
  const [showPassword, setShowPassword] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);
  const [errors, setErrors] = useState([]);
  const [successMessage, setSuccessMessage] = useState("");
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    team: "",
    gender: "",
    role: "",
  });

  // -------------------------------------------------------
  // 2. INPUT HANDLERS
  // -------------------------------------------------------
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // -------------------------------------------------------
  // 3. FORM SUBMISSION LOGIC
  // -------------------------------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // --- Send registration request ---
      const data = await registerUser(formData);
      console.log("✅ User created successfully:", data);

      // --- If registration succeeded ---
      setSuccessMessage(data.message); // message comes directly from backend
      setErrors([]);
      setShowOverlay(true);
    } catch (error) {
      console.error("❌ Registration failed:", error);

      // --- Extract validation details from FastAPI response ---
      const detail = error.response?.data?.detail;
      if (Array.isArray(detail)) {
        setErrors(detail.map((err) => err.msg));
      } else if (typeof detail === "string") {
        setErrors([detail]);
      } else {
        setErrors(["Registration failed. Please check your input."]);
      }

      setShowOverlay(true);
    }
  };

  // -------------------------------------------------------
  // 4. GLOBAL LISTENER (ESC TO CLOSE OVERLAY)
  // -------------------------------------------------------
  useEffect(() => {
    function handleKey(e) {
      if (e.key === "Escape") setShowOverlay(false);
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, []);

  // -------------------------------------------------------
  // 5. JSX RENDERING
  // -------------------------------------------------------
  return (
    <div className="register-container">
      {/* --- LEFT SIDE TEXT SECTION --- */}
      <div className="register-left">
        <h2 className="logo-text">Strategix</h2>
        <h1 className="main-heading">Where strategy turns into execution.</h1>
        <p className="sub-heading">
          Take control of projects and empower your team to deliver results.
        </p>
      </div>

      {/* --- RIGHT SIDE FORM SECTION --- */}
      <div className="register-right">
        <div className="form-wrapper">
          <h1 className="form-title">Create an account</h1>

          <form className="register-form" onSubmit={handleSubmit}>
            <div className="form-fields">
              {/* --- First + Last name --- */}
              <div className="name-fields">
                <input
                  type="text"
                  name="firstname"
                  placeholder="First name"
                  value={formData.firstname}
                  onChange={handleChange}
                  required
                />
                <input
                  type="text"
                  name="lastname"
                  placeholder="Last name"
                  value={formData.lastname}
                  onChange={handleChange}
                  required
                />
              </div>

              {/* --- Email --- */}
              <input
                type="email"
                name="email"
                placeholder="Email"
                className="full-width"
                value={formData.email}
                onChange={handleChange}
                required
              />

              {/* --- Password --- */}
              <div className="password-wrapper">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Password"
                  className="full-width"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                {showPassword ? (
                  <Eye
                    size={20}
                    className="eye-icon"
                    onClick={() => setShowPassword(false)}
                  />
                ) : (
                  <EyeOff
                    size={20}
                    className="eye-icon"
                    onClick={() => setShowPassword(true)}
                  />
                )}
              </div>

              {/* --- Team --- */}
              <input
                type="number"
                name="team"
                placeholder="Team"
                className="full-width"
                value={formData.team}
                onChange={handleChange}
                required
              />

              {/* --- Gender --- */}
              <select
                id="gender"
                name="gender"
                className="full-width"
                value={formData.gender}
                onChange={handleChange}
                required
              >
                <option value="">Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer not to say</option>
              </select>

              {/* --- Role --- */}
              <select
                id="role"
                name="role"
                className="full-width"
                value={formData.role}
                onChange={handleChange}
                required
              >
                <option value="">Role</option>
                <option value="Admin">Admin</option>
                <option value="Team leader">Team leader</option>
                <option value="Developer">Developer</option>
              </select>

              {/* --- Submit Button --- */}
              <button type="submit" className="submit-btn">
                <strong>Sign up</strong>
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* -------------------------------------------------------
         6. OVERLAY (ERRORS OR SUCCESS FEEDBACK)
      ------------------------------------------------------- */}
      {showOverlay && (
        <div
          className="error-overlay"
          onClick={() => {
            setShowOverlay(false);
            if (successMessage) {
              navigate("/login");
            }
          }}
        >
          <div
            className={`error-modal ${successMessage ? "success" : ""}`}
            onClick={(e) => e.stopPropagation()}
          >
            {successMessage ? (
              <>
                <h2>Success</h2>
                <ul>
                  <li style={{ color: "#16a34a", fontWeight: "600" }}>
                    {successMessage}
                  </li>
                </ul>
                <p className="hint">Click anywhere to continue</p>
              </>
            ) : (
              <>
                <h2>Validation Errors</h2>
                <ul>
                  {errors.map((err, i) => (
                    <li key={i}>{err}</li>
                  ))}
                </ul>
                <p className="hint">Click anywhere to close</p>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default RegisterPage;
