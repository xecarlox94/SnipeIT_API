import os, json
from math import ceil

import requests
from dotenv import load_dotenv

from pprint import pprint

from notion_client import Client
import logging
from notion_client import APIErrorCode, APIResponseError



load_dotenv()





get_row_robot = lambda robot: {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": robot['name']
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

def get_robot_gen_info(robot):

    mnt = robot.get("custom_fields").get("Maintainer")
    if mnt is not None:
        mnt = mnt.get("value")
    else:
        mnt = ""

    loc = ""
    if robot["location"] is not None:
        loc = robot["location"]["name"]

    return {
        "id": robot["id"],
        "name": robot["name"],
        "loc": loc,
        "cat": robot.get("category"),
        "mnt": mnt
    }




#total=35
offset=0
limit=0

body = requests.get(
        "https://nationalrobotarium.snipe-it.io/api/v1/hardware?offset="+ str(offset) +"&limit="+str(limit)+"&sort=created_at&order=desc"
    , headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + os.getenv("SNIPE_API_KEY")
}).json()


robots_dict = dict(
    map(
        lambda r: (r['id'], r),
        filter(
            lambda r: r['cat']['id'] != 6,
            map(
                get_robot_gen_info,
                body['rows']
            )
        )
    )
)



notion = Client(auth=os.environ["NOTION_API_KEY"])
db_id = os.environ["NOTION_DB_ID"]


database = notion.databases.query(
    **{
        "database_id": db_id
    }
)


db_entries_dict = dict(map(
    lambda x: (
        x['properties']['ID']['number'],
        x['id']
    ),
    database['results']
))


#pprint(db_entries_dict)
#pprint(robots_dict)


db_entries_keys = set(db_entries_dict.keys())
robots_keys = set(robots_dict.keys())

pprint(db_entries_keys)
pprint(robots_keys)

pprint("to add")
pprint(robots_keys - db_entries_keys)

pprint("to update")
to_update = db_entries_keys & robots_keys
pprint(to_update)

print("to remove")
to_remove_set = db_entries_keys - robots_keys
pprint(to_remove_set)




def create_row_page(robot):
    notion.pages.create(
        parent={
            "database_id": db_id
        },
        properties=get_row_robot(robot)
    )
#for r in robots: create_row_page(r)
