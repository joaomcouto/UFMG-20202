import { mount } from 'enzyme';

import React from 'react';
import Home from './Home';

import recipesMock from '../../recipesMock.json';
import CardList from '../UX/CardList/CardList';


describe('<Home />', () => {
  let component, useStateSpy, fetchSpy, setRecipes;
  const data = recipesMock.data;

  beforeEach(() => {
    setRecipes = jest.fn();

    useStateSpy = jest.spyOn(React, 'useState');
    fetchSpy = jest.spyOn(window, 'fetch');
    useStateSpy.mockImplementationOnce(init => [init, setRecipes]);
    fetchSpy.mockImplementationOnce(() => {
      return Promise.resolve({
        status: 200,
        json: () => Promise.resolve({
          data
        })
      })
    })
    component = mount(
      <Home/>
    );
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should render both card list with the recipes', () => {
    expect(component.find(CardList)).toHaveLength(2);
  });
});