import speech_recognition as sr
import controller as ct
import sys

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        print("Initializing microphone...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen_for_speech(self, prompt=None):
        if prompt:
            print(f"\n {prompt}")
        with self.mic as source:
            try:
                print(" Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: '{text}'")
                return text
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                print(" Sorry, couldn't understand. Please try again.")
                return None
            except sr.RequestError as e:
                print(f" Connection error: {e}")
                return None

    def get_yes_no(self, prompt):
        while True:
            response = self.listen_for_speech(prompt + " Say 'yes' or 'no'.")
            if response in ["yes", "no"]:
                return response == "yes"
            print("Please respond with 'yes' or 'no'.")

class PlaylistCreator:
    def __init__(self):
        self.speech_handler = SpeechHandler()

    def create_playlist(self):
        print("\n Creating a new playlist...")

        # Get and confirm the playlist name
        while True:
            name = self.speech_handler.listen_for_speech("What name would you like for your playlist?")
            if name and self.speech_handler.get_yes_no(f"You said '{name}'. Is that correct?"):
                break

        # Get public and collaborative settings
        is_public = self.speech_handler.get_yes_no("Should the playlist be public?")
        is_collaborative = self.speech_handler.get_yes_no("Should the playlist be collaborative?")
        
        # Get description if wanted
        description = ""
        if self.speech_handler.get_yes_no("Would you like to add a description?"):
            description = self.speech_handler.listen_for_speech("Please say your description") or ""

        # Show and confirm the playlist details
        print("\n Playlist Details:")
        print(f" Name: {name}")
        print(f" Public: {'Yes' if is_public else 'No'}")
        print(f" Collaborative: {'Yes' if is_collaborative else 'No'}")
        if description:
            print(f" Description: {description}")
        print(" Playlist created successfully!")
        if description:
            ct.createPlaylist(name,is_public,is_collaborative, description)
        else:
            ct.createPlaylist(name,is_public,is_collaborative)

class SpotifyVoiceAssistant:
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.playlist_creator = PlaylistCreator()
        
    def show_help(self):
        """Display available commands"""
        print("\n Available commands:")
        print("• Play - Resume playback")
        print("• Pause - Pause playback")
        print("• Skip/Next - Play next track")
        print("• Previous/Go back - Play previous track")
        print("• Shuffle on/off - Toggle shuffle mode")
        print("• Repeat on/off - Toggle repeat mode")
        print("• Create - Start playlist creation")
        print("• Help - Show this help message")
        print("• Exit - Quit the program")
        # new additions
        print("• Volume up - Raise the volume")
        print("• Volume down - Lower the volume")
        print("• Mute - Mute the volume")
        print("• Max volume - Set volume to the maximum")
        print("• Add current song to playlist - Add the currently playing song to a playlist")
        print("• Add previous song to playlist - Add the previously played song to a playlist")
        print("• Play playlist - Play a specified playlist")
        print("• Advance - Jump to a specific time in the current track")

    def process_command(self, command):
        """Process voice commands for Spotify control"""
        try:
                
            if "play playlist" in command:
                playlist_name = self.speech_handler.listen_for_speech("Please say the name of the playlist you want to play.")
                if playlist_name:
                    print(f" Playing playlist: {playlist_name}")
                    ct.playPlaylist(playlist_name)
                else:
                    print(" Could not recognize the playlist name. Please try again.")
                # ct.playPlaylist(playlist_name)
                
            elif "pause" in command:
                print(" Paused")
                ct.pauseSong()
            
            elif "skip" in command or "next" in command:
                print(" Skipping to next track")
                ct.skipSong()
            
            elif "add" in command and "previous" in command:
                name = self.speech_handler.listen_for_speech("What playlist do you want to add to? ")
                if name:
                    print(f" Adding to {name}")
                    ct.addPreviousSongToPlaylist(name)
                else:
                    print(" Could not recognize the playlist name. Please try again.")
                
            elif "add" in command and "current" in command:
                name = self.speech_handler.listen_for_speech("What playlist do you want to add to? ")
                if name:
                    print(f" Adding to {name}")
                    ct.addCurrentSongToPlaylist(name)
                else:
                    print(" Could not recognize the playlist name. Please try again.")
                
            elif "previous" in command or "go back" in command:
                print(" Playing previous track")
                ct.previousSong()
            
            elif "shuffle on" in command:
                print(" Shuffle enabled")
                ct.shuffle(True)
            
            elif "shuffle off" in command:
                print(" Shuffle disabled")
                ct.shuffle(False)
            
            elif "repeat" in command:
                print(" Repeating song")
                ct.repeat('')
            
            elif "repeat song" in command:
                print(" Repeating song")
                ct.repeat('song')
            
            elif "repeat playlist" in command:
                print(" setting playlist to repeat")
                ct.repeat('playlist')
            
            elif "create" in command:
                print('playlist')
                self.playlist_creator.create_playlist()
                
            elif "volume up" in command:
                print(" raising volume")
                ct.volumeUp()
                
            elif "volume down" in command:
                print(" lowering volume")
                ct.volumeDown()
            
            elif "mute" in command:
                print(" mute")
                ct.mute()
            
            elif "max volume" in command:
                print(" Setting max volume.")
                ct.maxVolume()
                
            elif "advance" in command:
                seek_time = self.speech_handler.listen_for_speech("What time do you want to advance/seek to? ")
                print(f" Seeking to {seek_time}")
                ct.seekTo(int(seek_time))
                
            elif "play" in command:
                print(" Playing")
                ct.playSong()
            
            elif "help" in command:
                self.show_help()
            
            else:
                print(" Unknown command. Say 'help' for available commands.")
        except Exception as e:
            print(f" Error processing command: {e}")

    def run(self):
        print("\n Voice-Controlled Spotify Assistant ")
        print("Say 'help' for available commands or 'exit' to quit.")
        
        while True:
            command = self.speech_handler.listen_for_speech()
            if not command:
                continue
            if "exit" in command:
                print("\n Goodbye!")
                sys.exit(0)
            else:
                self.process_command(command)

def main():
    assistant = SpotifyVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
