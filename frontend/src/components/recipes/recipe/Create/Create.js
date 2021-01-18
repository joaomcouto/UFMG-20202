import React from 'react';
import { useLocation } from 'react-router-dom';
//import { Redirect } from 'react-router-dom';
//import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useAuth } from '../../../../context/Auth';
import classes from './Create.module.css';

const Create = props => {
  const user = useAuth().user;
  
  const location = useLocation();
  
  
  console.log(location);
/*
const formData = React.useState({
    ingredients: '',
    howTo: ''
  });
*/
  
  
  const handleSubmit = () => {

  };
  
  if(!user){
    return <p> Você não pode adicionar uma receita sem fazer login. <a href="/login">Faça seu login</a></p>
  }

  return (
    <div className={[classes.flexgrow, 'd-flex'].join` `}>
      <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center'].join` `} style={{background:'yellow'}}>Ingredientes</div>
      <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center'].join` `} style={{background:'blue'}}>
        <p> Modo de preparo: </p>
        <textarea cols="80" rows="15" />
        <Button onClick={handleSubmit}> Salvar </Button>
      </div>
    </div>
  )
}

export default Create;