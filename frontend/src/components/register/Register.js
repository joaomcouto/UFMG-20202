import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import {Link} from 'react-router-dom';
import classes from './Register.module.css';

const Register = () => {
  const formClasses = [
    classes.Form, 'w-25','p-4' ,'m-auto', 'd-flex', 'flex-column',
    'border', 'border-dark', 'rounded'
  ];
  return (
    <Form className={formClasses.join` `}>
      <Form.Group controlId="email">
        <Form.Label>Nome</Form.Label>
        <Form.Control type="email" placeholder="Seu email" />
      </Form.Group>

      <Form.Group controlId="email">
        <Form.Label>Email</Form.Label>
        <Form.Control type="email" placeholder="Digite seu email" />
      </Form.Group>

      <Form.Group controlId="password">
        <Form.Label>Senha</Form.Label>
        <Form.Control type="password" placeholder="Senha" />
      </Form.Group>

      <Form.Group controlId="confirmPassword">
        <Form.Label>Confirmar senha</Form.Label>
        <Form.Control type="password" placeholder="Confirmar senha" />
      </Form.Group>
      <Button className={'m-auto'} variant="primary" type="submit">
        Cadastrar
      </Button>
      <Form.Text>
        <Link to="/login">
          Já possui uma conta? Faça o login!
        </Link>
      </Form.Text>
    </Form>
  )
}

export default Register;