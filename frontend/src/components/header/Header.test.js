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

  it('should render two nav links and a button when is user logged', () => {    
    const context = {
      token: 12345,
      setToken: defaultContext.setToken
    };

    const contextComponent = mount(
      <AuthContext.Provider value={context}>
        <Header />
      </AuthContext.Provider>
    );

    expect(contextComponent.find(Nav.Link)).toHaveLength(2);
    expect(contextComponent.find(Button)).toHaveLength(1)
  });

  it('should remove the token from localstorage on logout', () => {
    localStorage.setItem("token", JSON.stringify(12345));

    const context = {
      token: 12345,
      setToken: defaultContext.setToken
    };

    const contextComponent = mount(
      <AuthContext.Provider value={context}>
        <Header logout={context.setToken}/>
      </AuthContext.Provider>
    );

    const logoutButton = contextComponent.find(Button);

    logoutButton.simulate('click');

    const localToken = JSON.parse(localStorage.getItem("token"))
    expect(localToken).toBe(null);
  });
})