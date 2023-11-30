from appwrite.client import Client
from appwrite.services.databases import Databases
import os
import requests
import datetime
import uuid


# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    heartbeatUrl = os.environ.get('REMOTE_HEARTBEAT_URL', None)
    if heartbeatUrl:
        context.log(f'Calling {heartbeatUrl}')
        res = requests.get(heartbeatUrl)
        # context.log(res)
    else:
        res = "ERROR - No heartbeat url specified"
        context.log(res)
        exit(-1)

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
    # collection = databases.create_collection(DATABASE_ID, COLLECTION['ID'], COLLECTION['NAME'])

    dbDoc = databases.create_document(DATABASE_ID, COLLECTION['ID'], str(uuid.uuid4()), heartBeatJson)

    return context.res.json(heartBeatJson)

if __name__ == '__main__':
    import sys
    import os
    cwd = os.getcwd()
    sys.path.append(cwd.replace('functions/pynotifier/src',''))

    from functions.shared.mockContext import MockContext,loadLocalEnv
    loadLocalEnv(os.path.abspath('../.env'))
    main(MockContext())