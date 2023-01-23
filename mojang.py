import requests

def get_uuid(name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{name}?'
    response = requests.get(url)
    uuid = response.json()["id"]
    return uuid

def get_name(uuid):
    url = f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'
    response = requests.get(url)
    name = response.json()["name"]
    return name
