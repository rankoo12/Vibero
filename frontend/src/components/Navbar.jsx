import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
    const location = useLocation();
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
          }`}>Home </Link>
        <Link to="/store/rankoo12" className={`text-lg font-medium hover:text-blue-300 ${
            location.pathname.startsWith('/store') ? 'underline text-blue-400' : 'text-white no-underline'
          }`}>My Store</Link>
      </div>
    </nav>
  );
}
