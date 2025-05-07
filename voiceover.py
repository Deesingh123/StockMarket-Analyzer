from gtts import gTTS

def generate_voice_report(text: str, filename="report.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename