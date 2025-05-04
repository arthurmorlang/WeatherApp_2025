import tkinter as tk #GUI Bib
from PIL import Image, ImageTk
import requests
import time
from io import BytesIO
import datetime
import locale
import os
from dotenv import load_dotenv



def getWeather(fenster):
    city = textInput.get()
    load_dotenv()
    
    API_key = os.getenv('API_key')
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    
    locale.setlocale(locale.LC_TIME, "de_DE")
    jetzt = datetime.datetime.now()
    test_time = jetzt.strftime('%A, %d.%B.%Y, %H:%M')
    print(test_time)

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main'] #holt erstes Objekt aus Json "Array" Liste
    temp = int(json_data['main']['temp'] - 273.15) #normales Json Objekt kein [0] notwendig
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    feels = int(json_data['main']['feels_like'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    windspeed = int(json_data['wind']['speed'] * 3.6 )
    sunrise = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunrise'] + 7200))
    sunset = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunset'] + 7200))
    icon_code = json_data['weather'][0]['icon']
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png" #f um {} als Variable zu erkennen    
    response = requests.get(icon_url)
    img_data = response.content
    
    pil_image = Image.open(BytesIO(img_data))
    tk_image = ImageTk.PhotoImage(pil_image)
    canvas_icon.create_image(50,50, image = tk_image)
    canvas_icon.image = tk_image
    
    weather_translation = { #Dictionary für Zuordnung
        "Clear": "Klarer Himmel",
        "Rain": "Regen",
        "Clouds": "Bewölkt",
        "Haze": "Dunst",
        "Snow": "Schnee",
        "Mist": "feiner Nebel",
        "Drizzle": "Nieselregen",
        "Thunderstorm": "Gewitter",
        "Fog": "Nebel",
        "Smoke": "Rauch",
        "Sand": "Sand in der Luft",
        "Ash": "Asche in der Luft",
        "Tornado": "Tornado Gefahr",
        "Squall": "Sturmböen"
    }
    
    translated_condition = weather_translation.get(condition)
    final_info = translated_condition + "\n" + str(temp) + "°C" 
    final_data = "\n" + str(test_time) + "\n" + "Gefühlt: " + str(feels) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" + "\n" + "Min Temp: " + str(min_temp) + "°C" + "\n" + "Luftdruck: " + str(pressure) + "hPa" + "\n" + "Feuchtigkeit: " + str(humidity) + "%" + "\n" + "Windspeed: " + str(windspeed) + " km/h" + "\n" + "Sonnenaufgang: " + str(sunrise) + "\n" + "Sonnenuntergang: " + str(sunset)
    label1.config(text = final_info)
    label2.config(text = final_data)



fenster = tk.Tk() #erstellt das Hauptfenster
fenster.geometry("600x500")
fenster.title("Wetter APP")

f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")
textInput = tk.Entry(fenster, font = f)
textInput.pack(pady = 20) #Padding in Y-Axis
textInput.focus()
textInput.bind('<Return>', getWeather) #Wenn Enter -> getWeather func Aufruf.. Fenster wird zu Event-Objekt

#DATA präsentieren
canvas_icon = tk.Canvas(fenster, width= 100, height= 100)
canvas_icon.pack()

label1 = tk.Label(fenster, font = t) #Label is a basic Textfield
label1.pack() #pack -> Visibility

label2 = tk.Label(fenster, font = f)
label2.pack()

fenster.mainloop()

