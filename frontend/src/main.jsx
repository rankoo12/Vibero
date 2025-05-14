import React from 'react'
import ReactDOM from 'react-dom/client'
import { AuthProvider } from './context/AuthContext.jsx';
import { BrowserRouter } from 'react-router-dom'
import AppRoutes from './routes/AppRoutes'
import Navbar from './components/Navbar'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
    <BrowserRouter>
      <div className="min-h-screen w-full overflow-x-hidden">
        <Navbar />
        <AppRoutes />
      </div>
    </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>,
)
