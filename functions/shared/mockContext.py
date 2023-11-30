import json
import os
from dotenv import dotenv_values, load_dotenv


def loadLocalEnv(localEnvPath):
    MockContext().log(f'{__name__} - Loading dotenv')
    MockContext().log(f'{__name__} - Loading {localEnvPath}')

    config = {
        **dotenv_values(".env"),  # load shared development variables
        **dotenv_values(localEnvPath),  # load shared development variables
        **os.environ,  # override loaded values with environment variables
    }
    os.environ.update(config)

class MockContext():
    def __init__(self):
        self.res = {
            "json": lambda x: self.log(json.dumps(x)),
            "send": lambda x: self.log(x)
        }
        self.req = {
            "method": "GET"
        }

    def log(self, message):
        print(str(message))

    def error(self, message):
        self.log(message)

    