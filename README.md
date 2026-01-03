# Weather Forecast App

A clean and modern desktop weather application built with Python and CustomTkinter. Get real-time weather updates for any city in the world with a beautiful, easy-to-use interface.

## What This App Does

This is a simple weather app that shows you current weather conditions for any location. It automatically detects your location or you can search for any city you want. The interface is clean, modern, and supports both dark and light themes.

## Features

- **Auto Location Detection** - Opens up and shows your local weather automatically
- **Search Any City** - Type in any city name worldwide and get instant weather data
- **Temperature Units** - Switch between Celsius and Fahrenheit with one click
- **Theme Toggle** - Choose between dark mode and light mode
- **Real-time Data** - Shows current temperature, humidity, wind speed, UV index, and more
- **Clean UI** - Modern interface that's easy on the eyes and simple to use

## Screenshots

The app shows:
- Current temperature and weather condition
- Feels-like temperature
- Humidity percentage
- Wind speed
- UV index
- Location details (city, region, country)

## Getting Started

### What You Need

- Python 3.7 or higher
- Internet connection
- A free API key from WeatherAPI.com

### Installation

1. Clone this repository or download the files:
```bash
git clone https://github.com/yourusername/weather-forecast.git
cd weather-forecast
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

That's it! The dependencies are pretty lightweight.

### Getting Your API Key

You'll need a free API key from WeatherAPI to make this work:

1. Go to [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)
2. Sign up for a free account (takes like 2 minutes)
3. Verify your email
4. Log in and copy your API key from the dashboard
5. Open `weather_app.py` and replace `YOUR_WEATHERAPI_KEY` on line 26 with your actual key

The free tier gives you 1 million API calls per month, which is way more than you'll ever need for personal use.

### Running the App

Just run:
```bash
python weather_app.py
```

The app will open up and automatically try to detect your location. If that doesn't work, just type in your city name and hit enter.

## How to Use

It's pretty straightforward:

- ** Button** - Click this to auto-detect your location and show local weather
- **Search Bar** - Type any city name and press Enter or click the search button
- **°F/°C Button** - Toggle between Fahrenheit and Celsius
- **☀/🌙 Button** - Switch between light and dark theme

## What's Inside

```
weather-forecast/
├── weather_app.py      # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

The code is organized into:
- **Services** - Handle API calls and location detection
- **UI Components** - Weather card, loading spinner, error displays
- **Main App** - Puts everything together

## Technical Details

### Built With

- **CustomTkinter** - Modern UI framework for Python
- **Requests** - For API calls
- **Threading** - Keeps the UI responsive while fetching data
- **WeatherAPI** - Provides the weather data

### How It Works

The app uses threading to make API calls in the background, so the interface never freezes while loading data. When you search for a city or click the location button, it:

1. Shows a loading spinner
2. Makes an API call in a background thread
3. Updates the UI with the weather data when it arrives
4. Shows an error message if something goes wrong

The location detection uses your IP address to figure out where you are, then fetches weather for that location.

## API Information

This app uses the [WeatherAPI.com](https://www.weatherapi.com/) service. The free tier includes:

- 1,000,000 calls per month
- Current weather data
- 3-day forecast capability (not currently used in this app)
- Global coverage

## Customization Ideas

If you want to extend this app, here are some ideas:

- Add a 3-day or 7-day forecast view
- Save favorite cities
- Add weather alerts/notifications
- Show sunrise and sunset times
- Add weather charts or graphs
- Support multiple languages

The code is pretty modular, so adding features shouldn't be too hard.

## Troubleshooting

**App shows "Demo City" instead of real weather:**
- Make sure you've added your API key to line 26 in `weather_app.py`
- Save the file after editing

**"Could not fetch weather data" error:**
- Check your internet connection
- Verify your API key is correct
- Make sure you haven't exceeded the API rate limit (check your WeatherAPI dashboard)

**App won't start:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.7 or higher: `python --version`

## License

Feel free to use this code however you want. No restrictions.

## Contributing

If you find bugs or want to add features, feel free to open an issue or submit a pull request. I'm open to improvements!

## Acknowledgments

- Weather data provided by [WeatherAPI.com](https://www.weatherapi.com/)
- UI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Contact

If you have questions or suggestions, feel free to reach out or open an issue on GitHub.

