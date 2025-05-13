import { Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import UserStore from '../pages/UserStore';
import GamePage from '../pages/GamePage';
import RegisterPage from "../pages/Register";
import LoginPage from "../pages/Login";
// You can import Store, GamePage, etc. later

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/store/:username" element={<UserStore />} />
      <Route path="/store/:username/:gameId" element={<GamePage />} />
      
      {/* 🔐 Auth routes */}
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
      {/* Add future routes like /store and /store/:gameId here */}
    </Routes>
  );
}
