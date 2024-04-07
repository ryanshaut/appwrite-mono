import { Client, Databases } from 'node-appwrite';

import mysql from 'mysql2/promise';

function create_mysql_client(){

  // Create the connection pool. The pool-specific settings are the defaults
  const pool = mysql.createPool({
    host: get_env_var('MYSQL_DB_HOST'),
    user: get_env_var('MYSQL_DB_USER'),
    database: get_env_var('MYSQL_DB_DATABASE'),
    password: get_env_var('MYSQL_DB_PASSWORD'),
    waitForConnections: true,
    connectionLimit: 10,
    maxIdle: 10, // max idle connections, the default value is the same as `connectionLimit`
    idleTimeout: 60000, // idle connections timeout, in milliseconds, the default value 60000
    queueLimit: 0,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0,
  });
  return pool
}

function get_env_var(key){
  const value = process.env[key]
  if (!value){
    throw new Error(`Missing required env var ${key}`)
  }
  return value

}

function create_appwrite_client(){
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
  log('creating Appwrite client')
  const client = create_appwrite_client()

  log('creating mysql client')
  const db_client = create_mysql_client()
  try {
    // For pool initialization, see above
    const [rows, fields] = await pool.query('SELECT 1 + 1 AS solution');
    // Connection is automatically released when query resolves
  } catch (err) {
    console.log(err);
    rows = [err]
    fields = [err]
  }
    return res.json({
      date: new Date(),
      rows,
      fields,
      request:{
        //queryString: req.queryString,
        ...req
      }
    });

};