const baseUrl = process.env.REACT_APP_SERVER_URL;

export async function get(url){
  const response = await fetch(baseUrl + url);
  return await response.json();
}

export async function post(url, reqOptions){

  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    ...reqOptions
  }

  try{
    const response = await fetch(baseUrl + url, options);
    const data = await response.json();
    return {status: 200, data: data};
  } catch (e) {
    return { status: 500}
  }
}