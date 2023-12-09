from appwrite.client import Client
import os
import requests
import datetime

DadJokeSchema = {
    "id": {"type": "string"},
    "joke": {"type": "string"},
    "status": {"type": "string"},
    "insertedAtDateUTC": {"type": "datetime"},
}


def main(context):
    try:
        res = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        # context.log(res.json())

        dadJoke = {
            "id": res.json()["id"],
            "joke": res.json()["joke"],
            "status": str(res.json()["status"]),
            "insertedAtDateUTC": datetime.datetime.now().isoformat()
        }
    except requests.exceptions.RequestException as e:
        res = e

    dbClient = AppwriteDbClient(context)
    db = dbClient.try_create_database("primary_db")
    # collection = dbClient.try_create_collection(db, "Dadjokes", None, DadJokeSchema)
    collection = dbClient.try_create_collection(db, "Dadjokes", None, None)
    dbDoc = dbClient.addDocument(db, collection, dadJoke)

    return context.res.json({"message": "ok", **dadJoke})


if __name__ == "__main__":
    import sys
    import os
    import re

    cwd = os.getcwd()
    sys.path.append(re.sub(r"functions\/(.*)", "", cwd))
    # sys.path.append(cwd.replace("functions/dadjoke-extractor/src", ""))

    from functions.shared.mockContext import MockContext, loadLocalEnv
    from functions.shared.dbServices import AppwriteDbClient

    loadLocalEnv(cwd)
    main(MockContext())

else:
    from ...shared.dbServices import AppwriteDbClient
