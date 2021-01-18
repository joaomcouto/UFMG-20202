import { mount } from 'enzyme';


import Login from "./Login";
import Form from 'react-bootstrap/Form';
import {AuthContext} from '../../context/Auth';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';

describe('<Login />', () => {
  let component, setFormData, useStateSpy, setHasError, setIsFormValid;

  
  const context = {
    token: null,
    setToken: token => localStorage.setItem("token", JSON.stringify(token))
  }

  beforeEach(() => {
    setFormData = jest.fn();
    setHasError = jest.fn();
    setIsFormValid = jest.fn();

    useStateSpy = jest.spyOn(React, 'useState')
    useStateSpy.mockImplementationOnce(init => [init, setHasError]);
    useStateSpy.mockImplementationOnce(init => [init, setIsFormValid]);
    useStateSpy.mockImplementationOnce(init => [init, setFormData]);

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

  it('should handle changes', () => {
    const input = component.find('#email').at(0);

    input.value = 'vitor@email.com';

    input.simulate('change');

    expect(setFormData).toHaveBeenCalled();
  });

  it('should check if form is validated on input change', () => {
    const fields = {
      email: "vitor@email.com",
      password: 12345678,
    };

    for(let field in fields){
      
      const input = component.find(`#${field}`).at(0);
      
      input.value = fields[field];
      
      input.simulate('change');
    }

    expect(setIsFormValid).toHaveBeenCalled();
  });

  it('should submit the form', () => {
    component.find(Form).simulate('submit');
  });

});