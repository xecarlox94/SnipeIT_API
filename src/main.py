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



get_row_robot = lambda r: {
    "Name": title_cell(r['name']),
    "ID": number_cell(r['id']),
    "Category": text_cell(r['cat']['name']),
    "Maintainer": text_cell(r['mnt']),
    "Location": text_cell(r['loc']),
}


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


def req_snipeit(f, end_point, body={}):
    url = f"https://nationalrobotarium.snipe-it.io/api/v1/{end_point}"

    print(url)
    return f(
        url,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + os.getenv("SNIPE_API_KEY")
        },
        json=body
    ).json()


get_body = lambda end_point: req_snipeit(
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


# CONSUMABLES endpoint
#
#
# post_consume = lambda
# @app.route("...")
# def consume_item():

@app.route('/')
def hello_geek():

    """
    ID=9

    USER_ID=5

    curl \
        --request POST \
        --url "$NR_URL/consumables/$ID/checkout" \
        --header "Authorization: Bearer $API_KEY" \
        --header "accept: application/json" \
        --header "content-type: application/json" \
        -d "{\"assigned_to\": $USER_ID}"
    """
    CONSUMABLE_ID=9

    req_post(
        f"consumables/{9}/checkout",
        {
            "assigned_to": 5
        }
    )


    return "done"

    robots_dict = dict(
        map(
            lambda r: (r['id'], r),
            filter(
                lambda r: True, #r['cat']['id'] != 6 and not r["id"] == 60,
                map(
                    get_gen_info_robot,
                    body['rows']
                )
            )
        )
    )


    db_id_robots = os.environ["NOTION_DB_ID"]
    db_id_robots = "3412568aa7914734b22cd1a34b43ad7a"

    get_db_entry_robots_table = lambda x: (
        x['properties']['ID']['number'],
        x['id']
    )

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


    def sync_table(
            db_id,
            items_dict,
            get_db_entry_table,
            get_row_item,
            delete_row_item,
        ):

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

        pprint(
            list(
                map(
                    lambda x: x['properties']['ID'],
                    filter(
                        lambda x: True,
                        results
                    )
                )
            )
        )

        # delete_row_page(page_id, iid)

        #return


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



    sync_table(
        db_id,
        robots_dict,
        get_db_entry_robots_table,
        get_row_robot,
        delete_row_robot
    )


    return '\n<h1>Updated Notion!</h1>\n'


if __name__ == "__main__":
    app.run(debug=True)

