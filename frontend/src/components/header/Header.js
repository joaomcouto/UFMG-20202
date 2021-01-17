import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import { useAuth } from '../../context/Auth';

const Header = ({ logout }) => {
  const token = useAuth().token;

  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
      <Navbar.Brand href="/">MyRecipes</Navbar.Brand>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/recipes">Receitas</Nav.Link>
        </Nav>
        <Nav>
          {
            token ?
              (
                <>
                <Nav.Link href="/profile">
                  Perfil
                </Nav.Link>
                <Button onClick={() => logout(null)}>Sair</Button>
                </>
              ) :
              (
                <>
                <Nav.Link href="/login">Entrar</Nav.Link>
                <Nav.Link href="/register">Cadastrar</Nav.Link>
                </>
              )
          }
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Header;