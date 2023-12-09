from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import os
import requests
import datetime
import uuid
import json


def main(context):
    '''
    entry point for the function
    '''
    heartbeatUrl = os.environ.get("REMOTE_HEARTBEAT_URL", None)
    if heartbeatUrl:
        context.log(f"Calling {heartbeatUrl}")
        res = requests.get(heartbeatUrl)
        # context.log(res)
    else:
        res = "ERROR - No heartbeat url specified"
        context.log(res)
        exit(-1)

    heartBeatJson = {
        "now": str(datetime.datetime.now()),
        "res": {"status": res.status_code, "body": res.json()},
    }

    client = (
        Client()
        .set_endpoint("https://cloud.appwrite.io/v1")
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(os.environ["APPWRITE_API_KEY"])
    )

    databases = Databases(client)
    DATABASE_ID = "6563d535a0e17a3dba0e"
    COLLECTION = {"ID": "ef96a122b28c64372c698bee5614ae25", "NAME": "Heartbeats"}

    try:
        collection = databases.create_collection(
            DATABASE_ID, COLLECTION["ID"], COLLECTION["NAME"]
        )
    except AppwriteException as e:
        if e.message.startswith("A collection with the requested ID already exists"):
            pass
        else:
            context.log(f"Error creating collection: {e.message}")
            raise e

    # try:
    #     # db_id, collection_id, key, required, default, array
    #     result = databases.create_datetime_attribute(DATABASE_ID, COLLECTION['ID'], "now", False)
    #     # db_id, collection_id, key, size, required, default, array
    #     result = databases.create_string_attribute(DATABASE_ID, COLLECTION['ID'], 'res',200, False)
    # except AppwriteException as e:
    #     context.log(f'Error creating schema: {e.message}')
    #     raise e

    try:
        context.log("Adding document")
        dbDoc = databases.create_document(
            DATABASE_ID,
            COLLECTION["ID"],
            str(uuid.uuid4()),
            {"now": heartBeatJson["now"], "res": json.dumps(heartBeatJson["res"])},
        )
    except AppwriteException as e:
        context.log(f"Error creating document: {e.message}")
        raise e

    return context.res.json(heartBeatJson)


if __name__ == "__main__":
    import sys
    import os

    cwd = os.getcwd()
    sys.path.append(cwd.replace("functions/pynotifier/src", ""))

    from functions.shared.mockContext import MockContext, loadLocalEnv

    loadLocalEnv(cwd)
    main(MockContext())
