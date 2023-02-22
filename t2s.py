import pyttsx3
import os
from pydub import AudioSegment
from pydub.utils import which
from tqdm import tqdm
import shutil

engine = pyttsx3.init()
AudioSegment.converter = which("ffmpeg")

name = input("Enter the name of the text file in this folder\n")
rate = input("Enter the speed of narration (recomended between 125 and 150)\n")
print("Enter the narration voice")
voices = engine.getProperty('voices')
for i in range(len(voices)):
    print(str(i) + ": " + voices[i].name)
voice = input()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[int(voice)].id)
engine.setProperty('rate', int(rate))


text = open(name, encoding='utf-8', mode='r').read()

if os.path.exists("tmp"):
    shutil.rmtree('tmp')
    
os.mkdir("tmp")

print("processing text")

paragraphs = text.split("\n\n")
for i in tqdm(range(len(paragraphs))):
    engine.save_to_file(paragraphs[i], "tmp/" + str(i) + ".wav")
    engine.runAndWait()

print("combining files")

result = None
paths = os.listdir('tmp')
for i in tqdm(range(len(paragraphs))):
    try:
        sound = AudioSegment.from_file("tmp/" + paths[i])
        if len(sound) > 0.1:
            if result == None:
                result = sound
            else:
                result = result.append(sound)
    except:
        pass

if result == None:
    raise Exception("Something wen't wrong!")

result.export("result.mp3", format="mp3")

try:
    shutil.rmtree('tmp')
except:
    pass

input("Done! Press enter to exit")