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

  //let users = new Users(client);

  //let user = await users.create(ID.unique(), "email@example.com", "+123456789", "password", "Walter O'Brien");

  log('creating Health client')
  const health = new Health(client);
  log('fetching time from Health endpoint')
  const result = null
  try {  
    result = await health.getTime();
  } catch (e){
    log(`error checking health ${e}`)
  }
  if (req.method === 'GET') {
    return res.json({
      date: new Date(),
      health: result,
    //  user,
      request:{
        //headers: req.headers,
        queryString: req.queryString,
        //body: req.body
      }
    });
  } else {
    return res.json({message: `bad HTTP method ${req.method}`})
  }

};