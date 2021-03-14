import React from 'react';
import { useAuth } from '../../../context/Auth';
import classes from './UserRecipes.module.css';
import CardList from '../../UX/CardList/CardList';

const UserRecipes = () => {
  const user = useAuth().user;
  const [recipes, setRecipes] = React.useState([]);

  React.useEffect(() => {
    const getRecipes = async () => {
      const url = `${process.env.REACT_APP_SERVER_URL}/receitas/user_all_recipes`;
      const options ={ 
        headers: {
          Authorization: `Bearer ${user.access_token}`
        }
      }
      const json = await fetch(url, options);
      const response = await json.json();
      setRecipes(Object.values(response));
    }

    if(user) getRecipes();
  }, [user]);


  if(!user) {
    return <p> Você precisa estar logado para acessar essa página. <a href="/login">Faça seu login</a></p>
  }

  return (
    <div className={`${classes.Container}`}>
      <CardList list={recipes} hideAuthor/>
    </div>
  )
}

export default UserRecipes;