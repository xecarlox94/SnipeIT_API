
import os, json
from math import ceil

import requests
from dotenv import load_dotenv

from pprint import pprint

from notion_client import Client
import logging
from notion_client import APIErrorCode, APIResponseError


from flask import Flask
app = Flask(__name__)


load_dotenv()




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



def get_items_dict(
        item_type,
        get_gen_info_item=lambda x:x,
        filterf=lambda i: True,
        get_item_id=lambda i: i['id'],
    ):

    item_rows = req_get(f"{item_type}?offset=0&limit=0")['rows']

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
        get_db_entry_table,
        get_row_item,
        delete_row_item,
    ):

    print(db_id)

    database = notion.databases.query(
        **{
            "database_id": db_id
        }
    )

    results = database['results']

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
            archived=archived
        )

    def delete_row_page(page_id, iid):

        update_row_page(
            delete_row_item(iid),
            page_id,
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




@app.route("/checkout/consumable/<CONS_ID>")
def consume_item(CONS_ID):

    USER_ID=5

    req_post(
        f"consumables/{CONS_ID}/checkout",
        {
            "assigned_to": USER_ID
        }
    )



@app.route('/')
def hello_geek():



    # ManufacturersSuppliers, 8b77ab855e8549da8bc9a85ac508e21d
    # JustPeople, f97734ca13bc4fe9a76b2a2ac6fd95df



    def sync_assets(
            db_id_assets,
            assets_dict,
            filterf=lambda i: True,
        ):


        def get_gen_info_asset(asset):

            # mnt = robot.get("custom_fields").get("Maintainer")
            # if mnt is not None:
                # mnt = mnt.get("value")
            # else:
                # mnt = ""
            # loc = ""
            # if robot["location"] is not None:
                # loc = robot["location"]["name"]

            return {
                "id": asset["id"],
                "name": asset["name"],
            }


        get_db_entry_asset_table = lambda x: (
            x['properties']['ID']['number'],
            x['id']
        )


        get_row_asset = lambda a: {
            "Name": title_cell(a['name']),
            "ID": number_cell(a['id']),
        }


        delete_row_asset = lambda a_id: {
            "id": a_id,
            "name": "DELETE",
        }


        sync_table(
            db_id_assets,
            assets_dict,
            get_db_entry_asset_table,
            get_row_asset,
            delete_row_asset
        )


    # Assets, "65d8908c2a18400c9ffc25de796611c0"
    # AssetsUnavailableRepair, "77e76d14c4d64f4297630bc4fe18487a"
    # AssetsWarrantyExpiring, "0bd595cdbe9d446e89cafc920fef07e7"


    assets_dict = get_items_dict(
        "hardware",
    )

    print(assets_dict)

    sync_assets(
        "0bd595cdbe9d446e89cafc920fef07e7",
        assets_dict,
        filterf=lambda i: True,
    )



    print(assets_dict)


    return "Hello"



    #db_id_robots = os.environ["NOTION_DB_ID"]
    db_id_robots = "3412568aa7914734b22cd1a34b43ad7a"

    def sync_robots(
            db_id, # Robots, 3412568aa7914734b22cd1a34b43ad7a
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



        get_db_entry_robots_table = lambda x: (
            x['properties']['ID']['number'],
            x['id']
        )


        get_row_robot = lambda r: {
            "Name": title_cell(r['name']),
            "ID": number_cell(r['id']),
            "Category": text_cell(r['cat']['name']),
            "Maintainer": text_cell(r['mnt']),
            "Location": text_cell(r['loc']),
        }


        delete_row_robot = lambda rid: {
            "id": rid,
            "name": "DELETE",
            "loc": "DELETE",
            "cat": {
                'id': rid,
                'name': "DELETE"
            },
            "mnt": "DELETE"
        }



        robots_dict = get_items_dict(
            "hardware",
            get_gen_info_item=get_gen_info_robot,
            filterf=lambda i: True,
        )


        pprint(robots_dict)


        sync_table(
            db_id_robots,
            robots_dict,
            get_db_entry_robots_table,
            get_row_robot,
            delete_row_robot
        )

    """
    # ConsumablesPurchaseHistory, 817259b1f9ba45e583c335f7b19eb800
    consumable_actions = get_items_dict(
        "reports/activity",
        filterf=lambda i: i['action_type'] == 'create new' and (
            True #i['item']['type'] in ['consumable']
        ),
    )
    pprint(list(map(lambda i: i['item']['type'] == 'consumable', consumable_actions)))
    """


    return '\n<h1>Updated Notion!</h1>\n'



if __name__ == "__main__":
    app.run(debug=True)

