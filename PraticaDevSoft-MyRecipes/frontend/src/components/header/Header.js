import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
import { useAuth } from '../../context/Auth';

const Header = ({ logout }) => {
  const user = useAuth().user;

  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
      <Navbar.Brand href="/">MyRecipes</Navbar.Brand>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto">
          <NavDropdown title="Receitas" id="recipes-dropdown">
            <NavDropdown.Item href="/recipes">Ver todas</NavDropdown.Item>
            { user ? <NavDropdown.Item href="/recipes/new">Adicionar nova</NavDropdown.Item> : ''} 
          </NavDropdown>
        </Nav>
        <Nav>
          {
            user ?
              (
                <>
                <Button variant="dark" href="/profile">
                  {user.nome}
                </Button>
                <Button id="logout" variant="dark" onClick={() => logout(null)}>Sair</Button>
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