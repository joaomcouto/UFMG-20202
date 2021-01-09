import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from '../home/Home';
import Login from '../login/Login';
import Register from '../register/Register';

const Router = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="/login">
          <Login/>
        </Route>
        <Route path="/register">
          <Register/>
        </Route>
      </Switch>
    </BrowserRouter>
  )
}

export default Router;