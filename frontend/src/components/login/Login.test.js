import { mount } from 'enzyme';


import Login from "./Login";
import Form from 'react-bootstrap/Form';
import {AuthContext} from '../../context/Auth';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';

describe('<Login />', () => {
  let component;
  const setFormData = jest.fn();
  const useStateSpy = jest.spyOn(React, 'useState')
  useStateSpy.mockImplementation((init) => [init, setFormData]);
  
  const context = {
    token: null,
    setToken: token => localStorage.setItem("token", JSON.stringify(token))
  }
  beforeEach(() => {
    component = mount(
      <BrowserRouter>
        <AuthContext.Provider value={context}>
          <Login/>
        </AuthContext.Provider>
      </BrowserRouter>
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should render the form', () => {
    expect(component.find(Form)).toHaveLength(1);
  });
});