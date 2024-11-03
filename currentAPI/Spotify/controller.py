import spotipy
from spotipy.oauth2 import SpotifyOAuth

'''!!!! REMOVE BEFORE SENDING OR SAVING !!!!'''
#did
#c_id
#c_secret
#uid
'''!!!! REMOVE BEFORE SENDING OR SAVING !!!!'''

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=c_id,
    client_secret=c_secret,
    redirect_uri="http://localhost:1508",
    scope="user-modify-playback-state user-read-playback-state playlist-modify-private playlist-modify-public"))

def info():
    #stuff = sp.current_playback(market=None, additional_types=None)
    stuff = sp.current_user_playing_track()
    for thing in stuff:
        print(thing)
        if type(stuff[thing]) == dict:
            for i in stuff[thing]:
                print(i, "\n", stuff[thing][i])
        else:
            print(stuff[thing])
        print()

def playSong():
    try:
        sp.start_playback(device_id=did)
    except:
        return 0
    return 1

def pauseSong():
    try:
        sp.pause_playback(device_id=did)
    except:
        return 0
    return 1

def skipSong():
    try:
        sp.next_track(device_id=did)
    except:
        return 0
    return 1

def previousSong():
    try:
        sp.previous_track(device_id=did)
    except:
        return 0
    return 1

def shuffle(state):
    try:
        sp.shuffle(state, device_id=did)
    except:
        return 0
    return 1

def repeat(state):
    try:
        if state:
            sp.repeat("track", device_id= did)
        else:
            sp.repeat("off", device_id=did)
    except:
        return 0
    return 1

def seekTo(time):
    try:
        sp.seek_track(position_ms=time, device_id=did)
    except:
        return 0
    return 1

def createPlaylist(name, isPublic=False, isCollab=False, desc=""):
    try:
        sp.user_playlist_create(uid, name, isPublic, isCollab, desc)
    except:
        return 0
    return 1



def main():
    print("Spotify is working")

if __name__ == "__main__":
    main()

    



''' The fun stuff
user-read-playback-state   app-remote-control   streaming
sp.me()
shuffle(state, device_id=None)
seek_track(position_ms, device_id=None)
repeat(state, device_id=None)
previous_track(device_id=None)
next_track(device_id=None)
pause_playback(device_id=None)
current_playback(market=None, additional_types=None)
current_user_playing_track()
start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)
devices()
search(q, limit=10, offset=0, type='track', market=None)
transfer_playback(device_id, force_play=True)

'''