import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import { useAuth } from '../../context/Auth';
import Login from '../login/Login';
import Create from '../recipes/recipe/Create/Create';
import List from '../recipes/list/List';
import Register from '../register/Register';
import Home from '../home/Home';

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
        <Route path="/recipes" component={List}/>
      </Switch>
    </BrowserRouter>
  )
}

export default Router;