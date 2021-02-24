import Card from "react-bootstrap/Card"
import classes from './CardList.module.css';
import recipeIcon from '../../../assets/dinner.svg';

const CardList = ({list}) => {
  return (
    <div className={['m-auto', classes.w_100].join` `}>
      {list.map(element => {
        return <Card border="dark" bg="#ff8282" className={classes.Card} key={element.ID}>
          <Card.Body className={['d-flex'].join` `}>
            <img className={[classes.image].join` `} alt="" src={element.imagem || recipeIcon}></img>
            <div className={[classes.card_body].join` `}>
              <Card.Title> <a className={classes.Link} href={`/recipe/${element.ID}`}> {element.titulo} </a></Card.Title>
              <Card.Text> Por: {element.nome}</Card.Text>
            </div>
          </Card.Body>
        </Card>
      })}
    </div>
  )
}

export default CardList;