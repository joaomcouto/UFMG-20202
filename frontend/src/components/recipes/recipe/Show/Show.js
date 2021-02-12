import React from 'react';
import { useParams } from 'react-router-dom';
import classes from './Show.module.css';
import recipeIcon from '../../../../assets/dinner.svg';
import Image from 'react-bootstrap/Image';
import { FaRegClock } from 'react-icons/fa';

import mockImage from '../../../../assets/brigadeiro.jpg';
import recipesMock from '../../../../recipesMock.json';

const Show = () => {
  const [recipe, setRecipe] = React.useState({});
  const { id } = useParams();

  
  React.useEffect(() => {
    const getRecipe = async () => {
      const url = `${process.env.REACT_APP_SERVER_URL}/receita/${id}`
      const response = await fetch(url);
      setRecipe(await response.json());
    }

    if(process.env.REACT_APP_IS_SERVER_WORKING !== 'false'){
      getRecipe();
    } else {
      console.log(recipesMock.data.recipes[0]);
      const recipe = recipesMock.data.recipes[0];
      recipe.imagem = recipe.imagem ? mockImage : null;
      setRecipe(recipesMock.data.recipes[0])
    }
  }, [id]);


  return (
    <div className={[classes.container].join` `}>
      <div className={[classes.recipe_header].join` `}>
        <h3> {recipe.titulo}</h3>
        <div>
          <Image className={[classes.image].join` `} src={recipe.imagem || recipeIcon} fluid />
        </div>
      </div>
      <div className={[classes.info].join` `}>
        <div className={[classes.time]}>
          < FaRegClock /> {recipe.tempo}
        </div>
        <div className={[classes.servings]}>
          {recipe.porcoes} porção(ões)
        </div>
      </div>
      <div className={[classes.ingredients].join` `}>
        <ul>
          {
            recipe.ingredientes.split('\n').map((ingredient, i) => {
              return <li key={i}>{ingredient}</li>
            })
          }
        </ul>
      </div>
      <div className={[classes.howTo].join` `}>
        <ol>
          {
            recipe.howTo.split('\n').map((step, i) => {
              return <li key={i}>{step}</li>
            })
          }
        </ol>
      </div>
    </div>
  )
}

export default Show;