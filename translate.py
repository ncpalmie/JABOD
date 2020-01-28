#Below code was taken from Google's Speech-To-Text python guides
#https://cloud.google.com/speech-to-text/docs/
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = "speech.wav"

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    language_code='en-US',
    audio_channel_count=2)

# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    out_file = open("voice_cmd", "w")
    out_file.write('Transcript: {}'.format(result.alternatives[0].transcript))
    out_file.close()
    os.system("mv voice_cmd voice_cmd.txt")
    print('Transcript: {}'.format(result.alternatives[0].transcript))
