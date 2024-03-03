from appwrite.client import Client
import os
from pyappwriteutils import AppwriteDbClient


MinecraftItemSchema = {
    "amount": {"type": "string"},
    "displayName": {"type": "string"},
    "fingerprint": {"type": "string"},
    "isCraftable": {"type": "boolean"},
    "name": {"type": "string"},
    "tags": {"type": "string"},
    "lastChangedAt": {"type": "datetime"},
}

def main(context):

    dbClient = AppwriteDbClient(context)
    db = dbClient.try_create_database("primary_db")
    collection = dbClient.try_create_collection(db, "Minecraft_items", None, None)
    # dbDoc = dbClient.addDocument(db, collection, dadJoke)

    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
        return context.res.json({"databases":dbClient.get_all_databases()})