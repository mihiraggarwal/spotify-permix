import os
import sys
import json
import requests
import spotipy.util as util

# Figure out a way to get username/token using /authorize
# Run = python main.py {username} {daily_mix_number}
# Remove cache before committing
# Prerequisites - following the playlist

username = sys.argv[1]
number = sys.argv[2]
scope = 'playlist-read-private'

try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

headers = {"Authorization": f"Bearer {token}"}

# Change get limit to more than 20
res_playlists = requests.get(f'https://api.spotify.com/v1/users/{username}/playlists', headers = headers)
respl_json = res_playlists.json()

mix_id = ''
for i in respl_json["items"]:
    if i["name"] == f"Daily Mix {number}":
        mix_id = i["id"]
        break
else:
    print(f"Could not find Daily Mix {number} in followed playlists")
    quit()

res_tracks = requests.get(f"https://api.spotify.com/v1/playlists/{mix_id}/tracks", headers = headers)
restr_json = res_tracks.json()

tracks = {}
for i in restr_json["items"]:
    tracks[i["track"]["name"]] = i["track"]["id"]

print(tracks)
# print(json.dumps(restr_json, sort_keys = True, indent = 4))
