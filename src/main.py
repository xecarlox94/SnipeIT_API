import os, json
from math import ceil

import requests
from dotenv import load_dotenv



from notion_client import Client

import logging
from notion_client import APIErrorCode, APIResponseError






load_dotenv()
api_key = os.getenv("SNIPE_API_KEY")



#total=35
offset=0
limit=0





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

# print(body['total'])
# print(body.keys())


items = list(map(get_robot_gen_info, robots))


#print(items)







notion = Client(
    auth=os.environ["NOTION_API_KEY"],
    log_level=logging.DEBUG
)

notion = Client(auth=os.environ["NOTION_API_KEY"])

db_id = os.environ["NOTION_DB_ID"]

database = notion.databases.query(
    **{
        "database_id": db_id
    }
)

print(json.dumps(database, indent=1))



def create_row_page(robot):

    robot_name = robot['name']

    row_page = {
        "Name": {"title": [{"text": {"content": robot_name}}]},
        "Tags": {"type": "multi_select", "multi_select": [{"name": "Class 1"}]}
    }

    notion.pages.create(
        parent={"database_id": db_id},
        properties=row_page
    )


for r in robots:

    create_row_page(r)



