from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *
import csv

database_id = 'lab-dev'
token = ''

columns = {
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

def init_client(database_id, token):
    client = RecombeeClient(
        database_id,
        token,
        region=Region.EU_WEST
    )
    return client


def set_item_properties(client, properties):
    for col in properties:
        client.send(AddItemProperty(col, properties[col]))

def parse_csv(csv_file, columns):
    parsed_rows = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
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


    client = init_client(database_id, token)
    data = parse_csv("dataset.csv", columns)


    # set_item_properties(client, columns)


    for i, item in enumerate(data):
        item_id = str(i)
        client.send(AddItem(item_id))


