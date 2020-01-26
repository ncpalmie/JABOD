import speech_recognition as sr
import subprocess, jack

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=6)
transcription = ""

#Launch port configurer script
pc = subprocess.Popen([sys.executable, "port_configurer.py"])

while transcription != "quit":
    print("Listening")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    transcription = recognizer.recognize_sphinx(audio)
    print(transcription)
    print("Not Listening")

pc.kill()
