import { mount } from 'enzyme';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Header from './Header';
import { AuthContext, defaultContext } from '../../context/Auth';

describe("<Header/>", () => {
  let component;
  beforeEach(() => {
    component = mount(<Header />);
  });

  it('should render one navbar', () => {
    expect(component.find(Navbar)).toHaveLength(1);
  });

  it('should render three nav links when user is not logged', () => {
    expect(component.find(Nav.Link)).toHaveLength(3);
  })

  it('should render three nav links and two button when is user logged', () => {    
    const context = {
      user: {name: 'vitor', email: 'vitor@email.com', id: 1},
      setUser: defaultContext.setUser
    };

    const contextComponent = mount(
      <AuthContext.Provider value={context}>
        <Header />
      </AuthContext.Provider>
    );

    expect(contextComponent.find(Nav.Link)).toHaveLength(1);
    expect(contextComponent.find(Button)).toHaveLength(2)
  });

  it('should remove the token from localstorage on logout', () => {
    localStorage.setItem("user", JSON.stringify({name: 'vitor', email: 'vitor@email.com', id: 1}));

    const context = {
      user: {name: 'vitor', email: 'vitor@email.com', id: 1},
      setUser: defaultContext.setUser
    };

    const contextComponent = mount(
      <AuthContext.Provider value={context}>
        <Header logout={context.setUser}/>
      </AuthContext.Provider>
    );

    const logoutButton = contextComponent.find('#logout').at(0);

    logoutButton.simulate('click');

    const localToken = JSON.parse(localStorage.getItem("user"))
    expect(localToken).toBe(null);
  });
})