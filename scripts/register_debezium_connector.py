# scripts/register_connector.py

import requests
import json
import os

DEBEZIUM_CONNECT_URL = "http://localhost:8083/connectors"
# Resolve path relative to this script file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config/debezium-source.json")


def register_connector():
    with open(CONFIG_PATH, "r") as f:
        payload = f.read()
        headers = {"Content-Type": "application/json"}
        response = requests.post(DEBEZIUM_CONNECT_URL,
                                 headers=headers, data=payload)

        if response.status_code == 201:
            print("Connector registered successfully.")
        elif response.status_code == 409:
            print("Connector already exists.")
        else:
            print(
                f"Failed to register connector: {response.status_code} - {response.text}")


if __name__ == "__main__":
    register_connector()
