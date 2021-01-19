import os
import sys
import requests
import spotipy.util as util

# Figure out a way to get username/token using /authorize
# Run = python main.py {username} {daily_mix_number}
username = sys.argv[1]
scope = 'playlist-read-private'

try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

headers = {"Authorization": f"Bearer {token}"}

# Change get limit to more than 20
res = requests.get(f'https://api.spotify.com/v1/users/{username}/playlists', headers = headers)

res_json = res.json()
playlists = [i["name"] for i in res_json["items"]]

print(playlists)
# print(json.dumps(res_json, sort_keys = True, indent = 4))