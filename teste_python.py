import whisper
import os

modelo = whisper.load_model("base")
#resposta = modelo.transcribe(".\minha_voz.mp3")
print(os.listdir())
#print(resposta['text'])