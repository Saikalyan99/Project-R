import json
import math
import time
import requests
from code_modules.db_insertion import DbDataProcessor

class SearchArea:
    def __init__(self, api_key, latitude, longitude, radius):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        
        # Hexagonal search parameters
        self.max_radius = 243000                                                                    # Max starting radius in meters
        self.min_radius = 27000                                                                     # Initial radius for each hexagon in meters
        self.stage = 1                                                                              # Track stages in hexagonal expansion
        self.coordinates_list_old = []                                                              # Stores previous stage coordinates 
        self.coordinates_list = []                                                                  # Store current stage coordinates
        self.restaurants = []                                                                       # Store found restaurant data
        
        # Correct instantiation of DbDataProcessor with request_type included
        self.data_dump = DbDataProcessor(latitude, longitude, self.haversine_distance, request_type="API")

    def grid_initiator(self):
        """Initiates the grid search process starting with the center hexagon."""
        if self.radius < self.min_radius:
            self.min_radius = self.radius
            self.restaurants.extend(self.grid_process_n_check(self.latitude, self.longitude, self.min_radius * 1.1, 0))
        else:
            # Start the search and expansion process with min_radius
            self.restaurants = self.grid_calculator(self.latitude, self.longitude, self.min_radius)

        self.restaurants = self.data_dump.data_deduplicator(self.restaurants)
        return self.restaurants                                                                     # Return the aggregated results as a list

    def grid_calculator(self, center_x, center_y, radius):
        """Keeps track of position of the hexagons and manages multi-stage expansion."""
        results = []
        results.extend(self.grid_process_n_check(center_x, center_y, radius * 1.1, 0))
        
        # Continue expanding in a loop until a kill condition is added
        condition = True
        while condition:
            for i in range((self.stage * 6) + 1):
                angle = math.radians(60 * i)                                                        # Angle per hexagon in the current ring
                new_center_x = center_x + (radius / 111320) * math.cos(angle)
                new_center_y = center_y + (radius / (111320 * math.cos(math.radians(center_x)))) * math.sin(angle)
                
                # Calculate distance to determine whether to continue with internal or external expansion
                distance_from_origin = self.haversine_distance(self.latitude, self.longitude, new_center_x, new_center_y)
                self.coordinates_list.append((new_center_x, new_center_y))
                
                if distance_from_origin > (self.radius + 1.5 * self.min_radius):
                    condition = False                                                               # Break when the radius exceeded requirement
                    break

                if i == 0:
                    temp_x, temp_y = new_center_x, new_center_y

                if i == 6:
                    # Move to the next stage after processing all six neighbors
                    self.coordinates_list_old = self.coordinates_list.copy()
                    self.coordinates_list.clear()
                    self.stage += 1
                    index = 0
                    break
                else:
                    # Process each hexagon in the current stage
                    results.extend(self.grid_process_n_check(new_center_x, new_center_y, radius * 1.1, 0))
                    if self.stage > 1:
                        # Generate hexagons in a straight line within the stage
                        for j in range(self.stage - 1):
                            new_center_x, new_center_y = self.coordinates_list_old[index]
                            index += 1
                            self.coordinates_list.append(self.move_external_inline(new_center_x, new_center_y, radius * 1.1, 60 + (60 * i)))
        return results
    
    def move_external_inline(self, new_center_x, new_center_y, radius, angle):
        """Move to the 6 external neighboring hexagons and check them."""
        rad_angle = math.radians(angle)
        neighbor_center_x = new_center_x + (radius / 111320) * math.cos(rad_angle)
        neighbor_center_y = new_center_y + (radius / (111320 * math.cos(math.radians(new_center_x)))) * math.sin(rad_angle)
        return self.grid_process_n_check(neighbor_center_x, neighbor_center_y, radius * 1.1, 0)
    
    def grid_process_n_check(self, center_x, center_y, radius, depth):
        """Process and check if internal divide is needed based on restaurant count."""
        total_restaurants = self.find_restaurants(center_x, center_y, radius)
        #print("API called, number of restaurants in (", center_x, center_y, ", radius =", radius, ") =", len(total_restaurants))
        # If restaurant count exceeds the threshold, proceed to internal division
        if len(total_restaurants) > 59:
            total_restaurants.extend(self.internal_divide(center_x, center_y, radius, depth + 1))
        return total_restaurants                                                                    # Return results for the current hexagon
            
    def internal_divide(self, center_x, center_y, radius, depth):
        """Divide the circle into seven smaller circles and gather results."""
        results = []
        sub_radius = (radius / 3) + (radius / 10)
        
        for i in range(6):                                                                          # Generate six surrounding hexagon centers
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

        all_pages = []                                                                  # To store results from all pages
        for _ in range(3):                                                              # Loop to handle pagination up to 3 pages
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                all_pages.extend(results)

                if len(results) < 20:                                                   # Break if fewer than 20 results are returned
                    break
                
                next_page_token = data.get('next_page_token')                           # Check for the next page token
                if next_page_token:
                    params['pagetoken'] = next_page_token
                    time.sleep(2)                                                       # Wait for the next page to become available
                else:
                    break                                                               # No next page token, so break the loop
            else:
                break                                                                   # Break on API call failure

        unique_restaurants = self.data_dump.filter_restaurants_api(all_pages)           # Process the collected data filter restaurants
        self.restaurants.extend(unique_restaurants)                                     # Store unique results in the main restaurants list
        return unique_restaurants
  
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points in kilometers.
        """
        R = 6371                                                                        # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c