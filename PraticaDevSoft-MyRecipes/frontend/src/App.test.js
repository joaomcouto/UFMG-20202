import { shallow } from 'enzyme';

import App from './App';
import Header from './components/header/Header';
import Router from './components/router/Router';

describe('<App/>', () => {
  let component;

  beforeEach(() => {
    component = shallow(<App/>);
  });

  it('should render a <Header /> and a <Router/>', () => {    
    expect(component.find(Header)).toHaveLength(1);
    expect(component.find(Router)).toHaveLength(1);
  });
});