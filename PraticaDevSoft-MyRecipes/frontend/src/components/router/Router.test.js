import { shallow } from 'enzyme';
import { BrowserRouter, Switch} from 'react-router-dom';
import Home from '../home/Home';
import Login from '../login/Login';
import * as AuthContext from '../../context/Auth';

import Router from './Router';
import Register from '../register/Register';

describe("<Router />", () => {
  let component;

  beforeEach(() => {
    component = shallow(<Router/>);
  });

  it('should render one BrowserRouter', () => {
    expect(component.find(BrowserRouter)).toHaveLength(1);
  });

  it('should render on Switch', () => {
    expect(component.find(Switch)).toHaveLength(1);  
  });

  it('should render one route to home component', () => {
    const homeRoute = component.find({path: '/'});
    
    expect(homeRoute).toHaveLength(1);
    expect(homeRoute.prop('component')).toBe(Home);
  });

  it('should render one route to login component when user is not authenticated', () => {
    const loginRoute = component.find({path: '/login'});
    
    expect(loginRoute).toHaveLength(1);
    expect(loginRoute.children().type()).toBe(Login);

  });

  

  it('should render one route to register component when user is not authenticated', () => {
    const registerRoute = component.find({path: '/register'});
    
    expect(registerRoute).toHaveLength(1);
    expect(registerRoute.children().type()).toBe(Register);

  });

  it('should render a redirect when user is authenticated', () => {
    const contextValues = {
      user: {id: 2, name: 'Vitor'},
      setToken: null
    };

    jest.spyOn(AuthContext, 'useAuth').mockImplementation(() => contextValues);

    const contextComponent = shallow(<Router />);

    const redirect = contextComponent.find({to: "/"});

    expect(redirect).toHaveLength(2);
  });
})