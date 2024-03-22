from dotenv import load_dotenv,dotenv_values
import os

load_dotenv()
class DotEnv():
    def dotenv(self, env_key=None):
        if env_key is None:
            return dotenv_values(".env")
        else:
            return os.getenv(env_key)