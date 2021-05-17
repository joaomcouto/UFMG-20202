import React from 'react';
import CardList from '../UX/CardList/CardList';
import classes from './Home.module.css';
import Button from 'react-bootstrap/Button';

const Home = () => {
  const [lastRecipes, setLastRecipes] = React.useState([]);
  const [bestRecipes, setBestRecipes] = React.useState([]);

  React.useEffect(() => {
    const getData = async() => {
      const urls = [`${process.env.REACT_APP_SERVER_URL}/receitas?limit=5`, `${process.env.REACT_APP_SERVER_URL}/receitas?limit=5`];
      const responses = await Promise.all(urls.map(url => fetch(url)));
      const lists = await Promise.all(responses.map(r => r.json()));
      setLastRecipes(Object.values(lists[0]))
      setBestRecipes(Object.values(lists[1]))
    }
    //Todo: pegar por nota média
    getData();
  }, []);

  return (
    <div className={`${classes.Container}`}>

      <div className={[classes.list_container].join` `}>
        <h4 className={classes.header}>Últimas receitas:</h4>
        <CardList list={lastRecipes}/>
        <div className={['w-100', 'text-right'].join` `}>
          <Button variant="link" href="/recipes">Ver mais...</Button>
        </div>
      </div>
      
      <div className={[classes.list_container].join` `}>
        <h4 className={classes.header}>Receitas populares:</h4>
        <CardList list={bestRecipes}/>
        <div className={['w-100', 'text-right'].join` `}>
          <Button variant="link" href="/recipes">Ver mais...</Button>
        </div>
      </div>
    </div>
  )
}

export default Home;