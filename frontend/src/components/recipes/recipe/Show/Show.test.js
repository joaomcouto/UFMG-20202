import { mount, shallow } from 'enzyme';

import React from 'react';
import ReactRouter from 'react-router'
import Show from './Show';
import classes from './Show.module.css';

import recipesMock from '../../../../recipesMock.json';


describe('<Show />', () => {
  let component;
  let useStateSpy, fetchSpy, useEffectSpy, useParamsSpy;
  let setRecipe;

  const data = recipesMock.data;

  beforeEach(() => {
    setRecipe = jest.fn();
    window.alert = () => {}
    useStateSpy = jest.spyOn(React, 'useState');
    useParamsSpy = jest.spyOn(ReactRouter, 'useParams');
    fetchSpy = jest.spyOn(global, 'fetch');
    useEffectSpy = jest.spyOn(React, 'useEffect');

    useEffectSpy.mockImplementationOnce(f => f());

    useStateSpy.mockImplementationOnce(init => [init, setRecipe]);
    fetchSpy.mockImplementationOnce(() => {
      return Promise.resolve({
        status: 200,
        json: () => Promise.resolve({
          ...data.recipes[0]
        })
      })
    })

    useParamsSpy.mockReturnValue({id: 1})


    component = shallow(
      <Show/>
    );
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should set the recipe', () => {
    expect(setRecipe).toHaveBeenCalledWith(data.recipes[0]);
  });

  it('should render the title element', () => {
    const element = component.find(`.${classes.recipe_name}`);
    
    expect(element.exists()).toBeTruthy();
  });
  it('should render the cooktime element', () => {
    const element = component.find(`.${classes.time}`);
    
    expect(element.exists()).toBeTruthy();
  });
  it('should render the servings element', () => {
    const element = component.find(`.${classes.servings}`);
    
    expect(element.exists()).toBeTruthy();
  });
  it('should render the ingredients element', () => {
    const element = component.find(`.${classes.ingredients}`);
    
    expect(element.exists()).toBeTruthy();
  });

  it('should render the cooking steps element', () => {
    const element = component.find(`.${classes.howTo}`);
    
    expect(element.exists()).toBeTruthy();
  });

  it('should handle a recipe being marked as favourite', () => {
    const element = component.find(`#favouriteButton`).at(0);

    element.simulate('click');

    expect(setRecipe).toHaveBeenCalled()
  });
});