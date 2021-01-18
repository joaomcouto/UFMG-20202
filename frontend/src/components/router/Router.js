import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import { useAuth } from '../../context/Auth';
import Home from '../home/Home';
import Login from '../login/Login';
import Create from '../recipes/recipe/Create/Create';
import Register from '../register/Register';

const Router = () => {
  const user = useAuth().user;

  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/login">
          {!user ? (<Login/>) : (<Redirect to="/" />)}
        </Route>
        <Route path="/register">
          {!user ? (<Register/>) : (<Redirect to="/" />)}
        </Route>
        <Route path="/recipes/new" component={Create}/>
      </Switch>
    </BrowserRouter>
  )
}

export default Router;