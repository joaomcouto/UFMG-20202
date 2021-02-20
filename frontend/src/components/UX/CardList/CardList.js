import Card from "react-bootstrap/Card"
import classes from './CardList.module.css';

const CardList = ({list}) => {
  return (
    <div className='m-auto'>
      {list.map(element => {
        console.log(element);
        return <Card border="dark" bg="#ff8282" className={classes.Card} key={element.ID}>
          <Card.Body>
            <Card.Title> <a className={classes.Link} href={`/recipe/${element.ID}`}> {element.titulo} </a></Card.Title>
            <Card.Text> Por: {element.autor}</Card.Text>
          </Card.Body>
        </Card>
      })}
    </div>
  )
}

export default CardList;