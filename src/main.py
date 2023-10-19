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


print("running")

response = requests.get(url, headers=headers)
print("running")

body = response.json()

robots = body['rows']


def get_robot_gen_info(robot): 

    mnt = robot.get("custom_fields").get("Maintainer")
    if mnt is not None:
        mnt = mnt.get("value")
    else:
        mnt = ""

    loc = ""
    if robot["location"] is not None:
        loc = robot["location"]["name"]

    print(loc)

    return {
        "id": robot["id"],
        "name": robot["name"],
        "loc": loc,
        "cat": robot.get("category"),
        "mnt": mnt
    }


print(body['total'])
# print(body.keys())





notion = Client(auth=os.environ["NOTION_API_KEY"])

db_id = os.environ["NOTION_DB_ID"]

database = notion.databases.query(
    **{
        "database_id": db_id
    }
)

db_content = json.dumps(database, indent=1)

print(db_content)





print("\n\nEND NOTION DUMP\n\n")



def create_row_page(robot):

    print(robot)

    robot_name = robot['name']

    row_page = {
        "Name": {
            "title": [
                {
                    "text": { 
                        "content": robot_name 
                    }
                }
            ]
        },
        "ID": {
            "type": "number",
            "number": robot['id']
        },
        "Category": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": r['cat']['name']
                    },
                }
            ]
        },
        "Maintainer": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": r['mnt']
                    },
                }
            ]
        },
        "Location": {
            "id": "%3Fd%5CR",
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": r["loc"],
                    },
                }
            ]
        }
    }

    notion.pages.create(
        parent={"database_id": db_id},
        properties=row_page
    )




robots = list(
    filter(
        lambda r: r['cat']['id'] != 6,
        map(
            get_robot_gen_info,
            robots
        )
    )
)

#robots = list(map(lambda r: r['mnt'], robots))


for r in robots: create_row_page(r)


# "object": "page",
# "id": "5b0dfed0-8bca-4bc2-a2c7-70ac0ae42e4b",

