import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import UserStore from './pages/UserStore'
import './index.css'
import Navbar from './components/Navbar'


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
    <div className="min-h-screen w-full overflow-x-hidden">
  <Navbar />
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/store/:username" element={<UserStore />} />
  </Routes>
  </div>
</BrowserRouter>

  </React.StrictMode>
)
