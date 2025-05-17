import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import apiClient from "@/api/client";

export default function Navbar() {
  const location = useLocation();
  const { user, loading , setUser} = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const navigate = useNavigate();


  return (
    <nav className="nav-style">
      <div className="text-xl font-bold">
        <Link to="/">
          <img src="/src/assets/logo.png" alt="Vibero Logo" className="h-14" />
        </Link>
      </div>
      <div className="flex space-x-6 items-center">
        <Link to="/" className={`text-lg font-medium hover:text-blue-300 ${
          location.pathname === '/' ? 'underline text-blue-400' : 'text-white no-underline'
        }`}>Home</Link>

        {user && (
          <Link to={`/store/${user.username}`} className={`text-lg font-medium hover:text-blue-300 ${
            location.pathname.startsWith('/store') ? 'underline text-blue-400' : 'text-white no-underline'
          }`}>My Store</Link>
        )}

        {loading ? null : (
          user ? (
            <div className="relative inline-block text-left">
              <button
                onClick={() => setShowDropdown(prev => !prev)}
                className="text-lg font-medium text-white hover:text-blue-300 bg-transparent border-none focus:outline-none"
              >
                {user.username}
              </button>
              {showDropdown && (
                <div className="absolute left-0 mt-2 w-32 bg-gray-800 border border-gray-700 rounded shadow-lg z-50">
                  <div className="px-4 py-2 text-sm text-gray-300 cursor-default">
                    Profile
                  </div>
                  <button
                    onClick={async () => {
                      try {
                        await apiClient.post(`/users/${user.username}/logout`);
                        setUser(null);
                        setShowDropdown(false);
                        navigate("/")
                      } catch (err) {
                        console.error("Logout failed", err);
                      }
                    }}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 bg-transparent border-none focus:outline-none"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <Link to="/login" className={`text-lg font-medium hover:text-blue-300 ${
              location.pathname === '/login' ? 'underline text-blue-400' : 'text-white no-underline'
            }`}>Login</Link>
          )
        )}
      </div>
    </nav>
  );
}
