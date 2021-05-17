import React from 'react';
import { useParams } from 'react-router-dom';

import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';
import { useAuth } from '../../../../context/Auth';
import classes from './Create.module.css';
import { Redirect } from 'react-router-dom';
const Create = () => {
  const user = useAuth().user;

  const [error, setError] = React.useState(false);
  const [recipeId, setRecipeId] = React.useState(null);
  const [formData, setFormData] = React.useState({
    title: '',
    time: 0,
    servings: 0,
    ingredients: '',
    howTo: '',
    image: '',
  });
  const [imageUrl, setImageUrl] = React.useState('');
  const [formSent, setFormSent] = React.useState(false);
  const [editForm, setEditForm] = React.useState(false);

  const { id } = useParams();

  React.useEffect(() => {
    // Buscar receita no back se tiver um Id
    if(id){
      const url = `${process.env.REACT_APP_SERVER_URL}/receitas/${id}`;
      setEditForm(true);
      fetch(url).then(data => data.json()).then(response => {
        console.log('After fetching');
        setFormData({
          title: response.titulo,
          time: response.tempo_preparo,
          servings: response.texto,
          ingredients: response.ingredientes,
          howTo: response.modo_preparo,
        });
      });
    }    
  }, [id]);

  const handleImageChange = (e) => {
    setFormData({
      ...formData,
      image: e.target.files[0]
    });

    let reader = new FileReader();

    reader.onloadend = () => {
      setImageUrl(reader.result);
    }

    reader.readAsDataURL(e.target.files[0]);
  }

  const handleFormDataChange = (e) => {
    const data = {...formData};
    data[e.target.id] = e.target.value;
    setFormData(data)
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();

    for(let prop in formData) {
      if(prop !== 'image' && !formData[prop]){
        setError(true);
        return
      }
    }
    
    if(editForm){
      data.append('id', id);
    }

    data.append('title', formData.title);
    data.append('ingredients', formData.ingredients);
    data.append('directions', formData.howTo);
    data.append('time', formData.time);
    data.append('text', formData.servings);
    data.append('userId', user.UserID);
    // data.append('image', formData.image);

    const url = `${process.env.REACT_APP_SERVER_URL}/${editForm ? 'edit' : 'new'}_recipe`
    const options = {
      method: 'POST',
      body: data,
      headers: {
        Authorization: `Bearer ${user.access_token}`
      }
    }
    try{
      const json = await fetch(url, options);
      const response = await json.json();

      if(json.status !== 201 && !editForm){
        setError(true);
        return;
      }
      setRecipeId(response.id);
      setFormSent(true);
    } catch(e){
      setError(true);
      return;
    }
  };

  if(!user){
    return <p> Você não pode adicionar uma receita sem fazer login. <a href="/login">Faça seu login</a></p>
  }

  if(formSent){
    return (<Redirect to={`/recipe/${recipeId || id}`}/>);
  }
  return (
    <div className={[classes.container, 'd-flex', 'flex-column', 'align-items-center'].join` `}>
      <div className={[classes.form, 'd-flex', 'flex-column', 'align-items-center'].join` `}>
        <div className={['w-100', 'text-center', 'mb-4'].join` `}>
          <InputGroup size="sm" className={[classes.title].join` `}>
            <FormControl value={formData.title} className={[classes.name].join` `} placeholder="Nome da receita" id="title" onChange={handleFormDataChange} aria-label="Small" aria-describedby="inputGroup-sizing-sm" required/>
          </InputGroup>
        </div>

        <div className={[classes.recipe_info].join` `}>
          <InputGroup className={['m-auto, text-center'].join` `}>
            <h5 className={[classes.info_title]}> Tempo de preparo</h5>
            <FormControl value={formData.time} id="time" type="number" onChange={handleFormDataChange} />
            <InputGroup.Append>
              <InputGroup.Text>min</InputGroup.Text>
            </InputGroup.Append>
          </InputGroup>

          <InputGroup className={['text-center', classes.portion].join` `}>
            <h5 className={[classes.info_title]}> Porções</h5>
            <FormControl value={formData.servings} onChange={handleFormDataChange} id="servings" type="number" />
          </InputGroup>
        </div>

        <div className={[classes.recipe_info].join` `}>
          <InputGroup className={['text-center', classes.portion].join` `}>
            {
              imageUrl ?
              (<Image className={[classes.image].join` `} src={imageUrl} fluid />)
              :
              (<div className="image-container" ><span>Selecione uma imagem para a sua receita (opcional)</span></div>)
            }
            <label className={[classes.image_submit]}>
              <input className={[classes.image_submit_input].join` `} type="file" onChange={handleImageChange}/>
              Enviar foto
            </label>
          </InputGroup>
        </div>
        <div className={[classes.recipe_info, 'text-center'].join` `}>
          <h4>Ingredientes </h4>
          <p> Separe um ingrediente por linha</p>
          <textarea value={formData.ingredients} id="ingredients" required className={[classes.textarea].join` `} onChange={handleFormDataChange}/>
        </div>
        <div className={[classes.recipe_info, 'text-center'].join` `}>
          <h4> Modo de preparo</h4>
          <p> Separe um passo por linha</p>
          <textarea value={formData.howTo} id="howTo" required className={[classes.textarea].join` `} onChange={handleFormDataChange}/>
        </div>

        <Button variant="dark" id="submit" className={['m-auto', classes.submit].join` `} onClick={handleSubmit}> Salvar </Button>
        <div className={[classes.flexgrow, 'd-flex', 'flex-column', 'align-items-center', 'justify-content-around'].join` `}>
          {error ? <span className={classes.error_message}> Não foi possível salvar a receita. Confira se todos os dados foram preenchidos </span> : ''}
        </div> 
      </div>
    </div>
  )
}

export default Create;