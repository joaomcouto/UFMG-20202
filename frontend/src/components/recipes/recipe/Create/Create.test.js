import { mount } from 'enzyme';

import { AuthContext } from '../../../../context/Auth';
import FormControl from 'react-bootstrap/FormControl';
import Create from "./Create";
import React from 'react';

describe('<Login />', () => {
  let component, setFormData, useStateSpy, setError;
  const context = {
    user: {id: 1, name: 'Vitor'}
  };

  beforeEach(() => {
    setFormData = jest.fn();
    setError = jest.fn();

    useStateSpy = jest.spyOn(React, 'useState')
    useStateSpy.mockImplementationOnce(init => [init, setError]);
    useStateSpy.mockImplementationOnce(init => [init, setFormData]);

    component = mount(
      <AuthContext.Provider value={context}>
        <Create/>
      </AuthContext.Provider>
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should render the two textareas and one input', () => {
    expect(component.find(FormControl)).toHaveLength(1);
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
    const input = component.find('#howto').at(0);

    input.value = 'Ferva a água';

    input.simulate('change');

    expect(setFormData).toHaveBeenCalled();
  });
});