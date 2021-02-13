import React from 'react';
import ReactRouter from 'react-router';
import classes from './Show.module.css';
import recipeIcon from '../../../../assets/dinner.svg';
import Image from 'react-bootstrap/Image';
import { FaRegClock, FaRegHeart, FaHeart } from 'react-icons/fa';

import mockImage from '../../../../assets/brigadeiro.jpg';
import recipesMock from '../../../../recipesMock.json';

const Show = () => {
  const [recipe, setRecipe] = React.useState({
    ingredientes: '',
    howTo: '',
    favourite: false
  });
  const { id } = ReactRouter.useParams();

  React.useEffect(() => {
    const getRecipe = async () => {
      const url = `${process.env.REACT_APP_SERVER_URL}/receita/${id}`
      const response = await fetch(url);
      const data = (await response.json()).data;
      setRecipe(data);
    }

    // if(process.env.REACT_APP_IS_SERVER_WORKING === 'false'){
      getRecipe();
    // } else {
    //   console.log(recipesMock.data.recipes[0]);
    //   const recipe = recipesMock.data.recipes[0];
    //   recipe.imagem = recipe.imagem ? mockImage : null;
    //   setRecipe(recipesMock.data.recipes[0]);
    // }
  }, [id]);


  return (
    <div className={[classes.container].join` `}>
      <div className={[classes.lg_header_container]}>
        <div className = {[classes.title].join` `}>
          <h3 className={[classes.recipe_name]}> {recipe.titulo}</h3>
          {
            recipe.favourite ? 
            <FaHeart className={[classes.favourite_icon]}/>
            : <FaRegHeart className={[classes.favourite_icon]}/> 
          }
        </div>
        <hr className={[classes.hr].join` `}/>
        <div className={[classes.recipe_header].join` `}>
          <div className={classes.image_div}>
            <Image className={[classes.image].join` `} src={recipe.imagem || recipeIcon} fluid />
          </div>
        </div>
      </div>
      <div className={[classes.info].join` `}>
        <div className={[classes.time].join` `}>
          < FaRegClock className={[classes.clock_icon]}/> {recipe.tempo} minutos
        </div>
        <div className={[classes.servings].join` `}>
          {recipe.porcoes} porções
        </div>
      </div>
      <div className={[classes.ingredients].join` `}>
        <h5>INGREDIENTES</h5>
        <ul>
          {
            recipe ? recipe.ingredientes.split('\n').map((ingredient, i) => {
              return <li key={i}>{ingredient}</li>
            }) : ''
          }
        </ul>
      </div>
      <div className={[classes.howTo].join` `}>
        <h5>MODO DE PREPARO</h5> 
        <ol>
          {
            recipe ? recipe.howTo.split('\n').map((step, i) => {
              return <li key={i}>{step}</li>
            }) : ''
          }
        </ol>
      </div>
    </div>
  )
}

export default Show;