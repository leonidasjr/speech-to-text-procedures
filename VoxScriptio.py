import os
import speech_recognition as sr
from pydub import AudioSegment
from tkinter import Tk, Label, Button, StringVar, OptionMenu, filedialog, Toplevel

def transcribe_audio():
    # Initialize Tkinter root
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select folder
    folder_path = filedialog.askdirectory(title="Select a folder containing audio files")
    
    if not folder_path:
        print("No folder selected")
        root.destroy()
        return

    # Create a new window for language selection
    language_window = Toplevel(root)
    language_window.title("Language options")
    language_window.geometry("280x100")  # Set window size

    # Language options
    language_var = StringVar(language_window)
    language_var.set("----")  # default value

    languages = {
        "American English (en-US)": "en-US",
        "Brazilian Portuguese (pt-BR)": "pt-BR",
        "British English (en-GB)": "en-GB",
        "Irish English (en-IE)": "en-IE",
    }
    
    Label(language_window, text="Select the audio language:").pack()
    OptionMenu(language_window, language_var, *languages.keys()).pack()

    def on_language_select():
        selected = language_var.get()
        if selected == "----":
            print("No language selected")
            return

        language = languages[selected]
        language_window.destroy()

        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Loop through all audio files in the selected folder
        for audio_file_name in os.listdir(folder_path):
            audio_file_path = os.path.join(folder_path, audio_file_name)
            
            if not audio_file_path.endswith(('.wav', '.mp3', '.flac', '.ogg')):
                continue  # Skip non-audio files
            
            # Convert audio file to WAV format if necessary
            if not audio_file_path.endswith('.wav'):
                audio = AudioSegment.from_file(audio_file_path)
                audio_file_path = audio_file_path.rsplit('.', 1)[0] + '.wav'
                audio.export(audio_file_path, format='wav')
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
            
            # Recognize speech using Google Web Speech API
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                
                print("")
                print('=======')
                print(f"Transcribed Text for {audio_file_name}:")
                print(text)
                print('=======')
                
                text_file_name = os.path.splitext(audio_file_name)[0] + ".txt"
                save_path = os.path.join(folder_path, text_file_name)
                
                with open(save_path, 'w') as file:
                    # file.write(f"Audio File: {audio_file_name}\n\n")
                    file.write(text)
                
                print(f"Transcription saved successfully as {text_file_name}.")
            except sr.UnknownValueError:
                print(f"Google Web Speech API could not understand the audio for {audio_file_name}")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API for {audio_file_name}; {e}")

        print("")
        print("------------")
        print("Script ended")

        # Cleanly exit Tkinter and return control to terminal
        root.destroy()

    Button(language_window, text="OK", command=on_language_select).pack()
    root.mainloop()

# Example usage
transcribe_audio()