from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import os
import uuid

from typing import Union


class AppwriteDbClient:
    def __init__(self, context):
        self.client = (
            Client()
            .set_endpoint("https://cloud.appwrite.io/v1")
            .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
            .set_key(os.environ["APPWRITE_API_KEY"])
        )
        self.context = context
        self.databases = Databases(self.client)
        self.get_all_databases()

    def get_all_databases(self) -> None:
        self.known_dbs = self.databases.list()["databases"]
        return self.known_dbs

    def get_collections_in_db(self, db) -> None:
        self.known_dbs = self.databases.list()["databases"]
        return self.known_dbs

    def db_exists(self, db_name: str) -> bool:
        exists = any((x for x in self.known_dbs if x["name"] == db_name))
        if not exists:
            self.get_all_databases()
            exists = any(
                (x for x in self.known_dbs["databases"] if x["name"] == db_name)
            )
        return exists

    def try_create_database(self, db_name: str, db_id: Union[str, None] = None):
        if self.db_exists(db_name):
            # self.context.log(f"{__name__} - Database {db_name} already exists")
            db = [x for x in self.known_dbs if x["name"] == db_name]
            self.db_id = db[0]["$id"]
            return db[0]
        if db_id is None:
            # self.context.log(f"{__name__} - No db_id provided, generating a random one")
            db_id = self.context.get_random_string(32)

        try:
            db = self.databases.create(db_id, db_name)
            self.db_id = db["$id"]
            return db
        except AppwriteException as e:
            self.context.error(
                f"{__name__} - Error creating database {db_name}: {e.message}"
            )
            return None

    def try_create_collection(
        self,
        db: dict,
        collection_name: str,
        collection_id: Union[str, None] = None,
        schema: Union[dict, None] = None
    ) -> dict:
        collections = self.databases.list_collections(db.get("$id"))
        if any((x for x in collections["collections"] if x["name"] == collection_name)):
            self.context.log(
                f"{__name__} - Collection {collection_name} already exists in database {db.get('$id')}"
            )
            collection = [
                x for x in collections["collections"] if x["name"] == collection_name
            ][0]
            collection_id = collection["$id"]
        else:
            self.context.log(
            f"{__name__} - Collection {collection_name} does not exist in database {db.get('$id')}"
            )
            if collection_id is None:
                collection_id = self.context.get_random_string(32)
            try:
                collection = self.databases.create_collection(
                    db.get("$id"), collection_id, collection_name
                )
            except AppwriteException as e:
                self.context.error(
                    f"{__name__} - Error creating collection {collection_name}: {e.message}"
                )
                return None
        if schema is None:
            return collection
        try:
            for key, value in schema.items():
                if value["type"] == "string":
                    self.context.log(f"{__name__} - Creating string attribute {key}")
                    self.databases.create_string_attribute(
                        db.get("$id"),
                        collection_id,
                        key,
                        value.get("length", 200),
                        value.get("required", False),
                        value.get("default", ""),
                        value.get("array", False),
                    )
                elif value["type"] == "datetime":
                    self.context.log(f"{__name__} - Creating datetime attribute {key}")
                    self.databases.create_datetime_attribute(
                        db.get("$id"),
                        collection_id,
                        key,
                        value.get("required", False),
                        value.get("default", None),
                        value.get("array", False),
                    )
                elif value["type"] == "boolean":
                    self.context.log(f"{__name__} - Creating boolean attribute {key}")
                    self.databases.create_boolean_attribute(
                        db.get("$id"),
                        collection_id,
                        key,
                        value.get("required", False),
                        value.get("default", ""),
                        value.get("array", False),
                    )
                elif value["type"] == "float":
                    self.context.log(f"{__name__} - Creating float attribute {key}")
                    self.databases.create_float_attribute(
                        db.get("$id"),
                        collection_id,
                        key,
                        value.get("required", False),
                        value.get("default", ""),
                        value.get("array", False),
                    )
                elif value["type"] == "integer":
                    self.context.log(f"{__name__} - Creating integer attribute {key}")
                    self.databases.create_integer_attribute(
                        db.get("$id"),
                        collection_id,
                        key,
                        value.get("required", False),
                        value.get("default", ""),
                        value.get("array", False),
                    )
                elif value["type"] == "object":
                    self.context.log(f"{__name__} - Creating object attribute {key}")
                    self.databases.create_object_attribute(
                        db.get("$id"),
                        collection_id,
                        key,
                        value.get("required", False),
                        value.get("default", None),
                        value.get("array", False),
                    )
            return collection
        except AppwriteException as e:
            self.context.error(
                f"{__name__} - Error updating schema {collection_name}: {e.message}"
            )
            return None

    def addDocument(self, db: dict, collection: dict, document: dict):
        try:
            doc = self.databases.create_document(
                db.get("$id"), collection.get("$id"), str(uuid.uuid4()), document
            )
            return doc
        except AppwriteException as e:
            self.context.error(
                f"{__name__} - Error creating document {document}: {e.message}"
            )
            return None


if __name__ == "__main__":
    import os
    from mockContext import MockContext, loadLocalEnv

    loadLocalEnv(os.path.abspath("../.env"))
    cwd = os.getcwd()
    c = AppwriteDbClient(MockContext())
    db = c.try_create_database("testdb1")
    c.try_create_collection(
        db,
    )
