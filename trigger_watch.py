import speech_recognition as sr
import os, sys, subprocess, jack

"""
List of words that should trigger the trigger script;
It's a good idea to include words that sound alike to deal
with some inaccuracy in recognition
"""
valid_triggers = ["record", "coral", "course", "forward", "recorded",
 "recording", "quarter", "accord", "court"]
transcription = ""

#Setup pocketsphinx objects
recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=6)

#Launch port configurer script
pc = subprocess.Popen([sys.executable, "port_configurer.py"])

while transcription != "quit":
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        transcription = recognizer.recognize_sphinx(audio)
    except sr.UnknownValueError:
        continue
    print(transcription)
    for word in transcription.split(" "):
        if word in valid_triggers:
            print("Triggered by \"" + transcription + "\"")
            command_file = open("trigger", "w")
            command_file.close()
            os.system("mv trigger trigger.file")

pc.kill()
