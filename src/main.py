import os, json

from functools import reduce
from math import ceil
from pprint import pprint

import requests

from dotenv import load_dotenv

from notion_client import Client
from notion_client import APIErrorCode, APIResponseError
from notion_client.helpers import iterate_paginated_api

import logging

from flask import Flask



app = Flask(__name__)

load_dotenv()


dbs_dict = json.load(open("notion_dbs.json"))



# Notion Logic
notion = Client(auth=os.environ["NOTION_API_KEY"])


title_cell = lambda v: {
    "title": [
        {
            "text": {
                "content": v
            }
        }
    ]
}

text_cell = lambda v: {
    "type": "rich_text",
    "rich_text": [
        {
            "type": "text",
            "text": {
                "content": v
            },
        }
    ]
}

number_cell = lambda v: {
    "type": "number",
    "number": v
}



# Snipe it logic





def req_snipeit(f, end_point, body={}):
    url = f"https://nationalrobotarium.snipe-it.io/api/v1/{end_point}"

    return f(
        url,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + os.getenv("SNIPE_API_KEY")
        },
        json=body
    ).json()


req_get = lambda end_point: req_snipeit(
    requests.get,
    end_point
)


req_post = lambda end_point, body: req_snipeit(
    requests.post,
    end_point,
    body=body
)

req_patch = lambda end_point, body: req_snipeit(
    requests.patch,
    end_point,
    body
)


get_item_rows = lambda item_type: req_get(
    f"{item_type}?offset=0&limit=0"
)['rows']


def get_items_dict(
        item_rows,
        get_gen_info_item=lambda x:x,
        filterf=lambda i: True,
        get_item_id=lambda i: i['id'],
    ):

    return dict(
        map(
            lambda item: (get_item_id(item), item),
            filter(
                filterf,
                map(
                    get_gen_info_item,
                    item_rows
                )
            )
        )
    )



def sync_table(
        db_id,
        items_dict,
        get_row_item,
        get_db_entry_table=lambda x: (
            x['properties']['ID']['number'],
            x['id']
        ),
    ):


    blocks = iterate_paginated_api(
        notion.databases.query, database_id=db_id
    )

    results = reduce(
        lambda l, i: l + i,
        list(blocks),
        []
    )


    db_entries_dict = dict(map(
        get_db_entry_table,
        results
    ))


    db_entries_keys = set(db_entries_dict.keys())


    items_keys = set(items_dict.keys())

    to_add_set = items_keys - db_entries_keys

    to_update_set = db_entries_keys & items_keys

    to_remove_set = db_entries_keys - items_keys


    def create_row_page(item):
        notion.pages.create(
            parent={
                "database_id": db_id
            },
            properties=get_row_item(item)
        )


    def update_row_page(item, page_id, archived=False):
        notion.pages.update(
            parent={
                "database_id": db_id
            },
            properties=get_row_item(item),
            page_id=page_id,
            archived=False
        )

    def delete_row_page(page_id, iid):
        notion.pages.update(
            parent={
                "database_id": db_id
            },
            properties={},
            page_id=page_id,
            archived=True
        )


    for iid in to_update_set:

        item = items_dict[iid]
        page_id = db_entries_dict[iid]

        update_row_page(
            item,
            page_id
        )


    for iid in to_remove_set:

        page_id = db_entries_dict[iid]

        delete_row_page(page_id, iid)


    for iid in to_add_set:

        i = items_dict[iid]

        create_row_page(i)



def sync_robots(
        db_id,
        assets_rows,
        filterf=lambda i: True,
    ):


    def get_gen_info_robot(robot):

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


    get_row_robot = lambda r: {
        "Name": title_cell(r['name']),
        "ID": number_cell(r['id']),
        "Category": text_cell(r['cat']['name']),
        "Maintainer": text_cell(r['mnt']),
        "Location": text_cell(r['loc']),
    }


    f_pcs = lambda r_cat: "Robot" in r_cat


    robots_dict = get_items_dict(
        assets_rows,
        get_gen_info_item=get_gen_info_robot,
        filterf=lambda r: filterf(r) and f_pcs(r['cat']['name']),
    )


    sync_table(
        db_id,
        robots_dict,
        get_row_robot,
    )





@app.route('/')
def hello_geek():


    sync_table(
        dbs_dict["SuppliersManufacturers"],
        get_items_dict(
            get_item_rows("manufacturers"), # Need to add Suppliers
            get_gen_info_item=lambda p:{
                "id": p["id"],
                "name": p["name"],
            }
        ),
        lambda p: {
            "Name": title_cell(p['name']),
            "ID": number_cell(p['id']),
        }
    )


    sync_table(
        dbs_dict["Consumables"],
        get_items_dict(
            get_item_rows("consumables"),
            get_gen_info_item=lambda p:{
                "id": p["id"],
                "name": p["name"],
            }
        ),
        lambda p: {
            "Name": title_cell(p['name']),
            "ID": number_cell(p['id']),
        }
    )


    sync_table(
        dbs_dict["People"],
        get_items_dict(
            get_item_rows("users"),
            get_gen_info_item=lambda p:{
                "id": p["id"],
                "name": p["name"],
            }
        ),
        lambda p: {
            "Name": title_cell(p['name']),
            "ID": number_cell(p['id']),
        }
    )


    assets_rows = get_item_rows("hardware")


    sync_table(
        dbs_dict["Equipments"],
        get_items_dict(
            assets_rows,
            get_gen_info_item=lambda p:{
                "id": p["id"],
                "name": p["name"],
                "cat": p.get("category")['name']
            },
            filterf=lambda p: (
                ("Robot -" not in p['cat']) or
                ("Computer -" not in p['cat'])
            )
        ),
        lambda p: {
            "Name": title_cell(p['name']),
            "ID": number_cell(p['id']),
        }
    )


    sync_table(
        dbs_dict["Assets_UnavailableRepair"],
        get_items_dict(
            assets_rows,
            get_gen_info_item=lambda p:{
                "id": p["id"],
                "name": p["name"],
                "cat": p.get("category")['name']
            },
            filterf=lambda p: (
                ("Robot -" not in p['cat']) or
                ("Computer -" not in p['cat'])
            )
        ),
        lambda p: {
            "Name": title_cell(p['name']),
            "ID": number_cell(p['id']),
        }
    )


    sync_table(
        dbs_dict["Assets_WarrantyExpiring"],
        get_items_dict(
            assets_rows,
            get_gen_info_item=lambda p:{
                "id": p["id"],
                "name": p["name"],
                "cat": p.get("category")['name']
            },
            filterf=lambda p: (
                ("Robot -" not in p['cat']) or
                ("Computer -" not in p['cat'])
            )
        ),
        lambda p: {
            "Name": title_cell(p['name']),
            "ID": number_cell(p['id']),
        }
    )


    sync_robots(
        dbs_dict["Robots"],
        assets_rows
    )


    return '\n<h1>Updated Notion!</h1>\n'





@app.route("/checkout/consumable/<CONS_ID>")
def consume_item(CONS_ID):

    USER_ID=5

    req_post(
        f"consumables/{CONS_ID}/checkout",
        {
            "assigned_to": USER_ID
        }
    )




if __name__ == "__main__":
    app.run(debug=True)



