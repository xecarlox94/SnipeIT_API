import os

import requests
from dotenv import load_dotenv


load_dotenv()

url = "https://develop.snipeitapp.com/api/v1/hardware?limit=2&offset=0&sort=created_at&order=desc"

api_key = os.getenv("SNIPE_API_KEY")



headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + api_key
}

response = requests.get(url, headers=headers)
print(response)
print(response.text)
