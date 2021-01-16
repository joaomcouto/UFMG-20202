import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import { useAuth } from '../../context/Auth';
import Home from '../home/Home';
import Login from '../login/Login';
import Register from '../register/Register';

const Router = () => {
  const { authToken } = useAuth();
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
          {/* {authToken ? (<Register/>) : (<Redirect to="/" />)}> */}
          <Register/>
        </Route>
      </Switch>
    </BrowserRouter>
  )
}

export default Router;