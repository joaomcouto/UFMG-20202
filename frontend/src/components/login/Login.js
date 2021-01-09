import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import classes from './Login.module.css';
import { Link } from 'react-router-dom';

const Login = () => {
  const formClasses = [
    classes.Form,
    'w-25','p-4' ,'m-auto', 'd-flex', 'flex-column',
    'border', 'border-dark', 'rounded'
  ];

  return (
    <Form className={formClasses.join` `}>
      <Form.Group controlId="email">
        <Form.Label>Email</Form.Label>
        <Form.Control type="email" placeholder="Digite seu email" />
      </Form.Group>

      <Form.Group controlId="password">
        <Form.Label>Senha</Form.Label>
        <Form.Control type="password" placeholder="Senha" />
      </Form.Group>
      <Button className={'m-auto'} variant="primary" type="submit">
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