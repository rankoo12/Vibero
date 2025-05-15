import { createContext, useContext, useEffect, useState } from "react";
import { fetchSession } from "@/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchSession()
      .then(setUser)
      .catch(() => {
        setUser(null);
      });
  }, []);

  const logout = () => {
    setUser(null); // cookie will be cleared on backend later
  };

  return (
    <AuthContext.Provider value={{ user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
