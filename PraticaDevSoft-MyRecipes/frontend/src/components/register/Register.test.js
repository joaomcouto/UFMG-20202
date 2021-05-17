import { mount } from 'enzyme';


import Register from "./Register";
import Form from 'react-bootstrap/Form';
import {AuthContext} from '../../context/Auth';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';

describe('<Register />', () => {
  let component, setFormData, useStateSpy, setHasError, setIsFormValid, fetchSpy;

  let user = null;
  const setUser = jest.fn().mockImplementation(newUser => {
    console.log("Being called")
    user = newUser
  });
  
  beforeEach(() => {
    setFormData = jest.fn();
    setHasError = jest.fn();
    setIsFormValid = jest.fn();

    useStateSpy = jest.spyOn(React, 'useState');
    fetchSpy = jest.spyOn(window, 'fetch');
    useStateSpy.mockImplementationOnce(init => [init, setHasError]);
    useStateSpy.mockImplementationOnce(init => [init, setIsFormValid]);
    useStateSpy.mockImplementationOnce(init => [init, setFormData]);
    component = mount(
      <BrowserRouter>
        <AuthContext.Provider value={{user, setUser}}>
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

  // it('should call setHasError when form is submitted with invalid data', () => {
  //   fetchSpy.mockImplementation(() => {
  //     return Promise.resolve({
  //       status: 400,
  //       json:() => {
  //         return Promise.resolve({
  //           email: "vitor@email.com",
  //           password: 1234567
  //         })
  //       }
  //     })
  //   })
  //   component.find(Form).simulate('submit');
  //   expect(setHasError).toHaveBeenCalled();
  // });

  // it('should redirect when form is submitted with valid data', () => {
  //   fetchSpy.mockImplementation(() => {
  //     return Promise.resolve({
  //       status: 200,
  //       json:() => {
  //         return Promise.resolve({
  //           UserId: 1,
  //           email: "vitor@email.com",
  //           password: 12345678
  //         })
  //       }
  //     })
  //   })
  //   component.find(Form).simulate('submit');
  //   expect(setUser).toBeCalled();
  // });

});