"""
A program that automatically generates a playlist with the top 10 songs by artists specified by the user
"""

import config
import spotipy
import spotipy.util as util


def find_newest_playlist(username, playlist_name):
    playlists = sp.user_playlists(username, limit=50)   # list of 50 playlists
    for i, item in enumerate(playlists['items']):
        if item['name'] == playlist_name:           # if playlist name matches
            uri = item['uri']                       # get playlist ID

    return uri


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
        sp.user_playlist_create(user=username, name=p_name, public=False, description='')   # create new playlist

        p_id = find_newest_playlist(username, p_name)       # get ID of previously created playlist

        artists = input("Whose top 10 song do you want to add to your playlist?\n"
                        "Please separate multiple artists by comma.\n").split(", ")

        tracks = []
        for a in artists:
            result = sp.search(a, limit=1, type='artist')
            artist_uri = result['artists']['items'][-1]['uri']      # get IDs of each artist
            top_tracks = sp.artist_top_tracks(artist_uri)  # default country: US; maybe change to Germany

            for i in top_tracks['tracks']:
                tracks.append(i['uri'])     # get ID of each song

        sp.user_playlist_add_tracks(user=username, playlist_id=p_id, tracks=tracks)     # add songs to playlist

    else:
        print("Can't get token for", username)
