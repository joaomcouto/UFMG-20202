import { createContext, useContext } from 'react';


export const defaultContext = {
  user: null,
  setUser: (user) => {localStorage.setItem("user", JSON.stringify(user))}
}

export const AuthContext = createContext(defaultContext);

export const useAuth = () => {
  return useContext(AuthContext);
}