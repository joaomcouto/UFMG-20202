## MyRecipes

## Grupo: 
- João Marcos Machado Couto
- Pedro Nascimento Costa
- Vinícius Brenner 
- Vitor Siman do Amaral Lamartine

## Descrição breve:
O MyRecipes permite cadastro de receitas que podem ser compartilhadas entre usuários, os usuários podem avaliar as receitas e salva-lás como favorito. Além disso, permite que o usuário cadastre suas próprias receitas para que os demais usuários possam visualizá-las. 

## Escopo Funcional:
- Cadastro de Usuário, o usuário pode cadastrar-se.
- Cadastro de receitas, o usuário pode cadastrar novas receitas.
- Edição de receitas já existentes pelo usuário que a cadastrou.
- Adição de receitas aos favoritos.
- Avaliação de receitas cadastradas.
- Visualização de receitas cadastradas.
- Pesquisa avançada de receitas, de acordo com alguns filtros (nome, categoria).

## Escopo Tecnológico:
- backend: python, mySQL
- frontend: javascript, html, css (Framework: React)

### Teremos sprint de colocar em produção

-------------------------------------------------------------------------------------------------------------------------

## Sprint 1

### Histórias de Usuário:

#### Cadastro:
- Alguém que queira utilizar o MyRecipes precisa fazer cadastro no sistema, utilizando um nome de usuário e senha.

#### Login:
- Um usuário do MyRecipes pode fazer login no sistema com seu nome de usuário, email e senha.
- Um usuário do MyRecipes pode fazer logout do sistema após estar conectado.

#### Perfil & Receitas:
- Um usuário do MyRecipes pode adicionar receitas ao seu perfil, cadastrando novas receitas.

#### Responsabilidades:
- Pedro e Vinícius responsáveis pelas tarefas de backend, modelando o domínio do problema, implementando as APIs, refatorando erros de backend e implementando a criação do banco.
- Vitor responsável pelo frontend e implementação das telas com as quais o usuário interage.

#### Testes:
- Pedro:
  - Implementação do baseTest: https://github.com/VLamartine/pds2020-2/blob/d46a927834de3d42b0c33c0b802281212d105612/backend/baseTest.py#L7
  - Implementação de alguns testes backend (até o comentário indicando testes de outra pessoa): https://github.com/VLamartine/pds2020-2/blob/d46a927834de3d42b0c33c0b802281212d105612/backend/tests.py#L11

- Vinicius:
  - Implementação de alguns testes backend (até o fim da classe): https://github.com/VLamartine/pds2020-2/blob/d46a927834de3d42b0c33c0b802281212d105612/backend/tests.py#L135 

- Vitor:
  - Testes de todas as telas no frontend:
    Exemplos:
      Login: https://github.com/VLamartine/pds2020-2/blob/main/frontend/src/components/login/Login.test.js
      Cadastro: https://github.com/VLamartine/pds2020-2/blob/main/frontend/src/components/register/Register.test.js

#### Retrospective
- Pontos positivos:
  - Ótima comunicação do grupo, conseguimos inclusive parear para resolver problemas, refatorar o código e trocar informações para melhorar a implementação.
  - Conseguimos cumprir todas as histórias propostas (acima, sprint 1)
  - Aprendizado sobre algumas ferramentas, flaskSQLAlchemy do python, por exemplo, que devem ajudar bastatante e já ajudaram bastante na implementação.
  - Implementar os testes do back logo no início ajudou bastante na hora de rodar o código, achar problemas, corrigí-los e refatorar.
  
- Pontos Negativos:
  - Tivemos muitos erros que tiveram que ser solucionados, gastando um bom tempo, principalmente quando fomos ligar o back com o front através das APIs.
  - Atrasamos a primeira reunião de acompanhamento com o Professor.

-------------------------------------------------------------------------------------------------------------------------

## Sprint 2

### Histórias de Usuário:

#### Listagem:
- Um usuário do MyRecipes deseja visualizar receitas cadastradas no sistema de MyRecipes
- Um usuário do MyRecipes deseja visualizar receitas cadastradas no sistemas podendo filtrar de acordo com alguns parâmetros (por hora, faz filtragem apenas por titulo da receita)

#### Perfil & Receitas:
- Um usuário do MyRecipes deseja favoritar receitas de seu interesse.
- Um usuário do MyRecipes deseja visualizar suas receitas favoritadas.
- Um usuário do MyRecipes deseja visualizar suas receitas cadastradas.

#### Responsabilidades:
- Pedro, Vinícius e João responsáveis pelas tarefas de backend, modelando o domínio do problema, implementando as APIs, refatorando erros de backend, elaborando novos testes (de integração e unitários) e efetivando alterações do banco: através de novas tabelas e alteração de colunas já existentes

- Vitor e João responsável pelo frontend e implementação das telas com as quais o usuário interage para visualizar receitas cadastradas e favoritas, além de diversas outras modificações necessárias devido a mudanças nos endpoints

#### Testes:
- João: https://github.com/VLamartine/pds2020-2/blob/a1a57c2e09990d6d4ba19e729de35664b097c1ba/backend/tests.py#L423

- Pedro: https://github.com/VLamartine/pds2020-2/blob/a1a57c2e09990d6d4ba19e729de35664b097c1ba/backend/tests.py#L115

- Vinicius: https://github.com/VLamartine/pds2020-2/blob/a1a57c2e09990d6d4ba19e729de35664b097c1ba/backend/tests.py#L376

- Vitor: https://github.com/VLamartine/pds2020-2/blob/main/frontend/src/components/recipes/recipe/Show/Show.test.js

#### Retrospective

- Pontos positivos:
  - Conseguimos cumprir todas as histórias propostas (como listados acima, sprint 2)
  - Ótima comunicação do grupo, conseguimos inclusive parear para resolver problemas, refatorar o código e trocar informações para melhorar a implementação.
  - A implementação de testes de back end logo no começo do sprint permitiu um fluxo mais dinamico e efetivo de escrita de código, teste, correções e refatorações
  - Entrada de novos membros no grupo permitiu uma divisão mais homogenea das tarefas pendentes
  - A migração do sistema de autenticação dos usuários para JWP se provou extremamente positiva
  
- Pontos Negativos: 
  - Problemas no login causaram a necessidade de migrar a infraestrutura de autenticação
  - A proposta de utilizar o Selenium para simulações mais robustas se provou complexo demais para ser executado com apenas metade do tempo do sprint faltando. Estudaremos a possibilidade de dar continuidade a essa iniciativa durante o sprint 3.


-------------------------------------------------------------------------------------------------------------------------

## Sprint 3

### Histórias de Usuário:

#### Listagem:
- Um usuário do MyRecipes deseja visualizar se uma receita está entre suas favoritas, caso ele carregue ela individualmente
- Um usuário do MyRecipes deseja conseguir editar receitas dele.
- Um usuário do MyRecipes deseja conseguir deletar suas receitas.

### Perfil
 - Um usuário do MyRecipes deseja avaliar receitas, utilizando um sistema de nota (1 a 5)

#### Responsabilidades:
- Pedro, Vinícius e João responsáveis pelas tarefas de backend, modelando o domínio do problema, implementando as APIs, refatorando erros de backend, elaborando novos testes (de integração e unitários) e efetivando alterações do banco: através de novas tabelas e alteração de colunas já existentes

- Vitor responsável pelo frontend e implementação das telas com as quais o usuário interage para visualizar receitas cadastradas e favoritas, além de diversas outras modificações necessárias devido a mudanças nos endpoints

- Joao responsável pela utilização do framework Selenium para implementar testes completos de todo o frontend, passando

#### Testes:
- João: https://github.com/VLamartine/pds2020-2/blob/77f9d7fe143ab72bec818a6aebe8cd09dc74673a/seleniumTesting/main.py#L27

- Pedro: https://github.com/VLamartine/pds2020-2/blob/beb956668f351a20660489ddde9cc73c2fa0fdd5/backend/tests.py#L325

- Vinicius: 

- Vitor:
#### Retrospective

- Pontos positivos:
  - Amplo sucesso na implementação do Selenium
  - Conseguimos cumprir todas as histórias propostas (como listados acima, sprint 3)
  - Ótima comunicação do grupo, conseguimos inclusive parear para resolver problemas, refatorar o código e trocar informações para melhorar a implementação.
  - Como de costume, utilizar testes de back end logo no começo do sprint permitiu um fluxo mais dinamico e efetivo de escrita de código, teste, correções e refatorações
  
- Pontos Negativos: 
  - Sprint foi mais corrida devido ao final do semestre, com o fim de semestre acontecendo, então no geral o grupo sentiu um aperto maior.
  - Selenium demandou um tempo de desenvolvimento maior do que o esperavamos inicialmente, como consequência o frontend ficou com um membro a menos.

### Kanban: https://github.com/VLamartine/pds2020-2/projects/1

### pds2020-2
