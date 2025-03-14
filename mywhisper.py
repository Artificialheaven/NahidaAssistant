import whisper

model = whisper.load_model("base")


def transcribe(file):
    result = model.transcribe(file)
    return result["text"]
