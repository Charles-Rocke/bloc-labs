# Helper methods

import requests
import json
"""
    production env
"""
# get env variables
def get_env_variables():
    url = (
        "https://api.render.com/v1/services/srv-chn4p1m7avj3o321d4h0/env-vars?limit=20"
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
    url = "https://api.render.com/v1/services/srv-chn4p1m7avj3o321d4h0/env-vars"

    payload = [
        {"key": "SECRET_KEY", "value": "RfUjXn2r5u8x/A%D*G-KaPdSgVkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!z%C*F-J@NcRfUjXn2r5u8x/A?D(G+KbPdSgVkYp3s6v9y$B&E)H@McQfThWmZq4t7w!z%C*F-JaNdRgUkXn2r5u8x/A?D(G+KbPeShVmYq3t6v9y$B&E)H@McQfTjWnZr4u7x!z%C*F-JaNdRgUkXp2s5v8y/B?D(G+KbPeShVmYq3t6w9z$C&F)H@McQfTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v8y/B?E(H+MbQeShVmYq3t6w9z$C&F)J@NcRfUjWnZr4u7x!A%D*G-KaPdSgVkYp2s5v8y/B?E(H+MbQeThWmZq4t6w9z$C&F)J@NcRfUjXn2r5u8x!A%D*G-KaPdSgVkYp3s6v9y$B?E(H+MbQeThWmZq4t7w!z%C*F)J@NcRfUjXn2r5u8x/A?D(G+KaPdSgVkYp3s6v9y$B&E)H@McQeThWmZq4t7w!z%C*F-JaN"},
        {
            "key": "DATABASE_URL",
            "value": "postgresql://blocsquad_prod:6rgckwPN9z8u746boeiBQhVlHYpOZuCo@dpg-chn4ocm4dad21k4m0n60-a.ohio-postgres.render.com/bloc_prod_db",
        },
        {"key": "SERVER_NAME", "value": "bloc"},
        {"key": "SERVER_ORIGIN", "value": "https://bloc.id"},
        {"key": "SERVER_ID", "value": "bloc.id"},
        {"key": "MIXPANEL_PROJECT_ID", "value": "a3296db38d1b8533b188f4281b20fb51"},
    ]
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer rnd_h2ezMpqcy92kIx4mNCanLdoCTP1e",
    }

    response = requests.put(url, json=payload, headers=headers).json()

    return response



"""
    testing env
"""
# get testing env variables
def get_testing_env_variables():
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
def update_testing_env_variables():
    url = "https://api.render.com/v1/services/srv-chkhdam7avj217eb1k80/env-vars"

    payload = [
        {"key": "SECRET_KEY", "value": "bloc-testing"},
        {
            "key": "DATABASE_URL",
            "value": "postgresql://blocsquad_test_db:GYQxHXw4110RUu5mWDLbsTHYZwEgCMid@dpg-chl3ug67avj2179cm1fg-a.ohio-postgres.render.com/bloc_test_db",
        },
        {"key": "SERVER_NAME", "value": "Testing"},
        {"key": "SERVER_ORIGIN", "value": "https://bloc-testing.onrender.com"},
        {"key": "SERVER_ID", "value": "bloc-testing.onrender.com"},
        {"key": "MIXPANEL_PROJECT_ID", "value": "1ba15c80ce8bc4322c3cdbd7815f21e3"},
    ]
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer rnd_h2ezMpqcy92kIx4mNCanLdoCTP1e",
    }

    response = requests.put(url, json=payload, headers=headers).json()

    return response
