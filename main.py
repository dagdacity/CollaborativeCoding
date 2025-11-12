import sys
import requests
import json
from typing import List, Tuple

class Meteo:

    EARTH_RADIUS_KM = 6371.0

    def __init__(self, suit=None):
        self.suit = suit

    def get_weather_for_location(self, lat: float, lon: float, altitude = None) -> json:
        """Fetch weather data from Met.no API for specific location"""
        
        url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        
        params = {
            "lat": lat,
            "lon": lon
        }

        if altitude:
            params["altitude"] = altitude
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return e
    
    def calculate_middle_coordinates(
        self, 
        lat_start: float, 
        lon_start: float, 
        lat_end: float, 
        lon_end: float, 
        speed: float = None
    ) -> List[Tuple[float, float]]:
        """
        Calculates all middle points to get weather from along a route.
        
        Uses great circle (orthodromic) distance calculations to properly account
        for Earth's curvature. Points are calculated along the shortest path.
        
        Args:
            lat_start (float): Starting latitude in decimal degrees (-90 to 90)
            lon_start (float): Starting longitude in decimal degrees (-180 to 180)
            lat_end (float): Ending latitude in decimal degrees (-90 to 90)
            lon_end (float): Ending longitude in decimal degrees (-180 to 180)
            speed (float, optional): Speed in km/h. If provided, calculates waypoints
                                    at 1-hour intervals. If None, uses distance-based
                                    spacing (every ~100km). Defaults to None.
        
        Returns:
            List[Tuple[float, float]]: List of (latitude, longitude) tuples representing
                                       waypoints along the route, including start and end points.
        
        Example:
            >>> calculator = RouteWeatherCalculator()
            >>> # New York to London
            >>> waypoints = calculator.calculate_middle_coordinates(40.7128, -74.0060, 51.5074, -0.1278)
            >>> print(f"Route has {len(waypoints)} waypoints")
            
            >>> # With speed (120 km/h) - waypoints every hour
            >>> waypoints = calculator.calculate_middle_coordinates(40.7128, -74.0060, 51.5074, -0.1278, speed=120)
        """
        # Validate coordinates
        # self._validate_coordinates(lat_start, lon_start, lat_end, lon_end)
        
        # Calculate total distance
        total_distance_km = self.calculate_great_circle_distance(
            lat_start, lon_start, lat_end, lon_end
        )
        
        # Determine spacing between waypoints
        if speed is not None and speed > 0:
            # Calculate waypoints based on time intervals (1 hour)
            spacing_km = speed  # Distance covered in 1 hour
            num_intervals = max(1, int(total_distance_km / spacing_km))
        else:
            # Default: waypoint every ~100km or at least 5 waypoints for longer routes
            spacing_km = 50.0
            num_intervals = max(5, int(total_distance_km / spacing_km))
        
        # For very short distances, just return start and end
        if total_distance_km < 10:
            return [(lat_start, lon_start), (lat_end, lon_end)]
        
        # Calculate intermediate points
        waypoints = []
        
        # Always include start point
        waypoints.append((lat_start, lon_start))
        
        # Calculate intermediate points using great circle interpolation
        for i in range(1, num_intervals):
            fraction = i / num_intervals
            lat, lon = self._interpolate_great_circle(
                lat_start, lon_start, lat_end, lon_end, fraction
            )
            waypoints.append((lat, lon))
        
        # Always include end point
        waypoints.append((lat_end, lon_end))
        
        return waypoints

    def calculate_pants_wettness(
            self,
            lat_start: float, 
            lon_start: float, 
            lat_end: float, 
            lon_end: float, 
            time_start: float, 
            speed: float 
            ) -> int:
        """Clalculates wettness of the pants for the ride"""
        pass
    
    def get_weather_details(self, weather_for_locatio:json, time_for_location):
        pass
       

# Bauska 56.407122, 24.187309
# StartSchool 56.941407, 24.117372
# https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=56.407122&lon=24.187309
# https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=56.941407&lon=24.117372
# "time":"2025-11-12T09:00:00Z"
# "precipitation_amount":"mm"
# "air_temperature":"celsius"

def get_weather_for_location(lat: float, lon: float, altitude = None) -> json:
        """Fetch weather data from Met.no API for specific location"""
        
        url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        
        params = {
            "lat": lat,
            "lon": lon
        }

        headers = {
            "User-Agent": "WeatherFetcher/1.0 (your-email@example.com)"
        }
        
        if altitude:
            params["altitude"] = altitude
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
if __name__ == "__main__":
    print("hellow world!")
    met = Meteo()
    data = met.get_weather_for_location(56.407122, 24.187309)
    print(data)