import json
import os
from dotenv import dotenv_values


# loads any *.env files in the directory tree above the scriptDir with the closest to the running file taking precedence
def loadLocalEnv(scriptDir: str) -> None:
    MockContext().log(f'{__name__} - Loading dotenv')
    MockContext().log(f'{__name__} - Loading envs, starting at {scriptDir}')

    directory = scriptDir
    found_envs = []
    while directory:
        localEnvPath = os.path.join(directory, ".env")
        if os.path.isfile(localEnvPath):
            MockContext().log(f'{__name__} - Found .env at {localEnvPath}')
            found_envs.append(localEnvPath)
        directory = directory[0:directory.rindex('/')]
        
    for env in reversed(found_envs):
        config = dotenv_values(env)
        os.environ.update(config)

class MockRes():
    def __init__(self):
        self.status_code = 200
        self.json = lambda x: self.log(f"res.json - {json.dumps(x)}")
        self.send = lambda x: self.log(f"res.send - {x}")

    def log(self, message: any) -> None:
        print(str(message))

    def error(self, message: str) -> None:
        self.log(message)

class MockReq():
    def __init__(self):
        self.status_code = 200
        self.method = "GET"
        self.path = "/"

class MockContext():
    def __init__(self):
        self.res = MockRes()
        self.req = MockReq()

    def log(self, message: any) -> None:
        print(f"context.log - {str(message)}")

    def error(self, message: str) -> None:
        print(f"context.error - {str(message)}")

    def get_random_string(self, length) -> str:
        # generate hex string of length length
        return os.urandom(length//2).hex()

    