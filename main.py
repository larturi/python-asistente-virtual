import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import wikipedia
import webbrowser
import datetime

voice_paulina = "com.apple.speech.synthesis.voice.paulina"
voice_monica = "com.apple.speech.synthesis.voice.monica"
voice_diego = "com.apple.speech.synthesis.voice.diego"
voice_jorge = "com.apple.speech.synthesis.voice.jorge"
voice_juan = "com.apple.speech.synthesis.voice.juan"

def main():
    # Saludo inicial
    welcome()
    
    comenzar = True
    
    while comenzar:
        # activar el microfono y guardar el pedido en string
        pedido = audio_to_text().lower()
                
        if 'abrir youtube' in pedido or 'abrir iutub' in pedido:
            talk('Con gusto, estoy abriendo Youtube')
            webbrowser.open("https://youtube.com")
            continue
        
        elif 'abrir google' in pedido or 'abrir guguel' in pedido:
            talk('Con gusto, estoy abriendo Google')
            webbrowser.open("https://google.com")
            continue
        
        elif 'qué día es hoy' in pedido:
            speak_day_off_week()
            continue
        
        elif 'qué hora es' in pedido:
            speak_time()
            continue
        
        elif 'Jajaja' in pedido:
            talk('De que te ries?')
            continue


def audio_to_text():
    r = sr.Recognizer()
    
    # Configurar microfono
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Diga algo: ")
        
        audio = r.listen(source)
        
        try:
            solicitud = r.recognize_google(audio, language="es-AR")
            print("Tu dijiste: " + solicitud)
            return solicitud
        except sr.UnknownValueError:
            print("Lo siento, no te entendi")
            return "Sigo esperando"
        except sr.RequestError as e:
            print("No se puede conectar al servicio de Google Speech Recognition")
            return "Sigo esperando"
        except:
            print("Ups, algo salio mal")
            return "Sigo esperando"
    
        
def talk(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_paulina)
    engine.say(text)
    engine.runAndWait()
        
     
def check_voices():
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        print(voice)


def speak_day_off_week():
    today = datetime.date.today()
    day_of_week = today.weekday()
    
    calendar = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }
    
    talk(f'Hoy es {calendar[day_of_week]}')
    
    
def speak_time():
    hour = datetime.datetime.now()
    hour = f'Son las {hour.hour} y {hour.minute}' 
    talk(hour)


def welcome():    
    hora = datetime.datetime.now()
    
    if hora.hour < 12:
        momento = "Buenos días"
    elif hora.hour >= 12 and hora.hour < 19:
        momento = "Buenas tardes"
    else:
        momento = "Buenas noches"
        
    saludo = f"{momento}, soy Paulina, tu asistente personal. ¿Qué puedo hacer por ti?"
    
    talk(saludo)



main()
