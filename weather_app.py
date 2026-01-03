"""
Modern Weather Forecast Application
====================================
A sleek, non-blocking weather app using CustomTkinter.

Features:
- Modern dark/light theme UI
- Non-blocking API calls (threaded)
- Automatic IP-based location detection
- Manual city search
- Real-time weather data with icons
"""

import customtkinter as ctk
import requests
import threading
from typing import Optional, Callable
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# Configuration
# ============================================================================

API_KEY = "YOUR_WEATHERAPI_KEY"  # Replace with your WeatherAPI key from weatherapi.com
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
IPINFO_URL = "https://ipinfo.io/json"

# Theme configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class WeatherData:
    """Structured weather information."""
    city: str
    region: str
    country: str
    temp_c: float
    temp_f: float
    feels_like_c: float
    feels_like_f: float
    humidity: int
    wind_kph: float
    wind_mph: float
    condition: str
    condition_icon: str
    uv: float
    last_updated: str


@dataclass
class LocationData:
    """Location information from IP lookup."""
    city: str
    region: str
    country: str
    coordinates: str


# ============================================================================
# Services (API Layer)
# ============================================================================

class LocationService:
    """Handles IP-based location detection."""

    @staticmethod
    def get_location_from_ip() -> Optional[LocationData]:
        """
        Get location directly from IP - no redundant geocoding needed.
        ipinfo.io already provides city, region, country.
        """
        try:
            response = requests.get(IPINFO_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            return LocationData(
                city=data.get("city", "Unknown"),
                region=data.get("region", ""),
                country=data.get("country", ""),
                coordinates=data.get("loc", "")
            )
        except requests.RequestException:
            return None


class WeatherService:
    """Handles weather API interactions."""

    @staticmethod
    def get_weather(query: str) -> Optional[WeatherData]:
        """
        Fetch weather data for a city or coordinates.

        Args:
            query: City name or "lat,lon" coordinates
        """
        if API_KEY == "YOUR_WEATHERAPI_KEY":
            # Demo mode - return sample data
            return WeatherData(
                city="Demo City",
                region="Demo Region",
                country="DC",
                temp_c=22.5,
                temp_f=72.5,
                feels_like_c=23.0,
                feels_like_f=73.4,
                humidity=65,
                wind_kph=15.0,
                wind_mph=9.3,
                condition="Partly Cloudy",
                condition_icon="//cdn.weatherapi.com/weather/64x64/day/116.png",
                uv=5.0,
                last_updated="2024-01-01 12:00"
            )

        try:
            response = requests.get(
                WEATHER_API_URL,
                params={"key": API_KEY, "q": query, "aqi": "no"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            location = data["location"]
            current = data["current"]

            return WeatherData(
                city=location["name"],
                region=location["region"],
                country=location["country"],
                temp_c=current["temp_c"],
                temp_f=current["temp_f"],
                feels_like_c=current["feelslike_c"],
                feels_like_f=current["feelslike_f"],
                humidity=current["humidity"],
                wind_kph=current["wind_kph"],
                wind_mph=current["wind_mph"],
                condition=current["condition"]["text"],
                condition_icon=current["condition"]["icon"],
                uv=current["uv"],
                last_updated=current["last_updated"]
            )
        except requests.RequestException:
            return None


# ============================================================================
# Async Task Runner
# ============================================================================

class AsyncRunner:
    """
    Runs tasks in background threads without blocking the UI.
    Uses callbacks to update UI safely from the main thread.
    """

    @staticmethod
    def run(task: Callable, callback: Callable, root: ctk.CTk):
        """
        Execute a task in a background thread.

        Args:
            task: Function to run in background
            callback: Function to call with result (runs on main thread)
            root: CTk root window for thread-safe callback scheduling
        """
        def worker():
            result = task()
            # Schedule callback on main thread
            root.after(0, lambda: callback(result))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()


# ============================================================================
# UI Components
# ============================================================================

class LoadingSpinner(ctk.CTkFrame):
    """Animated loading indicator."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.label = ctk.CTkLabel(
            self,
            text="⟳ Loading...",
            font=ctk.CTkFont(size=16)
        )
        self.label.pack(pady=20)


class WeatherCard(ctk.CTkFrame):
    """Displays weather information in a card layout."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=15, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        # Location header
        self.location_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.location_label.pack(pady=(20, 5))

        self.region_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.region_label.pack()

        # Temperature display
        self.temp_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.temp_frame.pack(pady=20)

        self.temp_label = ctk.CTkLabel(
            self.temp_frame,
            text="--°",
            font=ctk.CTkFont(size=64, weight="bold")
        )
        self.temp_label.pack(side="left")

        self.unit_label = ctk.CTkLabel(
            self.temp_frame,
            text="C",
            font=ctk.CTkFont(size=24)
        )
        self.unit_label.pack(side="left", anchor="n", pady=(10, 0))

        # Condition
        self.condition_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(size=18)
        )
        self.condition_label.pack()

        # Details grid
        self.details_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.details_frame.pack(pady=20, padx=20, fill="x")

        self._create_detail("feels_like", "Feels Like", "--°C", 0, 0)
        self._create_detail("humidity", "Humidity", "--%", 0, 1)
        self._create_detail("wind", "Wind", "-- km/h", 1, 0)
        self._create_detail("uv", "UV Index", "--", 1, 1)

        # Last updated
        self.updated_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.updated_label.pack(pady=(0, 15))

    def _create_detail(self, name: str, label: str, value: str, row: int, col: int):
        frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        frame.grid(row=row, column=col, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w")

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        value_label.pack(anchor="w")
        setattr(self, f"{name}_value", value_label)

    def update_weather(self, weather: WeatherData, use_celsius: bool = True):
        """Update all weather display fields."""
        self.location_label.configure(text=weather.city)
        self.region_label.configure(text=f"{weather.region}, {weather.country}")

        if use_celsius:
            self.temp_label.configure(text=f"{weather.temp_c:.0f}°")
            self.unit_label.configure(text="C")
            self.feels_like_value.configure(text=f"{weather.feels_like_c:.0f}°C")
            self.wind_value.configure(text=f"{weather.wind_kph:.0f} km/h")
        else:
            self.temp_label.configure(text=f"{weather.temp_f:.0f}°")
            self.unit_label.configure(text="F")
            self.feels_like_value.configure(text=f"{weather.feels_like_f:.0f}°F")
            self.wind_value.configure(text=f"{weather.wind_mph:.0f} mph")

        self.condition_label.configure(text=weather.condition)
        self.humidity_value.configure(text=f"{weather.humidity}%")
        self.uv_value.configure(text=f"{weather.uv}")
        self.updated_label.configure(text=f"Updated: {weather.last_updated}")


class ErrorDisplay(ctk.CTkFrame):
    """Shows error messages with retry option."""

    def __init__(self, parent, retry_callback: Callable, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.retry_callback = retry_callback
        self._create_widgets()

    def _create_widgets(self):
        self.icon_label = ctk.CTkLabel(
            self,
            text="⚠",
            font=ctk.CTkFont(size=48)
        )
        self.icon_label.pack(pady=(30, 10))

        self.message_label = ctk.CTkLabel(
            self,
            text="Unable to fetch weather data",
            font=ctk.CTkFont(size=16)
        )
        self.message_label.pack(pady=10)

        self.retry_btn = ctk.CTkButton(
            self,
            text="Retry",
            command=self.retry_callback,
            width=120
        )
        self.retry_btn.pack(pady=20)

    def set_message(self, message: str):
        self.message_label.configure(text=message)


# ============================================================================
# Main Application
# ============================================================================

class WeatherApp(ctk.CTk):
    """Main weather application window."""

    def __init__(self):
        super().__init__()

        self.title("Weather Forecast")
        self.geometry("400x600")
        self.minsize(350, 500)

        self.current_weather: Optional[WeatherData] = None
        self.use_celsius = True

        self._create_ui()
        self._fetch_weather_by_location()

    def _create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with theme toggle
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Weather Forecast",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left")

        # Theme toggle
        self.theme_btn = ctk.CTkButton(
            header_frame,
            text="☀",
            width=35,
            height=35,
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right")

        # Unit toggle
        self.unit_btn = ctk.CTkButton(
            header_frame,
            text="°F",
            width=35,
            height=35,
            command=self._toggle_unit
        )
        self.unit_btn.pack(side="right", padx=(0, 10))

        # Search bar
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search city...",
            height=40
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self._search_city())

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=40,
            command=self._search_city
        )
        search_btn.pack(side="right")

        location_btn = ctk.CTkButton(
            search_frame,
            text="📍",
            width=40,
            height=40,
            command=self._fetch_weather_by_location
        )
        location_btn.pack(side="right", padx=(0, 5))

        # Content area (for weather card, loading, or error)
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # Initialize components
        self.weather_card = WeatherCard(self.content_frame)
        self.loading_spinner = LoadingSpinner(self.content_frame)
        self.error_display = ErrorDisplay(self.content_frame, self._fetch_weather_by_location)

        # Start with loading
        self._show_loading()

    def _clear_content(self):
        """Hide all content widgets."""
        self.weather_card.pack_forget()
        self.loading_spinner.pack_forget()
        self.error_display.pack_forget()

    def _show_loading(self):
        """Display loading state."""
        self._clear_content()
        self.loading_spinner.pack(fill="both", expand=True)

    def _show_weather(self):
        """Display weather card."""
        self._clear_content()
        self.weather_card.pack(fill="both", expand=True)

    def _show_error(self, message: str = "Unable to fetch weather data"):
        """Display error state."""
        self._clear_content()
        self.error_display.set_message(message)
        self.error_display.pack(fill="both", expand=True)

    def _toggle_theme(self):
        """Toggle between dark and light mode."""
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self.theme_btn.configure(text="🌙" if new_mode == "light" else "☀")

    def _toggle_unit(self):
        """Toggle between Celsius and Fahrenheit."""
        self.use_celsius = not self.use_celsius
        self.unit_btn.configure(text="°C" if not self.use_celsius else "°F")

        if self.current_weather:
            self.weather_card.update_weather(self.current_weather, self.use_celsius)

    def _fetch_weather_by_location(self):
        """Detect location from IP and fetch weather."""
        self._show_loading()

        def task():
            location = LocationService.get_location_from_ip()
            if location:
                return WeatherService.get_weather(location.city)
            return None

        AsyncRunner.run(task, self._handle_weather_result, self)

    def _search_city(self):
        """Search weather for entered city."""
        city = self.search_entry.get().strip()
        if not city:
            return

        self._show_loading()

        def task():
            return WeatherService.get_weather(city)

        AsyncRunner.run(task, self._handle_weather_result, self)

    def _handle_weather_result(self, weather: Optional[WeatherData]):
        """Handle weather API response."""
        if weather:
            self.current_weather = weather
            self.weather_card.update_weather(weather, self.use_celsius)
            self._show_weather()
        else:
            self._show_error("Could not fetch weather data.\nCheck your connection or API key.")


# ============================================================================
# Entry Point
# ============================================================================

def main():
    app = WeatherApp()
    app.mainloop()


if __name__ == "__main__":
    main()
