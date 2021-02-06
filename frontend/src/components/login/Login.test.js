import { mount } from 'enzyme';


import Login from "./Login";
import Form from 'react-bootstrap/Form';
import {AuthContext} from '../../context/Auth';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';

describe('<Login />', () => {
  let component, setFormData, useStateSpy, setHasError, setIsFormValid, fetchSpy;

  
  const user = null;
  const setUser = jest.fn();

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
          <Login/>
        </AuthContext.Provider>
      </BrowserRouter>
    );
  });

  afterEach(() => {
    // jest.restoreAllMocks();
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

  // it('should call setHasError when form is submitted with invalid data', () => {
  //   fetchSpy.mockImplementation(() => {
  //     return Promise.resolve({
  //       status: 200,
  //       json:() => {
  //         return Promise.resolve({
  //           email: "vitor@email.com",
  //           password: 1234567
  //         })
  //       }
  //     })
  //   })
  //   component.find(Form).simulate('submit');
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
  // });

});