import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import "./register.css";
import { registerUser } from "../../api";

function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    team: "",
    gender: "",
    role: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = await registerUser(formData);
      console.log("✅ User created successfully:", data);
      alert("User created successfully!");
    } catch (error) {
      console.error("❌ Registration failed:", error);
      alert(error.message);
    }
  };

  return (
    <div className="register-container">
      <div className="register-left">
        <h2 className="logo-text">Strategix</h2>
        <h1 className="main-heading">Where strategy turns into execution.</h1>
        <p className="sub-heading">
          Take control of projects and empower your team to deliver results.
        </p>
      </div>

      <div className="register-right">
        <div className="form-wrapper">
          <h1 className="form-title">Create an account</h1>

          {/* ✅ חיבור הפונקציה לטופס */}
          <form className="register-form" onSubmit={handleSubmit}>
            <div className="form-fields">
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

              <input
                type="email"
                name="email"
                placeholder="Email"
                className="full-width"
                value={formData.email}
                onChange={handleChange}
                required
              />

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

              <input
                type="number"
                name="team"
                placeholder="Team"
                className="full-width"
                value={formData.team}
                onChange={handleChange}
                required
              />

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

              <button type="submit" className="submit-btn">
                <strong>Sign up</strong>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
