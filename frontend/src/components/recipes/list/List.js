import React from 'react';
import recipesMock from '../../../recipesMock.json';
import CardList from '../../UX/CardList/CardList';
import classes from './List.module.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';

const List = () => {
  const [recipes, setRecipes] = React.useState([]);

  const getRecipes = async (params = "") => {
    const url = `${process.env.REACT_APP_SERVER_URL}/recipes`;
    const response = await fetch(url);
    const data = await response.json();

    setRecipes(data.recipes);
  }

  React.useEffect(() => {
    if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
      getRecipes();
    } else {
      setRecipes(recipesMock.data.recipes)
    }
  }, []);

  const handleFilterChange = (e) => {
    const searchParam = e.target.value;

    if(!searchParam) {
      setRecipes(recipesMock.data.recipes);
    }

    if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
      getRecipes(`search:${searchParam}`);
    } else {
      setRecipes(recipesMock.data.recipes.filter(recipe => recipe.titulo.includes(e.target.value)))
    }
  }


  return (
    <div className={`${classes.Container}`}>
      <div className={[classes.search_bar].join` `}>
        <InputGroup size="sm" >
          <InputGroup.Prepend>
            <InputGroup.Text id="inputGroup-sizing-sm">Filtrar</InputGroup.Text>
          </InputGroup.Prepend>
          <FormControl aria-label="Procurar" id="filter" onChange={handleFilterChange} aria-describedby="inputGroup-sizing-sm" />
        </InputGroup>
      </div>
      <CardList list={recipes}/>
    </div>
  )
}

export default List;