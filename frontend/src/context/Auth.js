import { createContext, useContext } from 'react';


export const defaultContext = {
  token: null,
  setToken: (token) => {localStorage.setItem("token", JSON.stringify(token))}
}

export const AuthContext = createContext(defaultContext);

export const useAuth = () => {
  return useContext(AuthContext);
}