import os
import sys
import json
import spotipy
import requests
import datetime
import configparser
import spotipy.util as util

# Remove cache and username before committing

config = configparser.ConfigParser()
config.read('config.ini')

SCOPE = 'playlist-read-private playlist-modify-private'
CLIENT_ID = "a27eac5f72414c3190b565abd15eb2f1"
CLIENT_SECRET = config["creds"]["CLIENT_SECRET"]

def kill():
    input('Press enter to exit.')
    sys.exit(0)

if __name__ == '__main__':
    try:
        try:
            number = sys.argv[1]
        except:
            number = int(input("Enter the number of the Daily Mix playlist which you want saved (1/2/3/4/5/6): "))

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

        try:
            token = util.prompt_for_user_token(username, SCOPE, CLIENT_ID, CLIENT_SECRET, redirect_uri='https://google.com/')
        except:
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, SCOPE, CLIENT_ID, CLIENT_SECRET, redirect_uri='https://google.com/')

        headers = {"Authorization": f"Bearer {token}"}

        try:
            res_playlists = requests.get(f'https://api.spotify.com/v1/users/{username}/playlists?limit=50', headers = headers)
        except:
            print('Invalid spotify uri')
            kill()

        if res_playlists.ok:
            respl_json = res_playlists.json()
        else:
            print('Couldn\'t get the playlists')
            kill()

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

        if res_tracks.ok:
            restr_json = res_tracks.json()
        else:
            print('Couldn\'t get the tracks')

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

        if res_newpl.ok:
            resnp_json = res_newpl.json()
        else:
            print('Couldn\'t create a new playlist')
        newpl_id = resnp_json["id"]

        new_songs = requests.post(f"https://api.spotify.com/v1/playlists/{newpl_id}/tracks", headers = headers, json = {"uris": uris})
        if new_songs.ok:
            print("Successful!")
        else:
            print("Something went wrong")
        input('Press enter to exit.')
        
    except:
        print('Something went wrong')
        input('Press enter to exit')
