

import React from 'react';
import CardList from '../UX/CardList/CardList';
import Button from 'react-bootstrap/Button';
import classes from './Profile.module.css';
import recipesMock from '../../recipesMock.json';

const Profile = () =>{
    const [favoriteRecipes, setFavoriteRecipes] = React.useState([]);
    const [userRecipes, setUserRecipes] = React.useState([]);

    React.useEffect(() => {
      const getData = async() => {
        const urls = [`${process.env.REACT_APP_SERVER_URL}/receitas?limit=5`, `${process.env.REACT_APP_SERVER_URL}/receitas?limit=5`];
        const responses = await Promise.all(urls.map(url => fetch(url)));
        const lists = await Promise.all(responses.map(r => r.json()));
        setFavoriteRecipes(Object.values(lists[0]))
        setUserRecipes(Object.values(lists[1]))
      }
      getData();
    }, []);

      return (
        <div className={`${classes.Container}`}>
    
          <div >
            <h4 className={classes.header}>Minhas Receitas:</h4>
            <CardList className={`${classes.List}`} list={userRecipes}/>
            <div className={['w-100', 'text-right'].join` `}>
              <Button variant="link" href="/profile/recipes">Ver mais...</Button>
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

