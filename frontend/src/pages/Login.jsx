import { useState } from "react";
import { loginUser } from "@/api";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";



export default function LoginPage() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [token, setToken] = useState(null);
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();



  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  setSuccess("");

  try {
    const data = await loginUser(form);
    setToken(data.access_token);
    localStorage.setItem("token", data.access_token);
    setSuccess("Logged in successfully!");
    setTimeout(() => navigate("/"), 1000); // small delay to show success
  } catch (err) {
    setError(err.message || "Login failed");
  }
};


  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-zinc-800 text-white rounded-xl shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>
      <form onSubmit={handleSubmit} className="space-y-4 w-full">
        <div className="flex justify-center">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-[90%] px-4 py-2  rounded outline-none"
          required
        />
        </div>
        <div className="flex justify-center">
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-[90%] px-4 py-2  rounded outline-none"
          required
        />
        </div>
        <button type="submit" className="w-full bg-violet-600 hover:bg-violet-500 p-2 rounded">
          Login
        </button>
        
      </form>

      <p className="text-sm text-center mt-4">
  Not registered?{" "}
  <Link to="/register" className="text-violet-400 hover:underline">
    Create an account
  </Link>
</p>

      {error && <p className="text-red-400 text-center mt-4">{error}</p>}
      {success && <p className="text-green-400 text-center mt-4">{success}</p>}

    </div>
  );
}
