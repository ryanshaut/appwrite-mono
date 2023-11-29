from appwrite.client import Client
from appwrite.services.databases import Databases
import os
import requests
import datetime


# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    heartbeatUrl = os.environ.get('REMOTE_HEARTBEAT_URL', None)
    if heartbeatUrl:
        res = requests.get(heartbeatUrl)
        context.log(res)
    else:
        res = "No heartbeat url specified"

    heartBeatJson =         {
            "now": str(datetime.datetime.now()),
            "res": {
                "status": res.status_code,
                "body": res.json()
            }
        }

    client = (
        Client()
        .set_endpoint("https://cloud.appwrite.io/v1")
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(os.environ["APPWRITE_API_KEY"])
    )

    databases = Databases(client)
    DATABASE_ID= '6563d535a0e17a3dba0e'
    COLLECTION = {
        "ID": 'ef96a122b28c64372c698bee5614ae25',
        "NAME": "Heartbeats"
    }
    collection = databases.create_collection(DATABASE_ID, COLLECTION['ID'], COLLECTION['NAME'])

    dbDoc = databases.create_document(DATABASE_ID, COLLECTION['ID'], uuid.uuid4(), heartBeatJson)

    return context.res.json(heartBeatJson)
    # Why not try the Appwrite SDK?
    #
    # client = (
    #     Client()
    #     .set_endpoint("https://cloud.appwrite.io/v1")
    #     .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #     .set_key(os.environ["APPWRITE_API_KEY"])
    # )

    # # You can log messages to the console
    # context.log("Hello, Logs!")

    # # If something goes wrong, log an error
    # context.error("Hello, Errors!")

    # # The `ctx.req` object contains the request data
    # if context.req.method == "GET":
    #     # Send a response with the res object helpers
    #     # `ctx.res.send()` dispatches a string back to the client
    #     return context.res.send("Hello, World!")

    # # `ctx.res.json()` is a handy helper for sending JSON
    # return context.res.json(
    #     {
    #         "motto": "Build like a team of hundreds_",
    #         "learn": "https://appwrite.io/docs",
    #         "connect": "https://appwrite.io/discord",
    #         "getInspired": "https://builtwith.appwrite.io",
    #     }
    # )
