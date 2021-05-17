import React from 'react';
import CardList from '../../UX/CardList/CardList';
import classes from './List.module.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import { FaQuestionCircle } from 'react-icons/fa';
import ReactModal from 'react-modal';

const List = () => {
  const [recipes, setRecipes] = React.useState([]);
  const [isHelpModalOpen, setIsHelpModalOpen] = React.useState(false);

  const getRecipes = async (params = '') => {
    const url = `${process.env.REACT_APP_SERVER_URL}/receitas?${params || ''}`;
    const response = await fetch(url);
    const data = await response.json();
    setRecipes(Object.values(data));
  }

  React.useEffect(() => {
    getRecipes();
  }, []);

  const handleFilterChange = (e) => {
    const terms = e.target.value.split(',');

    const params = {
      titulo: "",
      autor: "",
      estrelas: ""
    }

    terms.forEach(term => {
      const param = term.split(':');

      if(param.length === 1){
        params.titulo = param[0];
      } else {
        params[param[0]] = param[1];
      }
    })
    
    let queryString = '';

    for(let param in params){
      if(!params[param]) continue;

      queryString += `${param}=${encodeURIComponent(params[param])}&`;
    }
    
    getRecipes(queryString);
  }

  const toggleModal = (state) => {
    setIsHelpModalOpen(state);
  }

  return (
    <div className={`${classes.Container}`}>
      <ReactModal onRequestClose={() => toggleModal(false)} isOpen={isHelpModalOpen}>
        <p>Você pode filtrar as receitas de três maneiras diferentes</p>
        <ol>
          <li>
            Pelo título da receita: 
            <p className={[classes.exemplo].join` `}>
              <i>titulo:Brigadeiro</i>
            </p>
            <p> ou apenas</p>
            <p className={[classes.exemplo].join` `}>
              <i>Brigadeiro</i>
            </p>
          </li>
          <li>
            Pelo autor da receita: 
            <p className={[classes.exemplo].join` `}>
              <i>autor:andre</i>
            </p>
          </li>
          <li>
            Pela quantidade de estrlas (n estrelas ou mais): 
            <p className={[classes.exemplo].join` `}>
              <i>estrelas:5</i>
            </p>
          </li>
        </ol>
        <p>Também é possível combinar os filtros, separando-os por vírgulas(,)</p>
        <p className={[classes.exemplo].join` `}>
          <i>brigadeiro;autor:andre</i>
        </p>
      </ReactModal>
      <div className={[classes.search_bar].join` `}>
        <InputGroup size="sm" >
          <InputGroup.Prepend>
            <InputGroup.Text id="inputGroup-sizing-sm">Filtrar</InputGroup.Text>
          </InputGroup.Prepend>
          <FormControl aria-label="Procurar" id="filter" onChange={handleFilterChange} aria-describedby="inputGroup-sizing-sm" />
          <InputGroup.Append>
            <button onClick={() => toggleModal(true)} className={[classes.help_button].join` `}>
              <FaQuestionCircle></FaQuestionCircle>
            </button>
          </InputGroup.Append>
        </InputGroup>
      </div>
      <CardList list={recipes}/>
    </div>
  )
}

export default List;