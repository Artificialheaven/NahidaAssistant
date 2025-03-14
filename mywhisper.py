import whisper


model = whisper.load_model("base")
result = model.transcribe("audios/0-0.mp3")
print(result["text"])