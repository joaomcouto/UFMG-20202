import React from 'react';
import recipesMock from '../../../recipesMock.json';
import CardList from '../../UX/CardList/CardList';
import classes from './List.module.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';

const List = () => {
  const [recipes, setRecipes] = React.useState([]);

  React.useEffect(() => {
    if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
      // Fetch API
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
      // Fetch API
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
          <FormControl aria-label="Procurar" onChange={handleFilterChange} aria-describedby="inputGroup-sizing-sm" />
        </InputGroup>
      </div>
      <CardList list={recipes}/>
    </div>
  )
}

export default List;