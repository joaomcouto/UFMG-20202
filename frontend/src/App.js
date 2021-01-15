import React, { useState } from 'react';
import './App.css';

import Header from './components/header/Header';
import Router from './components/router/Router';
import { AuthContext } from './context/Auth';

function App() {
  const token = JSON.parse(localStorage.getItem('token'));
  const [authToken, setAuthToken] = useState(token);

  const setToken = (token) => {
    localStorage.setItem("token", JSON.stringify(token));
    setAuthToken(token);
  }

  return (
    <div className={['d-flex', 'flex-column', 'h-100'].join` `}>
      <AuthContext.Provider value={{authToken, setToken}}>
        <Header />
        <Router/>
      </AuthContext.Provider>
    </div>
  );
}

export default App;
