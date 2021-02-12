import React from 'react';
// import { useParams } from 'react-router-dom';

import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';
import { useAuth } from '../../../../context/Auth';
import classes from './Create.module.css';

const Create = () => {
  const user = useAuth().user;

  const [error, setError] = React.useState(false);
  const [formData, setFormData] = React.useState({
    title: '',
    time: 0,
    portions: 0,
    ingredients: '',
    howTo: '',
    image: '',
  });
  const [imageUrl, setImageUrl] = React.useState('');

  React.useEffect(() => {
    // Buscar receita no back se tiver um Id
  });

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
    console.log("Handle submit");
    for(let prop in formData) {
      if(prop !== 'image' && !formData[prop]){
        setError(true);
        return
      }

      data.append(prop, formData[prop]);

    }

    const url = `${process.env.REACT_APP_SERVER_URL}/new_recipe`
    const options = {
      method: 'POST',
      body: formData
    }
    try{
      const json = await fetch(url, options);
      /*const response = */await json.json();
      console.log(json.status);
      if(json.status !== 200){
        setError(true);
        return;
      }
      console.log("Estamos aqui");
      window.alert("Receita salva com sucesso");
      /*
        TODO: Redirecionar o usuário para a nova receita
      */ 
    } catch(e){
      setError(true);
      return;
    }
  };

  if(!user){
    return <p> Você não pode adicionar uma receita sem fazer login. <a href="/login">Faça seu login</a></p>
  }

  return (
    <div className={[classes.container, 'd-flex', 'flex-column', 'align-items-center'].join` `}>
      <div className={[classes.form, 'd-flex', 'flex-column', 'align-items-center'].join` `}>
        <div className={['w-100', 'text-center', 'mb-4'].join` `}>
          <InputGroup size="sm" className={[classes.title].join` `}>
            <FormControl className={[classes.name].join` `} placeholder="Nome da receita" id="title" onChange={handleFormDataChange} aria-label="Small" aria-describedby="inputGroup-sizing-sm" required/>
          </InputGroup>
        </div>

        <div className={[classes.recipe_info].join` `}>
          <InputGroup className={['m-auto, text-center'].join` `}>
            <h5 className={[classes.info_title]}> Tempo de preparo</h5>
            <FormControl id="time" type="number" onChange={handleFormDataChange} />
            <InputGroup.Append>
              <InputGroup.Text>min</InputGroup.Text>
            </InputGroup.Append>
          </InputGroup>

          <InputGroup className={['text-center', classes.portion].join` `}>
            <h5 className={[classes.info_title]}> Porções</h5>
            <FormControl onChange={handleFormDataChange} id="portions" type="number" />
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
          <textarea id="ingredients" required className={[classes.textarea].join` `} onChange={handleFormDataChange}/>
        </div>
        <div className={[classes.recipe_info, 'text-center'].join` `}>
          <h4> Modo de preparo</h4>
          <p> Separe um passo por linha</p>
          <textarea id="howTo" required className={[classes.textarea].join` `} onChange={handleFormDataChange}/>
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