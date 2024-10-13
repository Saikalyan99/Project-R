import requests
import math
from code_modules.db_insertion import calculate_next_coordinate

class SearchArea:
    def __init__(self, api_key, latitude, longitude, radius):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.min_radius = 2500
        self.max_radius = 5000
        self.restaurants = []

    def adjust_radius_based_on_results(self, results_count):
        """
        Adjust the search radius based on the number of results.
        """
        if results_count > 59:
            self.radius = max(self.min_radius, self.radius * 0.8)
        elif results_count < 20:
            self.radius = min(self.max_radius, self.radius * 2)
        elif 20 <= results_count < 40:
            self.radius = min(self.max_radius, self.radius * 1.5)
        elif 40 <= results_count < 50:
            self.radius = min(self.max_radius, self.radius * 1.25)

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points in kilometers.
        """
        R = 6371  # Radius of the Earth in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Distance in kilometers

    def fetch_restaurants(self):
        """
        Fetch restaurants from the Google Places API using latitude, longitude, and radius.
        Only extract the fields: name, business_status, address, types, price_level, rating, and distance.
        """
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f"{self.latitude},{self.longitude}",
            'radius': self.radius,
            'type': 'restaurant',
            'key': self.api_key
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])

            # Filter the fields we need: name, business_status, address, types, price_level, rating
            filtered_results = []
            for place in results:
                place_lat = place['geometry']['location']['lat']
                place_lng = place['geometry']['location']['lng']
                distance = self.haversine_distance(self.latitude, self.longitude, place_lat, place_lng)

                filtered_results.append({
                    'name': place.get('name'),
                    'business_status': place.get('business_status'),
                    'address': place.get('formatted_address'),  # Use 'vicinity' for address
                    'types': place.get('types'),
                    'price_level': place.get('price_level'),
                    'rating': place.get('rating'),
                    'distance_km': round(distance, 2)  # Distance to the restaurant in kilometers
                })
            print ("requested", self.radius, len(filtered_results), self.latitude, self.longitude)
            return filtered_results
        return []

    def perform_search(self):
        """
        Perform the search and adjust the radius dynamically.
        """
        results = self.fetch_restaurants()
        self.adjust_radius_based_on_results(len(results))
        self.restaurants.extend(results)

        # Perform perimeter search
        self.expand_search_area()
        return self.restaurants

    def expand_search_area(self):
        """
        Expand the search by adding more search circles around the perimeter.
        """
        num_circles = self.calculate_dynamic_perimeter_circles()
        distance = self.radius * 2

        for i in range(num_circles):
            angle = i * (360 / num_circles)
            new_lat, new_lng = calculate_next_coordinate(self.latitude, self.longitude, distance, angle)
            self.latitude, self.longitude = new_lat, new_lng

            results = self.fetch_restaurants()
            self.restaurants.extend(results)

    def calculate_dynamic_perimeter_circles(self):
        """
        Dynamically calculate the number of perimeter circles.
        """
        circumference = 2 * math.pi * self.radius
        num_circles = max(6, int(circumference / (2 * self.radius)))
        return num_circles