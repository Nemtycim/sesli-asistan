import tkinter as tk
import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime
from googletrans import Translator
import calendar
import locale

locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.setProperty('voice', 'turkish')
    engine.say(text)
    engine.runAndWait()

def get_date_time():
    now = datetime.now()
    current_date = now.strftime("%d %B %Y")
    current_time = now.strftime("%H:%M")
    day_of_week = now.strftime("%A")

    return f"Bugün {current_date}, {day_of_week}. Saat {current_time}"


def get_time():
    current_time = datetime.now().strftime("%H:%M")
    return f"Şu an saat {current_time}"

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        main_weather = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        return f"{city} şehrinin hava durumu: {main_weather}, Sıcaklık: {temperature}°C"
    else:
        return f"Hava durumu bilgisi alınamadı. Hata Kodu: {response.status_code}"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sizi dinliyorum...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Ses analizi yapılıyor...")
        command = recognizer.recognize_google(audio, language="tr-TR")
        print("Anladım: " + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Anlamadım, tekrar deneyin.")
        return ""
    except sr.RequestError as e:
        print(f"Ses analizi hatası: {e}")
        return ""

def on_button_click():
    command = recognize_speech()

    if "selam" in command:
        saat = datetime.now().hour

        if saat >= 7 and saat < 12:
            speak("Günaydın size nasıl yardımcı olabilirim.")
            print("Selam Sorunun Cevabı -> Günaydın size nasıl yardımcı olabilirim. ")
        elif saat >= 12 and saat < 18:
            speak("İyi öğlenler size nasıl yardımcı olabilirim.")
            print("Selam Sorunun Cevabı -> İyi Öğlenler size nasıl yardımcı olabilirim. ")
        elif saat >= 18 and saat < 23:
            speak("İyi akşamlar size nasıl yardımcı olabilirim.")
            print("Selam Sorunun Cevabı -> İyi akşamlar size nasıl yardımcı olabilirim. ")

    elif "hava durumu" in command:
        speak("Hangi şehirin hava durumunu öğrenmek istersiniz?")
        city_command = recognize_speech()
        api_key = "669eb036ecac673b269c27c70b2d387d"
        weather_result = get_weather(api_key, city_command)
        speak(weather_result)
        print("Şuan ki hava durumu "+weather_result)

    elif "çevir" in command:
     speak("Hangi kelimeyi İngilizce'ye çevirmemi istersiniz?")
     text_to_translate = recognize_speech() 
     translator = Translator()
     translation = translator.translate(text_to_translate, dest="en")
     translated_text = translation.text
     speak(f"Çeviri: {translated_text}")
     print(f"Çeviri: {translated_text}")
 
    elif "takvim" in command:
        date_time = get_date_time()
        speak("Bugünün tarihi ve saati: "+date_time)
        print("Bugünün tarihi ve saati: "+date_time)

    elif "saat kaç" in command:
        current_time = get_time()
        speak(current_time)
        print("Saat Kaç Sorunun Cevabı : "+current_time)
    else:
        speak("Üzgünüm, anlamadım. Tekrar deneyin.")

root = tk.Tk()
root.title("Sesli Asistan")

button = tk.Button(root, text="Konuş", command=on_button_click)
button.pack(pady=20)

root.mainloop()

