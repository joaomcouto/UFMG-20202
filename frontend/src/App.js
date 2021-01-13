import React from 'react';
import './App.css';

import Header from './components/header/Header';
import Router from './components/router/Router';

function App() {
  return (
    <div className={['d-flex', 'flex-column', 'h-100'].join` `}>
      <Header />
      
      <Router/>
    </div>
  );
}

export default App;
