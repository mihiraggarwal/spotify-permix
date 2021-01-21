import os
import sys
import json
import requests
import datetime
import spotipy.util as util

# Figure out a way to get username/token using /authorize
# Run = python main.py {username} {daily_mix_number}
# Remove cache before committing
# Prerequisites - following the playlist

username = sys.argv[1]
number = sys.argv[2]
scope = 'playlist-read-private playlist-modify-private'
client_id = "a27eac5f72414c3190b565abd15eb2f1"

try:
    token = util.prompt_for_user_token(username, scope, client_id)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope, client_id)

headers = {"Authorization": f"Bearer {token}"}

# Change get limit to more than 20
res_playlists = requests.get(f'https://api.spotify.com/v1/users/{username}/playlists', headers = headers)
respl_json = res_playlists.json()

mix_id = ''
mix_desc = ''
for i in respl_json["items"]:
    if i["name"] == f"Daily Mix {number}":
        mix_id = i["id"]
        mix_desc = i["description"]
        break
else:
    print(f"Could not find Daily Mix {number} in followed playlists")
    quit()

res_tracks = requests.get(f"https://api.spotify.com/v1/playlists/{mix_id}/tracks", headers = headers)
restr_json = res_tracks.json()

uris = [i["track"]["uri"] for i in restr_json["items"]]

json = {
    "name": f"Daily Mix {number} | {datetime.date.today()}",
    "public": False,
    "description": mix_desc
}

res_newpl = requests.post(f"https://api.spotify.com/v1/users/{username}/playlists", headers = headers, json = json)
resnp_json = res_newpl.json()
newpl_id = resnp_json["id"]

new_songs = requests.post(f"https://api.spotify.com/v1/playlists/{newpl_id}/tracks", headers = headers, json = {"uris": uris})
if new_songs.ok:
    print("Successful")
else:
    print("Something went wrong")