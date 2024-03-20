import os
import requests
from tempfile import NamedTemporaryFile
from gtts import gTTS
import pygame
import asyncio

def play_mp3(file_path):
    # Initiate pygame and play the audio.    
    pygame.init()
    pygame.mixer.init()
    audio = pygame.mixer.Sound(file_path)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Determine the duration of the audio file
    audio_duration = audio.get_length()
    # Set a small buffer for ticking
    tick_buffer = 0.5
    
    # Wait until the audio has finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(audio_duration + tick_buffer)

def text2speech(text):
    # Create a named temporary file instead of a generic temporary file
    with NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        tts = gTTS(text=text, lang='en', slow=False, tld="co.uk")
        tts.save(f.name)  # Save the TTS output to the temporary file

    play_mp3(f.name)
    # Delete the temporary file after the audio has finished playing
    os.remove(f.name)

def text2unreal_speech(text):
    headers = None
    json = {
    'Text': text, # Up to 1000 characters
    'VoiceId': 'Liv', # Dan, Will, Scarlett, Liv, Amy
    'Bitrate': '192k', # 320k, 256k, 192k, ...
    'Speed': '0', # -1.0 to 1.0
    'Pitch': '1', # -0.5 to 1.5
    'Codec': 'libmp3lame', # libmp3lame or pcm_mulaw
    }

    response = requests.post('https://api.v6.unrealspeech.com/stream', headers=headers, json=json)

    with NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(response.content)
        
    play_mp3(f.name)
    # Delete the temporary file after the audio has finished playing
    os.remove(f.name)
    
if __name__ == "__main__":
    # Test the module when running as a script.
    test_text = 'Hello! This is a test of text2speech.'

    text2speech(test_text)



