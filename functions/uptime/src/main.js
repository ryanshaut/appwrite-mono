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

export default async ({ req, res, log, error }) => {
  // blank favicon request
  if (req.url === '/favicon.ico') {
    return res.empty();
  }

  if (req.query.API_KEY !== get_env_var('UPTIME_CLIENT_API_KEY')){
    return res.json({error: 'Unauthorized'}, 403)
  }
  const db_client = create_mysql_client()
  
  const response = {
    version: '1.0',
    date: new Date(),
    source: req.query.source
  }
  
  if (req.query.includeRequest && (req.query.includeRequest == 'true')){
    response.request = req
  } 
  
  let rows, fields, dbError = null
  try {
    log('Inserting into database')
    table = get_env_var('MYSQL_DB_DATABASE')
    [rows, fields] = await db_client.execute(`INSERT INTO ${table} (data) VALUES (?)`, [JSON.stringify(response)]);
    log(`Done, inserted ${rows.affectedRows} rows`);
  } catch (err) {
    log(err);
    dbError = err;
  }
  return res.json({rows, fields, dbError, response});

};