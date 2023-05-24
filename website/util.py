# Helper methods

import requests


# get env variables
def get_env_variables():
    url = (
        "https://api.render.com/v1/services/srv-chkhdam7avj217eb1k80/env-vars?limit=20"
    )

    headers = {
        "accept": "application/json",
        "authorization": "Bearer rnd_h2ezMpqcy92kIx4mNCanLdoCTP1e",
    }

    response = requests.get(url, headers=headers).json()

    # sort though data to get each key and value
    key_value_pairs = {}  # Initialize an empty dictionary to store key-value pairs

    for element in response:
        env_var = element["envVar"]
        key = env_var["key"]
        value = env_var["value"]
        key_value_pairs[key] = value

    return key_value_pairs


# update env variables
def update_env_variables():
    url = "https://api.render.com/v1/services/srv-chkhdam7avj217eb1k80/env-vars"

    payload = [
        {"key": "SECRET_KEY", "value": "3xKZ{:>AEvc0!MvQ/+q}5we98Zx4-I"},
        {
            "key": "DATABASE_URL",
            "value": "postgresql://blocsquad_prod:6rgckwPN9z8u746boeiBQhVlHYpOZuCo@dpg-chn4ocm4dad21k4m0n60-a.ohio-postgres.render.com/bloc_prod_db",
        },
        {"key": "SERVER_NAME", "value": "bloc"},
        {"key": "SERVER_ORIGIN", "value": "https://bloc.id"},
        {"key": "SERVER_ID", "value": "bloc.id"},
    ]
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer rnd_h2ezMpqcy92kIx4mNCanLdoCTP1e",
    }

    response = requests.put(url, json=payload, headers=headers).json

    return response
