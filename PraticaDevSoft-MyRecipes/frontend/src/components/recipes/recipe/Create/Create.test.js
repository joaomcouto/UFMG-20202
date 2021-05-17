import { mount } from 'enzyme';

import { AuthContext } from '../../../../context/Auth';
import FormControl from 'react-bootstrap/FormControl';
import Create from "./Create";
import React from 'react';

describe('<Create />', () => {
  let component;
  let useStateSpy, fetchSpy, alertSpy, useEffectSpy;
  let setError, setRecipeId, setFormData,  setImageUrl, setFormSent;

  const context = {
    user: {id: 1, name: 'Vitor'}
  };


  const mockData = {
    title: "Brigadeiro",
    time: 0,
    servings: 10,
    ingredients: "Leite condensado e chocolate",
    howTo: "Jogar na panela",
  }
  beforeEach(() => {
    setError = jest.fn();
    setRecipeId = jest.fn();
    setFormData = jest.fn();
    setImageUrl = jest.fn();
    setFormSent = jest.fn();

    fetchSpy = jest.spyOn(global, 'fetch');

    alertSpy = jest.spyOn(window, 'alert');
    alertSpy.mockImplementation(() => {})
    
    useStateSpy = jest.spyOn(React, 'useState');
    useStateSpy.mockImplementationOnce(init => [init, setError]);
    useStateSpy.mockImplementationOnce(init => [init, setRecipeId]);
    useStateSpy.mockImplementationOnce(() => [mockData, setFormData]);
    useStateSpy.mockImplementationOnce(init => [init, setImageUrl]);
    useStateSpy.mockImplementationOnce(init => [init, setFormSent]);

    fetchSpy.mockImplementationOnce(() => {
      return Promise.resolve({
        status: 200,
        json: () => {
          return Promise.resolve({
            id: 1
          })
        }
      })
    })

    component = mount(
      <AuthContext.Provider value={context}>
        <Create/>
      </AuthContext.Provider>
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should render the two textareas and three inputs', () => {
    expect(component.find(FormControl)).toHaveLength(3);
    expect(component.find('textarea')).toHaveLength(2);
  });

  it('should handle title changes', () => {
    const input = component.find('#title').at(0);

    input.value = 'Brigadeiro';

    input.simulate('change');

    expect(setFormData).toHaveBeenCalled();
  });

  it('should handle ingredients changes', () => {
    const input = component.find('#ingredients').at(0);

    input.value = '500 ml de água';

    input.simulate('change');

    expect(setFormData).toHaveBeenCalled();
  });

  it('should handle howTo changes', () => {
    const input = component.find('#howTo').at(0);

    input.value = 'Ferva a água';

    input.simulate('change');

    expect(setFormData).toHaveBeenCalled();
  });

  it('should call hasError when submitting form with no data', () => {
    const submit = component.find('#submit').at(0);

    submit.simulate('click');

    expect(setError).toHaveBeenCalled()
  });

  it.skip('should handle success on saving recipe', () => {    
    for(let prop in mockData){
      const input = component.find(`#${prop}`).at(0);
      input.value = mockData[prop];
      input.simulate('change');
    }

    const submit = component.find('#submit').at(0);
    submit.simulate('click');
    expect(setRecipeId).toHaveBeenCalled();
    expect(setFormSent).toHaveBeenCalled();
  })
});