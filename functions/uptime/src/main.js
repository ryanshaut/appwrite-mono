import { Client } from 'node-appwrite';

// This is your Appwrite function
// It's executed each time we get a request
export default async ({ req, res, log, error }) => {

  log(new Date());
  if (req.method === 'GET') {
    return res.json({
      date: new Date(), 
      request:{
        headers: JSON.stringify(req.headers),
        parameters: JSON.stringify(req.parameters),
        body: req.body
      }
    });
  }

};