import React from 'react';
import { useLocation } from 'react-router-dom';

import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import { useAuth } from '../../../../context/Auth';
import classes from './Create.module.css';

const Create = props => {
  const user = useAuth().user;
  const location = useLocation();
  
  
  console.log(location);

  const [formData, setFormData] = React.useState({
    title: '',
    ingredients: '',
    howTo: ''
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
      title: e.target.value
    })
  }

  const setHowTo = (e) => {
    setFormData({
      ...formData,
      howTo: e.target.value
    });
  }

  const handleSubmit = () => {

  };

  if(!user){
    return <p> Você não pode adicionar uma receita sem fazer login. <a href="/login">Faça seu login</a></p>
  }

  return (
    <div className={[classes.flexgrow, 'd-flex'].join` `}>
      <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center'].join` `} style={{background:'yellow'}}>
        <div className={['w-100']}>
          <h4> Título </h4>
          <InputGroup size="sm" className={[classes.w80, classes.mAuto].join` `}>
            <FormControl aria-label="Small" aria-describedby="inputGroup-sizing-sm" />
          </InputGroup>
        </div>
        <div>
          <h4>Ingredientes </h4>
          <p> Separe um passo por linha</p>
          <textarea cols="80" rows="10" onChange={setHowTo}/>
        </div>
      </div>
      <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center', 'justify-content-around'].join` `} style={{background:'blue'}}>
        <h4> Modo de preparo:</h4>
        <p> Separe um passo por linha</p>
        <textarea cols="80" rows="15" onChange={setHowTo}/>
        <Button onClick={handleSubmit}> Salvar </Button>
      </div>
    </div>
  )
}

export default Create;