import { Link, useLocation } from 'react-router-dom';
import { useAuth } from "@/context/AuthContext";

export default function Navbar() {
  const location = useLocation();
  const { user } = useAuth();  // ✅ now we can check login

  return (
    <nav className="nav-style">
      <div className="text-xl font-bold">
        <Link to="/">
          <img src="/src/assets/logo.png" alt="Vibero Logo" className="h-14" />
        </Link>
      </div>
      <div className="flex space-x-6">
        <Link to="/" className={`text-lg font-medium hover:text-blue-300 ${
          location.pathname === '/' ? 'underline text-blue-400' : 'text-white no-underline'
        }`}>Home</Link>

        {user && (
          <Link to={`/store/${user.username}`} className={`text-lg font-medium hover:text-blue-300 ${
            location.pathname.startsWith('/store') ? 'underline text-blue-400' : 'text-white no-underline'
          }`}>My Store</Link>
        )}

        {user ? (
          <div className="text-lg font-medium hover:text-blue-300">{user.username}</div>  // 🔜 Replace with dropdown
        ) : (
          <Link to="/login" className={`text-lg font-medium hover:text-blue-300 ${
            location.pathname === '/login' ? 'underline text-blue-400' : 'text-white no-underline'
          }`}>Login</Link>
        )}
      </div>
    </nav>
  );
}
