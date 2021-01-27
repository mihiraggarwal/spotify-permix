import os
import sys
import json
import requests
import datetime
import subprocess
import spotipy.util as util

# Remove cache and username before committing

try:
    number = sys.argv[1]
except:
    number = int(input("Enter the number of the Daily Mix playlist which you want saved (1/2/3/4/5/6): "))

def kill():
    input('Press enter to exit.')
    subprocess.call(["taskkill","/F","/IM","permix.exe"])

f = open("username.txt", "r+")
rf = f.read()
if rf == "":
    try:
        user_uri = input("Enter your spotify uri: ").split(':')
        username = user_uri[2]
        f.write(username)
    except:
        print('Invalid spotify uri')
        kill()
else:
    username = rf

scope = 'playlist-read-private playlist-modify-private'
client_id = "a27eac5f72414c3190b565abd15eb2f1"

try:
    token = util.prompt_for_user_token(username, scope, client_id)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope, client_id)

headers = {"Authorization": f"Bearer {token}"}

try:
    res_playlists = requests.get(f'https://api.spotify.com/v1/users/{username}/playlists?limit=50', headers = headers)
except:
    print('Invalid spotify uri')
    kill()

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
    kill()

res_tracks = requests.get(f"https://api.spotify.com/v1/playlists/{mix_id}/tracks", headers = headers)
restr_json = res_tracks.json()

try:
    uris = [i["track"]["uri"] for i in restr_json["items"]]
except:
    print('Couldn\'t find any tracks')
    kill()

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
    print("Successful!")
else:
    print("Something went wrong")
input('Press enter to exit.')
    