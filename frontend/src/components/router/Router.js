import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import { useAuth } from '../../context/Auth';
import Home from '../home/Home';
import Login from '../login/Login';
import Register from '../register/Register';

const Router = () => {
  const token = useAuth().token;
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/login">
          {!token ? (<Login/>) : (<Redirect to="/" />)}
        </Route>
        <Route path="/register">
          {!token ? (<Register/>) : (<Redirect to="/" />)}
        </Route>
      </Switch>
    </BrowserRouter>
  )
}

export default Router;