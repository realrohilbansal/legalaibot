import os
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # os.getenv("AWS_ACCESS_KEY_ID")
    # os.getenv("AWS_SECRET_ACCESS_KEY")
    return openai_api_key
