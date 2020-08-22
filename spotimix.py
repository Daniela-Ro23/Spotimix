"""
A program that automatically generates a playlist with random songs from specified artists

- which library: spotipy or pyfy?
- how to authenticate user: config file?
- how to present: commands only or screen input?
- how to get user specifications: config file or command line?
- if with config file, then just run file!
- if I want simple use for other people, screen input!
- consider multiple options: playlists based on artists, mix several playlists etc
- present selection of options (eg. press 1 for..., 2 for...)
- additional idea: ask if user wants to add songs by related artists
- additional idea: give possibility of adding all songs of an artist or a number
- additional idea: add songs from artist's top songs only (all - some random songs - some top songs)
"""

import config
import argparse
import re
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


# user ID: Nvcvfjs5SfmMnvQk7PGkDg

def find_newest_playlist(username, playlist_name):
    playlists = sp.user_playlists(username, limit=50)

    for i, item in enumerate(playlists['items']):
        if item['name'] == playlist_name:
            uri = item['uri']

    return uri

    #matching_playlists = []
    #for i, item in enumerate(playlists['items']):
    #    if re.search(playlist_pattern, item['name']):
    #        matching_playlists.append((item['uri'], item['name']))
    #if matching_playlists:
    #    matching_playlists.sort(key=lambda tup: tup[1])
    #    return matching_playlists[-1]
    #return None, None


if __name__ == "__main__":

    username = config.username
    client_id = config.client_id
    client_secret = config.client_secret

    token = util.prompt_for_user_token(username=username,
                                       scope='playlist-modify-public playlist-modify-private playlist-read-private',
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri='http://localhost/')

    print('Welcome to Spotimix!')
    p_name = input('Enter a name for your new playlist:\n')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.user_playlist_create(user=username, name=p_name, public=False, description='')

        p_id = find_newest_playlist(username, p_name)

        artists = input("Whose top 10 song do you want to add to your playlist?\n"
                        "Please separate multiple artists by comma.\n").split(", ")

        tracks = []
        for a in artists:
            result = sp.search(a, limit=1, type='artist')
            artist_uri = result['artists']['items'][-1]['uri']
            top_tracks = sp.artist_top_tracks(artist_uri)  # default country: US; maybe change to Germany

            for i in top_tracks['tracks']:
                tracks.append(i['uri'])

        sp.user_playlist_add_tracks(user=username, playlist_id=p_id, tracks=tracks)


    else:
        print("Can't get token for", username)

    #parser = argparse.ArgumentParser()
    #parser.add_argument('playlist', 'p', metavar='P', type=str, nargs='+', required=True,
       #                 help='name of the new playlist')
    #parser.add_argument('artists', 'a', metavar='A', type=list, nargs='+', required=True,
      #                  help='list of artists')
    #parser.add_argument('--mode', '-m', choices=['all', 'rand', 'top'], default='rand',
     #                   help='choose whether to add all songs, some random songs or some top songs by this artist')
    #parser.add_argument('--number', '-n',
        #                help='number of songs from this artist')

    #args = parser.parse_args()



    # dic_list = []
    #
    # print('Welcome to Spotimix!')
    # p_name = input('Enter a name for your new playlist:\n')
    # cont = True
    # while cont:
    #     artists = input('Enter the artist, mode and number of songs, separated by comma:\n').split(', ')
    #     d = {'name': artists[0],
    #          'mode': artists[1],
    #          'num': artists[2]}
    #     dic_list.append(d)
    #
    #     next_artist = input('Do you want to add songs by another artist? y/n\n')
    #     if next_artist == "n":
    #         cont = False
    # print(dic_list)
