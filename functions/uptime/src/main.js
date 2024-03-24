import { Client } from 'node-appwrite';
const client = new Client()
  .setEndpoint(process.env.APPWRITE_BASE_URL + '/v1') // Your API Endpoint 
  .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID) // Your project ID 
  .setKey(process.env.HEALTHCHECK_API_KEY); // Your secret API key

// This is your Appwrite function
// It's executed each time we get a request
export default async ({ req, res, log, error }) => {

  log(process.env)
  const health = new sdk.Health(client);
  const result = await health.getTime();
  
  log(new Date());
  if (req.method === 'GET') {
    return res.json({
      date: new Date(),
      health,
      request:{
        headers: req.headers,
        queryString: req.queryString,
        body: req.body
      }
    });
  }

};