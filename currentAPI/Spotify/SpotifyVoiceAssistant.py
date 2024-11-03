import speech_recognition as sr
import sys
import controller as ct

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        print("Initializing microphone...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen_for_speech(self, prompt=None):
        if prompt:
            print(f"\n{prompt}")
        with self.mic as source:
            try:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: '{text}'")
                return text
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                print("Sorry, couldn't understand. Please try again.")
                return None
            except sr.RequestError as e:
                print(f"Connection error: {e}")
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
        print("\n🎵 Creating a new playlist...")

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
        print("\nPlaylist Details:")
        print(f"Name: {name}")
        print(f"Public: {'Yes' if is_public else 'No'}")
        print(f"Collaborative: {'Yes' if is_collaborative else 'No'}")
        if description:
            print(f"Description: {description}")
        print("Playlist created successfully!")

class SpotifyVoiceAssistant:
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.playlist_creator = PlaylistCreator()
        
    def show_help(self):
        """Display available commands"""
        print("\nAvailable commands:")
        print("• Play - Resume playback")
        print("• Pause - Pause playback")
        print("• Skip/Next - Play next track")
        print("• Previous/Go back - Play previous track")
        print("• Shuffle on/off - Toggle shuffle mode")
        print("• Repeat on/off - Toggle repeat mode")
        print("• Create - Start playlist creation")
        print("• Help - Show this help message")
        print("• Exit - Quit the program")

    def process_command(self, command):
        """Process voice commands for Spotify control"""
        try:
            if "play" in command:
                print("Playing")
                ct.playSong()
            
            elif "pause" in command:
                print("Paused")
                ct.pauseSong()
            
            elif "skip" in command or "next" in command:
                print("Skipping to next track")
                ct.skipSong()
            
            elif "previous" in command or "go back" in command:
                print("Playing previous track")
                ct.previousSong()
            
            elif "shuffle on" in command:
                print("Shuffle enabled")
                ct.shuffle(True)
            
            elif "shuffle off" in command:
                print("Shuffle disabled")
                ct.shuffle(False)
            
            elif "repeat on" in command:
                print("Repeat enabled")
                ct.repeat(True)
            
            elif "repeat off" in command:
                print("Repeat disabled")
                ct.repeat(False)
            
            elif "create" in command:
                print('playlist')
                playlist = self.playlist_creator.create_playlist()
            
            elif "help" in command:
                self.show_help()
            
            else:
                print("Unknown command. Say 'help' for available commands.")
        except Exception as e:
            print(f"Error processing command: {e}")

    def run(self):
        print("\nVoice-Controlled Spotify Assistant ")
        print("Say 'help' for available commands or 'exit' to quit.")
        
        while True:
            command = self.speech_handler.listen_for_speech()
            if not command:
                continue
            if "exit" in command:
                print("\nGoodbye!")
                sys.exit(0)
            else:
                self.process_command(command)

def main():
    assistant = SpotifyVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
