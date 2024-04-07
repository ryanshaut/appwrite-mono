import { Client, Databases } from 'node-appwrite';

function get_env_var(key){
  const value = process.env[key]
  if (!value){
    throw new Error(`Missing required env var ${key}`)
  }
  return value

}

function create_appwrite_client(){
  log('creating Appwrite client')
  const endpoint =  get_env_var('APPWRITE_BASE_URL') + '/v1'
  const project = get_env_var('APPWRITE_FUNCTION_PROJECT_ID')
  const api_key = get_env_var('HEALTHCHECK_API_KEY')
  const client = new Client()
  .setEndpoint(endpoint) // Your API Endpoint
  .setProject(project) // Your project ID
  .setKey(api_key); // Your secret API key
  return client
}

// This is your Appwrite function
// It's executed each time we get a request
export default async ({ req, res, log, error }) => {
  const client = create_appwrite_client()

    return res.json({
      date: new Date(),
      request:{
        //queryString: req.queryString,
        ...req
      }
    });

};