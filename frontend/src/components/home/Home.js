import React from 'react';
import recipesMock from '../../recipesMock.json';
import CardList from '../UX/CardList/CardList';
import classes from './Home.module.css';

const Home = () => {
  const [recipes, setRecipes] = React.useState([]);

  React.useEffect(() => {
    if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
      // Fetch API
    } else {
      setRecipes(recipesMock.data.recipes)
    }
  }, []);

  return (
    <div className={`${classes.Container}`}>
      <div>
      <h4>Últimas receitas:</h4>
      <CardList className={`${classes.List}`} list={recipes}/>
      </div>
      <div>
      <h4>Receitas populares:</h4>
      <CardList list={recipes}/>
      </div>
    </div>
  )
}

export default Home;