import os
from dotenv import load_dotenv

load_dotenv(override=True)

pushover_token = os.getenv('PUSHOVER_TOKEN')
pushover_user = os.getenv('PUSHOVER_USER')

print(pushover_token, pushover_user)
