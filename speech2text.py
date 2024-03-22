import speech_recognition as sr

r = sr.Recognizer()

def listen():
    # obtain audio from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    return audio

def speech2text(audio):
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        text = r.recognize_google(audio)
        print("Text: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # TODO Add logic to ensure text is returned.
    return text

if __name__ == "__main__":
    audio = listen()
    speech2text(audio)
