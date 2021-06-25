import speech_recognition as sr

def voice_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        text = "No_Audio"

    return text
