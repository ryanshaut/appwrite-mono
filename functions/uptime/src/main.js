import { Client, Health } from 'node-appwrite';

// This is your Appwrite function
// It's executed each time we get a request
export default async ({ req, res, log, error }) => {
  log('creating Appwrite client')
  const client = new Client()
  .setEndpoint(process.env.APPWRITE_BASE_URL + '/v1') // Your API Endpoint 
  .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID) // Your project ID 
  .setKey(process.env.HEALTHCHECK_API_KEY); // Your secret API key

  log('creating Health client')
  const health = new Health(client);
  log('fetching time from Health endpoint')
  const result = await health.getTime();
  
  if (req.method === 'GET') {
    return res.json({
      date: new Date(),
      health: result,
      request:{
        headers: req.headers,
        queryString: req.queryString,
        body: req.body
      }
    });
  } else {
    return res.json({message: `bad HTTP method ${req.method}`})
  }

};