import os, json
from math import ceil

import requests
from dotenv import load_dotenv




from pprint import pprint


from notion_client import Client

import logging
from notion_client import APIErrorCode, APIResponseError


# notion = Client(
#     auth=os.environ["NOTION_API_KEY"],
#     log_level=logging.DEBUG
# )

notion = Client(auth=os.environ["NOTION_API_KEY"])


database = notion.databases.query(
    **{
        "database_id":os.environ["NOTION_DB_ID"]
    }
)

print(type(database))
print(json.dumps(database, indent=1))

#notion.pages.create({


# load_dotenv()
# api_key = os.getenv("SNIPE_API_KEY")
#
#
#
# token = os.getenv("NOTION_API_KEY")
# databaseID = os.getenv("NOTION_DB_ID")
#
#
# headers = {
    # "Authorization": "Bearer " + token,
    # "Content-Type": "application/json",
    # "Notion-Version": "2022-02-22"
# }
#
#
# createUrl = 'https://api.notion.com/v1/pages'

# res = requests.request("GET", createUrl, headers=headers)
# print(res)

"""
# Create a Page
def createPage(databaseID, headers):


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


    # print(body['total'])
    # print(body.keys())

    for r in robots:
        # print(r.keys())
        # print("\n\n")
        # print(r['custom_fields'].keys())
        # print(get_robot_gen_info(r))

    list(map(robots, lambda r: get_robot_gen_info(r)))

    print


    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": { "database_id": databaseID },
        "properties": {
            "Text": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "This is thienqc"
                            },
                        }
                    ]
                },
            }
        }
    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)
    print(res)
createPage(databaseID, headers)
"""
