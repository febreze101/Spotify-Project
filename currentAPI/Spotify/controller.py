import spotipy
from spotipy.oauth2 import SpotifyOAuth

'''!!!! REMOVE BEFORE SENDING OR SAVING !!!!'''

'''!!!! REMOVE BEFORE SENDING OR SAVING !!!!'''

'''
Function returns:
1 = successful
0 = no change (already in state)
-1 = critical error (currenly outside of control)
-2 = option not supported (currently only used in volume control)
'''

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=c_id,
    client_secret=c_secret,
    redirect_uri="http://localhost:1508",
    scope="user-modify-playback-state user-read-playback-state playlist-modify-private playlist-modify-public"))

def info():
    #stuff = sp.current_playback(market=None, additional_types=None)
    stuff = sp.current_playback()
    for thing in stuff:
        print(thing)
        if type(stuff[thing]) == dict:
            for i in stuff[thing]:
                print(i, "\n", stuff[thing][i])
        else:
            print(stuff[thing])
        print()

def playSong():
    if 'resuming' not in sp.current_playback()['actions']['disallows']:    
        try:
            sp.start_playback(device_id=did)
        except:
            return -1
        return 1
    return 0

def pauseSong():
    if 'pausing' not in sp.current_playback()['actions']['disallows']:
        try:
            sp.pause_playback(device_id=did)
        except Exception as e:
            print ("\n",e, "\n")
            return -1
        return 1
    return 0

def skipSong():
    if 'skipping_next' not in sp.current_playback()['actions']['disallows']:
        try:
            sp.next_track(device_id=did)
        except:
            return -1
        return 1
    return 0

def previousSong():
    if 'skipping_previous' not in sp.current_playback()['actions']['disallows']:
        try:
            sp.previous_track(device_id=did)
        except:
            return -1
        return 1
    return 0

def shuffle(state):
    if state != sp.current_playback()['shuffle_state']:
        try:
            sp.shuffle(state, device_id=did)
        except:
            return -1
        return 1
    return 0

def repeat(state):
    if state != sp.current_playback()['repeat_state']:
        try:
            if state:
                sp.repeat("track", device_id= did)
            else:
                sp.repeat("off", device_id=did)
        except:
            return -1
        return 1
    return 0

def seekTo(time):
    try:
        sp.seek_track(position_ms=time*1000, device_id=did)
    except:
        return 0
    return 1

def volumeUp():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        try:
            if temp['volume_percent'] > 89:
                sp.volume(100)
                return 1
            elif temp['volume_percent'] == 100:
                return 0
            else:
                sp.volume(temp['volume_percent']+10)
                return 1
        except:
            return -1
    print("Current device doesn't support volume control")
    return -2

def volumeDown():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        try:
            if temp['volume_percent'] < 11:
                sp.volume(0)
                return 1
            elif temp['volume_percent'] == 0:
                return 0
            else:
                sp.volume(temp['volume_percent']-10)
                return 1
        except:
            return -1
    print("Current device doesn't support volume control")
    return -2

def mute():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        if temp['volume_percent'] != 0:    
            try:
                sp.volume(0)
                return 1
            except:
                return -1
        return 0
    print("Current device doesn't support volume control")
    return -2

def maxVolume():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        if temp['volume_percent'] != 100:    
            try:
                sp.volume(100)
                return 1
            except:
                return -1
        return 0
    print("Current device doesn't support volume control")
    return -2

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
