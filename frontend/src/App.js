import React, { useState, useEffect } from 'react';
import './App.css';

import Header from './components/header/Header';
import Router from './components/router/Router';
import { AuthContext } from './context/Auth';

function App() {

  const [user, saveUser] = useState(null);
  const setUser = (user) => {
    localStorage.setItem("user", JSON.stringify(user));
    saveUser(user);
  }

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    saveUser(user);
  }, []);

  return (
    <div className={['d-flex', 'flex-column', 'h-100'].join` `}>
      <AuthContext.Provider value={{user, setUser}}>
        <Header logout={setUser}/>
        <Router/>
      </AuthContext.Provider>
    </div>
  );
}

export default App;
