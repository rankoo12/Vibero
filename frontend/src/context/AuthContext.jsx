import { createContext, useContext, useEffect, useState } from "react";
import { fetchSession } from "@/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSession()
      .then(setUser)
      .catch(() => {
        // don't force reset — let UI render previous state if any
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const logout = () => {
    setUser(null);
  };

  // ✅ Block rendering until session is resolved
  if (loading) return null;

  return (
    <AuthContext.Provider value={{ user, setUser, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
