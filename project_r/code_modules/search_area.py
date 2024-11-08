import requests
import math

class SearchArea:
    def __init__(self, api_key, latitude, longitude, radius):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        
        # Hexagonal search parameters
        self.max_radius = 243000  # Max starting radius
        self.min_radius = 81000   # Initial radius for each hexagon
        self.stage = 1            # Track stages in hexagonal expansion
        self.coordinates_list_old = []
        self.coordinates_list = []
        self.restaurants = []     # Store found restaurant data

    def grid_initiator(self):
        """Initiates the grid search process starting with the center hexagon."""
        results = []
        self.restaurants.extend(self.grid_process_n_check(self.latitude, self.longitude, self.radius, 0))
        
        # Future placeholder for expanding outer hexagon layers
        # results.extend(self.expand_hexagon_layers(self.latitude, self.longitude))
        
        return self.restaurants  # Return the aggregated results as a list

    
    def grid_process_n_check(self, center_x, center_y, radius, depth):
        """Process and check if internal divide is needed based on restaurant count."""
        total_restaurants = self.find_restaurants(center_x, center_y, radius)
        
        # If restaurant count exceeds the threshold, proceed to internal division
        if len(total_restaurants) > 59:
            total_restaurants.extend(self.internal_divide(center_x, center_y, radius, depth + 1))
        
        return total_restaurants  # Return results for the current hexagon

            
    def internal_divide(self, center_x, center_y, radius, depth):
        """Divide the circle into seven smaller circles and gather results."""
        results = []
        sub_radius = (radius / 3) + (radius / 10)
        
        for i in range(6):  # Generate six surrounding hexagon centers
            angle = math.radians(60 * i)
            new_lat = center_x + (sub_radius / 111320) * math.cos(angle)
            new_lon = center_y + (sub_radius / (111320 * math.cos(math.radians(center_x)))) * math.sin(angle)
            results.extend(self.grid_process_n_check(new_lat, new_lon, sub_radius, depth))
        
        # Also gather results for the central point
        results.extend(self.grid_process_n_check(center_x, center_y, sub_radius, depth))
        
        return results
    
    def find_restaurants(self, latitude, longitude, search_radius):
        """
        Fetch restaurants from Google Places API within a specified radius.
        Also includes Plus Code search capability and distance calculation.
        """
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f"{latitude},{longitude}",
            'radius': search_radius,
            'type': 'restaurant',
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            # Extract necessary fields and add to the main restaurants list
            filtered_restaurants = []
            for place in results:
                place_lat = place['geometry']['location']['lat']
                place_lng = place['geometry']['location']['lng']
                
                # Calculate distance from search center and round to 2 decimal places
                distance = self.haversine_distance(self.latitude, self.longitude, place_lat, place_lng)
                distance = round(distance, 2)
                
                restaurant_data = {
                    'name': place.get('name'),
                    'business_status': place.get('business_status'),
                    'address': place.get('vicinity'),
                    'types': place.get('types'),
                    'price_level': place.get('price_level'),
                    'rating': place.get('rating'),
                    #'latitude': place_lat,
                    #'longitude': place_lng,  
                    'plus_code': place.get('plus_code', {}).get('global_code'),  # Retrieve Plus Code if available
                    'distance': round(distance, 2)  # Add rounded distance to the data
                }
                filtered_restaurants.append(restaurant_data)
            
            # Store the filtered results in the main restaurants list
            self.restaurants.extend(filtered_restaurants)
            return filtered_restaurants
        return []
  
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points in kilometers.
        """
        R = 6371  # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c