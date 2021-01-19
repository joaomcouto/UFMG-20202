import React from 'react';
// import { useParams } from 'react-router-dom';

import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import { useAuth } from '../../../../context/Auth';
import classes from './Create.module.css';
import { post } from '../../../../util/fetch';

const Create = props => {
  const user = useAuth().user;

  const [error, setError] = React.useState(false);
  const [formData, setFormData] = React.useState({
    title: '',
    ingredients: '',
    howTo: ''
  });

  React.useEffect(() => {
    // Buscar receita no back se tiver um Id
  });
  const setTitle = (e) => {
    setFormData({
      ...formData,
      title: e.target.value
    })
  }

  const setIngredients = (e) => {
    setFormData({
      ...formData,
      ingredients: e.target.value
    })
  }

  const setHowTo = (e) => {
    setFormData({
      ...formData,
      howTo: e.target.value
    });
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      user_id: user.UserID,
      title: formData.title,
      text: JSON.stringify({
        ingredients: formData.ingredients,
        howTo: formData.howTo
      })
    };

    const response = await post('/new_recipe', {body: JSON.stringify(data)});
    if(response.status === 200){
      // Redirecionar para a tela da receita
    } else {
      setError(true);
    }
  };

  if(!user){
    return <p> Você não pode adicionar uma receita sem fazer login. <a href="/login">Faça seu login</a></p>
  }

  return (
    <div className={[classes.flexgrow, 'd-flex', classes.background].join` `}>
      <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center', classes.contentEvenly].join` `}>
        <div className={['w-100', 'text-center'].join` `}>
          <h4> Título </h4>
          <InputGroup size="sm" className={[classes.w80, classes.mAuto].join` `}>
            <FormControl id="title" onChange={setTitle} aria-label="Small" aria-describedby="inputGroup-sizing-sm" />
          </InputGroup>
        </div>
        <div className={['w-100', 'text-center'].join` `}>
          <h4>Ingredientes </h4>
          <p> Separe um ingrediente por linha</p>
          <textarea id="ingredients" cols="80" rows="10" onChange={setIngredients}/>
        </div>
      </div>
      <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center', 'justify-content-around'].join` `}>
        <div className={['w-100', 'text-center'].join` `}>
          <h4> Modo de preparo:</h4>
          <p> Separe um passo por linha</p>
        </div>
        <textarea id="howto" cols="80" rows="15" onChange={setHowTo}/>
        <Button onClick={handleSubmit}> Salvar </Button>
        {error ? <span> Não foi possível salvar a receita </span> : ''}
      </div>
    </div>
  )
}

export default Create;