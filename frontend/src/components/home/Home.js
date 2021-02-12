import React from 'react';
import recipesMock from '../../recipesMock.json';
import CardList from '../UX/CardList/CardList';
import classes from './Home.module.css';
import Button from 'react-bootstrap/Button';

const Home = () => {
  const [recipes, setRecipes] = React.useState([]);

  React.useEffect(() => {
    if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
      // Fetch API
    } else {
      setRecipes(recipesMock.data.recipes.slice(0, 5))
    }
  }, []);

  return (
    <div className={`${classes.Container}`}>
      <div className={classes.last_recipes}>
      <h4 className={classes.header}>Últimas receitas:</h4>
      <CardList className={`${classes.List}`} list={recipes}/>
      <div className={['w-100', 'text-right'].join` `}>
        <Button variant="link" href="/recipes">Ver mais...</Button>
      </div>
      </div>
      <div>
      <h4 className={classes.header}>Receitas populares:</h4>
      <CardList list={recipes}/>
      <div className={['w-100', 'text-right'].join` `}>
        <Button variant="link" href="/recipes">Ver mais...</Button>
      </div>
      </div>
    </div>
  )
}

export default Home;