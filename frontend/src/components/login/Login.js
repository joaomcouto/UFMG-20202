import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import classes from './Login.module.css';
import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';

const Login = () => {
  const [isFormValid, setIsFormValid] = useState(false);
  const [formData, setFormData] = useState({
    email: {
      value: '',
      valid: false,
      touched: false
    },
    password: {
      value: '',
      valid: false,
      touched: false
    }
  })

  useEffect(() => {
    for(let field in formData){
      if(!formData[field].valid){
        setIsFormValid(false);
        return;
      }
    }
    setIsFormValid(true);
  }, [formData]);

  const handleChange = (e) => {
    const value = e.target.value;
    let valid;
    switch (e.target.id) {
      case 'email':
        const pattern = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
        valid = pattern.test(value);
        break;
      case 'password':
        valid = value.length >= 8;
        break;
      default:
        break;
    }

    setFormData({
      ...formData,
      [e.target.id]: {
        valid: valid,
        value: value,
        touched: true
      }
    });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
  }

  const formClasses = [
    classes.Form,
    'w-25','p-4' ,'m-auto', 'd-flex', 'flex-column',
    'border', 'border-dark', 'rounded'
  ];

  return (
    <Form className={formClasses.join` `} onSubmit={handleSubmit}>
      <Form.Group controlId="email">
        <Form.Label>Email</Form.Label>
        <Form.Control onChange={handleChange} isInvalid={!formData.email.valid && formData.email.touched} type="email" placeholder="Digite seu email" />
        <Form.Control.Feedback type="invalid">Digite um email válido</Form.Control.Feedback>
      </Form.Group>

      <Form.Group controlId="password">
        <Form.Label>Senha</Form.Label>
        <Form.Control onChange={handleChange} isInvalid={!formData.password.valid && formData.password.touched} type="password" placeholder="Senha" />
      
      </Form.Group>
      <Button disabled={!isFormValid} className={'m-auto'} variant="primary" type="submit">
        Entrar
      </Button>

      <Form.Text>
        <Link to="/register">
          Não possui uma conta? Cadastre-se agora!
        </Link>
      </Form.Text>
    </Form>
  );
}

export default Login;