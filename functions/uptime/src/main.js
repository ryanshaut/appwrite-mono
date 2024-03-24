import { Client } from 'node-appwrite';
//const sdk = require('node-appwrite');

//const client = new sdk.Client() .setEndpoint('https://cloud.appwrite.io/v1') // Your API Endpoint 
//.setProject('5df5acd0d48c2') // Your project ID 
//.setKey('919c2d18fb5d4...a2ae413da83346ad2'); // Your secret API key

//const health = new sdk.Health(client);

//const result = await health.getTime();
// This is your Appwrite function
// It's executed each time we get a request
export default async ({ req, res, log, error }) => {
  log(process.env)
  log(new Date());
  if (req.method === 'GET') {
    return res.json({
      date: new Date(), 
      request:{
        headers: req.headers,
        queryString: req.queryString,
        body: req.body
      }
    });
  }

};