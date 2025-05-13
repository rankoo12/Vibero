import { useState } from "react";
import { registerUser } from "@/api";
import { useNavigate } from "react-router-dom";


export default function RegisterPage() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
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
    const response = await registerUser(form);
    setSuccess("User registered! Redirecting to login...");
    setTimeout(() => navigate("/login"), 3000); // Wait 1s then redirect
  } catch (err) {
    setError(err.message || "Registration failed");
  }
};


  return (
    //max-w-md w-full
    //min-h-screen flex
    //<div className="w-full max-w-md p-6 bg-zinc-800 text-white rounded-xl shadow-lg">
    <div className="max-w-md mx-auto mt-10 p-6 bg-zinc-800 text-white rounded-xl shadow-lg">
    <h1 className="text-2xl font-bold mb-6 text-center">Register</h1>
    <form onSubmit={handleSubmit} className="space-y-4 w-full">
      <div className="flex justify-center">
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          className="w-[90%] px-4 py-2  rounded outline-none"
          required
        />
      </div>
      <div className="flex justify-center">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-[90%] px-4 py-2 rounded outline-none"
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
          className="w-[90%] px-4 py-2 rounded outline-none"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full bg-violet-600 hover:bg-violet-500 py-2 rounded shadow"
      >
        
        Create Account
      </button>
    </form>
    {error && (
  <p className="text-red-400 text-center mt-4">{error}</p>
)}

{success && (
  <p className="text-green-400 text-center mt-4">{success}</p>
)}

  </div>
  );
}
