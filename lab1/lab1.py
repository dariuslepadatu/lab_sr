from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *
import csv
import os
from dotenv import load_dotenv

load_dotenv()

dataset_columns = {
    "title": "string",
    "fulltitle": "string",
    "description": "string",
    "view_count": "int",
    "categories": "set",
    "tags": "set",
    "duration": "double",
    "duration_string": "string",
    "live_status": "string",
    "thumbnail": "string",
    "channel": "string",
    "channel_url": "string",
    "channel_follower_count": "int"
}

user_columns = {
    "Person": "string",
    "PID": "string",
    "Team": "string",
    "Location": "string",
}

def init_client(database_id, token):
    client = RecombeeClient(
        database_id,
        token,
        region=Region.EU_WEST
    )
    return client


def add_item_properties(client, properties):
    try:
        for col in properties:
            client.send(AddItemProperty(col, properties[col]))
    except APIException as e:
        print(e)

def delete_item_properties(client, properties):
    try:
        for col in properties:
            client.send(DeleteItemProperty(col))
    except APIException as e:
        print(e)

def add_items(client, data):
    try:
        for i, item in enumerate(data):
            item_id = str(i)
            client.send(AddItem(item_id))
            client.send(SetItemValues(item_id, item))
            print(item_id)
    except APIException as e:
        print(e)


def delete_items(client, items_ids):
    try:
        for item_id in items_ids:
            client.send(DeleteItem(item_id))
            print(item_id)
    except APIException as e:
        print(e)


def add_user_properties(client, properties):
    try:
        for col in properties:
            client.send(AddUserProperty(col, properties[col]))
    except APIException as e:
        print(e)

def delete_user_properties(client, properties):
    try:
        for col in properties:
            client.send(DeleteUserProperty(col))
    except APIException as e:
        print(e)


def add_users(client, data):
    try:
        for i, user in enumerate(data):
            user_id = str(i)
            print(user_id, user)
            client.send(AddUser(user_id))
            client.send(SetUserValues(user_id, user))
    except APIException as e:
        print(e)


def delete_users(client, users_ids):
    try:
        for user_id in users_ids:
            client.send(DeleteUser(user_id))
            print(user_id)

    except APIException as e:
        print(e)

def parse_csv(csv_file, columns):
    parsed_rows = []
    with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            parsed_row = {}
            for col, col_type in columns.items():
                value = row.get(col, '').strip()

                if col_type == "int":
                    parsed_row[col] = int(value) if value.isdigit() else 0
                elif col_type == "double":
                    parsed_row[col] = float(value) if value else 0.0
                elif col_type == "set":
                    parsed_row[col] = value.split(',') if value else []
                else:
                    parsed_row[col] = value

            parsed_rows.append(parsed_row)

    return parsed_rows


if __name__ == "__main__":
    database_id = os.getenv("DATABASE_ID")
    token = os.getenv("API_TOKEN")

    client = init_client(database_id, token)
    # data = parse_csv("dataset.csv", dataset_columns)

    # add_item_properties(client, dataset_columns)

    delete_item_properties(client, dataset_columns)

    # add_items(client, data)

    # delete_items(client, range(len(data)))

    # users = parse_csv("people.csv", user_columns)

    # add_user_properties(client, user_columns)
    delete_user_properties(client, user_columns)

    # add_users(client, users)

    # delete_users(client, range(len(users)))

