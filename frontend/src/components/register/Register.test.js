import { mount } from 'enzyme';


import Register from "./Register";
import Form from 'react-bootstrap/Form';
import {AuthContext} from '../../context/Auth';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import * as fetch from '../../util/fetch';

describe('<Register />', () => {
  let component, setFormData, useStateSpy, setHasError, setIsFormValid;
  const runAllPromises = () => new Promise(setImmediate);

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
          <Register/>
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
    const input = component.find('#name').at(0);

    input.value = 'Vitor';

    input.simulate('change');

    expect(setFormData).toHaveBeenCalled();
  });

  it('should check if form is validated on input change', () => {
    const fields = {
      name: "Vitor",
      email: "vitor@email.com",
      password: 12345678,
      passwordConfirmation: 12345678
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

  it.skip('should call hasError when form is invalid', async () => {

    const fetchSpy = jest.spyOn(fetch, 'post');

    fetchSpy.mockReturnValue({status: 401, error: 'Email já cadastradado'});

    await runAllPromises();
    expect(setHasError).toHaveBeenCalled();
  })
});