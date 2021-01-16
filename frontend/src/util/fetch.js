const baseUrl = process.env.REACT_APP_SERVER_URL;


const get = async (url) => {
  const response = await fetch(baseUrl + url);
  return await response.json();
}

const post = async (url, reqOptions) => {

  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    ...reqOptions
  }

  const response = await fetch(baseUrl + url, options);
  return await response.json;
}

const functions = {get, post}

export default functions;