import { Client, Health, Users, ID } from 'node-appwrite';

// This is your Appwrite function
// It's executed each time we get a request
export default async ({ req, res, log, error }) => {
  log('creating Appwrite client')
  const endpoint =  process.env.APPWRITE_BASE_URL + '/v1'
  const project = process.env.APPWRITE_FUNCTION_PROJECT_ID
  const api_key = process.env.HEALTHCHECK_API_KEY
  const client = new Client()
  .setEndpoint(endpoint) // Your API Endpoint 
  .setProject(project) // Your project ID 
  .setKey(api_key); // Your secret API key

  if (req.method === 'GET') {
    return res.json({
      date: new Date(),
      request:{
        //queryString: req.queryString,
        ...req
      }
    });
  } else {
    return res.json({message: `bad HTTP method ${req.method}`})
  }

};