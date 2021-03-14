

import React from 'react';
import CardList from '../UX/CardList/CardList';
import Button from 'react-bootstrap/Button';
import classes from './Profile.module.css';
import recipesMock from '../../recipesMock.json';
import { useAuth } from '../../context/Auth';

const Profile = () =>{
  const user = useAuth().user;
  console.log(user)
  //console.log(user)

  const [favoriteRecipes, setFavoriteRecipes] = React.useState([]);
  const [userRecipes, setUserRecipes] = React.useState([]);

  React.useEffect(() => {
    
<<<<<<< HEAD
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
=======
    if (user==null){
      return ;
    } 
    const getData = async() => {
      const urls = [`${process.env.REACT_APP_SERVER_URL}/receitas/favoritas`, `${process.env.REACT_APP_SERVER_URL}/receitas/user_all_recipes`];

      

    const options = {
      method: 'GET',
      headers: {
      Authorization: `Bearer ${user.access_token}`
      }
    }
      const responses = await Promise.all(urls.map(url => fetch(url, options)));
      const lists = await Promise.all(responses.map(r => r.json()));
      setFavoriteRecipes(Object.values(lists[0]))
      setUserRecipes(Object.values(lists[1]))
    }
    
    getData();
  }, [user]);

    return (
      <div className={`${classes.Container}`}>
  
        <div >
          <h4 className={classes.header}>Minhas Receitas:</h4>
          <CardList className={`${classes.List}`} list={userRecipes}/>
>>>>>>> 8342c04ce90e3ed9e41b51ea67e0760fe70e7a04
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

