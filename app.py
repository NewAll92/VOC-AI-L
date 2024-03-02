from flask import Flask, render_template
import speech_recognition as sr
import g4f
from g4f.Provider import You
from elevenlabs import generate, play, set_api_key
from screen_brightness_control import set_brightness, get_brightness
from AppOpener import open
import sys
import pyautogui


set_api_key("eda8a2c383db6485d14e2dc178626140")

app = Flask(__name__)

engine = None  

def speak(texte):
    audio = generate(
    text= texte,
    voice="Arnold",
    model="eleven_multilingual_v1"
    )
    play(audio)


r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='fr-FR')
        print("Vous avez dit : " + text)
        return text
    except Exception as e:
        print("Erreur de reconnaissance vocale : " + str(e))
        return None

def generate_response(prompt):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=You,
        messages=[{"role": "user", "content": prompt}],
    )
    return response


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/run_code', methods=['POST'])
def run_code():
    prompt = listen()
    result = None
    if prompt == "au revoir":
        print("Au revoir !")
        speak("Au revoir !")
    
    
    elif 'augmente la luminosité' in prompt or 'monte la luminosité' in prompt :
        speak("OK, j'augmente la luminosité")
        set_brightness("+25")
    
    elif 'baisse la luminosité' in prompt :
        speak("OK, je baisse la luminosité")
        set_brightness("-25")

    elif 'monte la luminosité au max' in prompt or 'monte la luminosité au maximum' in prompt or 'mets la luminosité au maximum' in prompt:
        speak('OK, je mets la luminosité au maximum')
        set_brightness(100)
        print(prompt)

    elif 'ouvre ' in prompt or "lance" in prompt or "démarre" in prompt:
        prompt = prompt.replace("ouvre", "").replace("lance", "").replace("démarre", "")
        speak(f" OK, j'ouvre" + prompt)
        [open(prompt, match_closest=True)]

    elif 'monte le son' in prompt or "augmente le son" in prompt:
        speak("OK, je monte le son.")
        for _ in range(12):
            pyautogui.press("volumeup")

    elif 'baisse le son' in prompt or "diminue le son" in prompt:
        speak("OK, je baisse le son.")
        for _ in range(12):
            pyautogui.press("volumedown")

    elif 'coupe le son' in prompt or "mute le son" in prompt:
            pyautogui.press("volumemute")
    
    elif 'remets le son' in prompt or 'réactive le son' in prompt:
            pyautogui.press("volumeup")

    else:
        speak("Une seconde...")
        response = generate_response(prompt)

        if "code Python" in response:
            print(response)
            speak('Bien sûr ! Je vous imprime la réponse.')
            result = response
        else:
            speak(response)
            result = response
            

    return render_template('index.html', result=result)
    
if __name__ == '__main__':
    app.run(debug=True)