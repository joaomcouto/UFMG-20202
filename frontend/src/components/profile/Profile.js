

import React from 'react';
import CardList from '../UX/CardList/CardList';
import Button from 'react-bootstrap/Button';
import classes from './Profile.module.css';
import recipesMock from '../../recipesMock.json';

const Profile = () =>{
    const [favoriteRecipes, setFavoriteRecipes] = React.useState([]);
    const [userRecipes, setUserRecipes] = React.useState([]);

    React.useEffect(() => {
        if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
          // Fetch API
        } else {
          setUserRecipes(recipesMock.data.recipes.slice(0, 5))
          setFavoriteRecipes(recipesMock.data.recipes.slice(0, 5))
        }
      }, []);

      return (
        <div className={`${classes.Container}`}>
    
          <div >
            <h4 className={classes.header}>Minhas Receitas:</h4>
            <CardList className={`${classes.List}`} list={userRecipes}/>
            <div className={['w-100', 'text-right'].join` `}>
              <Button variant="link" href="/recipes">Ver mais...</Button>
            </div>
          </div>
          
          <div>
          <h4 className={classes.header}>Receitas favoritas:</h4>
          <CardList list={favoriteRecipes}/>
          <div className={['w-100', 'text-right'].join` `}>
            <Button variant="link" href="/recipes">Ver mais...</Button>
          </div>
          </div>
        </div>
      )
} 

export default Profile; 

