import os
from math import ceil

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SNIPE_API_KEY")


#total=35
offset=0
limit=0




#exit(0)

#url = "https://nationalrobotarium.snipe-it.io/api/v1/hardware?offset=0&limit=2&sort=created_at&order=desc"
url = "https://nationalrobotarium.snipe-it.io/api/v1/hardware?offset="+ str(offset) +"&limit="+str(limit)+"&sort=created_at&order=desc"


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + api_key
}


response = requests.get(url, headers=headers)

body = response.json()

robots = body['rows']




get_robot_gen_info = lambda r: {
    "id": r["id"],
    "name": r["name"],
    "location": r["location"],
    "maintainer": r.get("custom_fields").get("Maintainer")
}


print(body['total'])
print(body.keys())

for r in robots:
    # print(r.keys())
    # print("\n\n")
    # print(r['custom_fields'].keys())
    print(get_robot_gen_info(r))
