import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import wikipedia
import webbrowser
import datetime
import utils


voice_paulina = "com.apple.speech.synthesis.voice.paulina"
voice_monica = "com.apple.speech.synthesis.voice.monica"
voice_diego = "com.apple.speech.synthesis.voice.diego"
voice_jorge = "com.apple.speech.synthesis.voice.jorge"
voice_juan = "com.apple.speech.synthesis.voice.juan"

global chiste

def main():
    
    utils.limpiar()
    
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
        
        elif 'wikipedia' in pedido:
            talk('Con gusto, estoy buscando en Wikipedia')
            pedido = pedido.replace('wikipedia', '')
            pedido = pedido.replace('buscar', '')
            pedido = pedido.replace('en', '')
            
            try:
                wikipedia.set_lang('es')
                result = wikipedia.summary(pedido, sentences=1)
                talk(result)
            except:
                talk('Lo siento, no pude encontrar esa información')
            continue
        
        elif 'buscar en internet' in pedido or 'busca en internet' in pedido:
            talk('Con gusto, estoy en eso')
            pedido = limpiar_pedido(pedido)
                        
            try:
                pywhatkit.search(pedido)
                talk("He encontrado lo que buscabas")
            except:
                talk('Lo siento, no pude encontrar esa información')
            continue
        
        elif 'reproducir' in pedido:
            talk('Buena idea, estoy reproduciendo')
            pedido = limpiar_pedido(pedido)
            pywhatkit.playonyt(pedido)
            continue
        
        elif 'repetir broma' in pedido or 'repetir chiste' in pedido:
            talk(chiste)
            continue
        
        elif 'broma' in pedido or 'chiste' in pedido:
            chiste = pyjokes.get_joke('es')
            print(chiste)
            talk(chiste)
            continue
        
        elif 'precio de las acciones' in pedido:
            talk('Con gusto, estoy buscando')
            accion = pedido.split('de')[-1].strip()
            cartera = {
                'apple': 'AAPL',
                'microsoft': 'MSFT',
                'facebook': 'FB',
                'google': 'GOOGL',
                'amazon': 'AMZN',
                'netflix': 'NFLX',
                'uber': 'UBER',
                'tesla': 'TSLA',
                'coca-cola': 'KO'
            }
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                talk('El precio de ' + accion + ' es ' + str(precio_actual) + ' dólares')
            except:
                talk('Lo siento, no pude encontrar esa información')
            continue
        
        elif 'salir' in pedido:
            talk('Me voy a descansar, hasta pronto')
            break
    


def audio_to_text():
    r = sr.Recognizer()
    
    # Configurar microfono
    with sr.Microphone() as source:
        utils.limpiar()
        r.pause_threshold = 1
        print("Diga algo: ")
        print("- Abrir YouTube")
        print("- Abrir Google")
        print("- Qué día es hoy")
        print("- Qué hora es")
        print("- Buscar en Wikipedia")
        print("- Buscar en Internet")
        print("- Reproducir en YouTube")
        print("- Contar chiste")
        print("- Repetir chiste")
        print("- Precio de las acciones")
        print("- Salir")
        
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
    
    # Traducir mes
    mes = int(today.month)
    mes_ok = utils.get_mes(mes)
    
    talk(f'Hoy es {calendar[day_of_week]} {today.day} de {mes_ok}')
    
    
def speak_time():
    hour = datetime.datetime.now()
    hour = f'Son las {hour.hour} y {hour.minute}' 
    talk(hour)


def limpiar_pedido(pedido):
    pedido = pedido.replace('buscar en internet', '')
    pedido = pedido.replace('busca en internet', '')
    pedido = pedido.replace('paulina', '')
    pedido = pedido.replace('buenos días', '')
    pedido = pedido.replace('buenas tardes', '')
    pedido = pedido.replace('buenas noches', '')
    pedido = pedido.replace('buenas hola', '')
    pedido = pedido.replace('por favor', '')
    
    return pedido


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
