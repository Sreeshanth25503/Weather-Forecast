import requests
from geopy.geocoders import Nominatim
from tkinter import Tk, Label, Button

# WeatherAPI key
API_KEY = 'f999b83bd93b4b5fb87170000242209'
BASE_URL = 'http://api.weatherapi.com/v1/current.json?'

def get_location():
    geolocator = Nominatim(user_agent="weather_app")
    try:
        ip_info = requests.get('https://ipinfo.io').json()  # Fetch location using IP
        location = geolocator.reverse(f"{ip_info['loc']}")  # Convert to city name
        return location.raw['address']['city'], ip_info['loc']  # Return city name
    except Exception as e:
        return None, None

def get_weather(city):
    try:
        complete_url = BASE_URL + f"key={API_KEY}&q={city}"
        response = requests.get(complete_url)
        print(response.json()) 
        
        data = response.json()

        if 'error' not in data:
            current = data['current']
            temp_c = current['temp_c']
            feels_like_c = current['feelslike_c']
            condition = current['condition']['text']
            
            return (f"Temperature: {temp_c}°C\n"
                    f"Feels Like: {feels_like_c}°C\n"
                    f"Condition: {condition}")
        else:
            return "City Not Found or Invalid API Key"
    except Exception as e:
        return "Error fetching weather data."

def display_weather():
    city, loc = get_location()
    if city:
        weather_info = get_weather(city)
        weather_label.config(text=f"Location: {city}\n\n{weather_info}")
    else:
        weather_label.config(text="Unable to determine location")

root = Tk()
root.title("Weather Forecast")
root.geometry("300x200")

label = Label(root, text="Real-Time Weather Forecast", font=("Helvetica", 14))
label.pack(pady=10)

weather_label = Label(root, text="Click below to get weather", font=("Helvetica", 12))
weather_label.pack(pady=10)

fetch_button = Button(root, text="Get Weather", command=display_weather)
fetch_button.pack(pady=10)

root.mainloop()
