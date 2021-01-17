import React, { useState } from 'react';
import './App.css';

import Header from './components/header/Header';
import Router from './components/router/Router';
import { AuthContext } from './context/Auth';

function App() {
  const [token, saveToken] = useState(null);
  const setToken = (token) => {
    localStorage.setItem("token", JSON.stringify(token));
    saveToken(token);
  }

  return (
    <div className={['d-flex', 'flex-column', 'h-100'].join` `}>
      <AuthContext.Provider value={token, setToken}>
        <Header logout={setToken}/>
        <Router/>
      </AuthContext.Provider>
    </div>
  );
}

export default App;
