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
        self.max_radius = 243000                                                        # Max starting radius in meters
        self.min_radius = 27000                                                         # Initial radius for each hexagon in meters
        self.stage = 1                                                                  # Track stages in hexagonal expansion
        self.coordinates_list_old = []                                                  # Stores previous stage coordinates 
        self.coordinates_list = []                                                      # Store current stage coordinates
        self.restaurants = []                                                           # Store found restaurant data
        
        # Correct instantiation of DbDataProcessor with request_type included
        self.data_dump = DbDataProcessor(latitude, longitude, self.haversine_distance, request_type="API")

    def grid_initiator(self):
        """ Initiates the grid search process starting with the center hexagon """
        if self.radius < self.min_radius:
            self.min_radius = self.radius
            self.grid_process_n_check(self.latitude, self.longitude, self.min_radius * 1.1, 0)
        else:
            # Start the search and expansion process with min_radius
            self.grid_calculator(self.latitude, self.longitude, self.min_radius)

        self.restaurants = self.data_dump.data_deduplicator(self.restaurants)
        return self.restaurants                                                         # Return the aggregated results as a list

    def grid_calculator(self, center_x, center_y, radius):
        """ Keeps track of position of the hexagons and manages multi-stage expansion """
        self.grid_process_n_check(center_x, center_y, radius * 1.1, 0)
        
        # Continue expanding in a loop until a kill condition is added
        condition = True
        while condition:
            for i in range((self.stage * 6) + 1):
                angle = math.radians(60 * i)                                            # Angle per hexagon in the current ring
                new_center_x = center_x + (radius * 2 * self.stage) / 111320 * math.cos(angle)
                new_center_y = center_y + (radius * 2 * self.stage) / (111320 * math.cos(math.radians(center_x))) * math.sin(angle)
                
                # Calculate distance to determine whether to continue with internal or external expansion
                distance_from_origin = self.haversine_distance(self.latitude, self.longitude, new_center_x, new_center_y)
                self.coordinates_list.append((new_center_x, new_center_y))
                
                if distance_from_origin > (self.radius + 1.5 * self.min_radius) / 1000:
                    condition = False                                                   # Break when the radius exceeded requirement
                    
                if i == 0:
                    (temp_x, temp_y) = (new_center_x, new_center_y)

                if i == 6:
                    """ Move to the next stage after processing all six neighbors """
                    self.coordinates_list_old = self.coordinates_list.copy()
                    self.coordinates_list.clear()
                    self.stage += 1
                    print("Moving to Stage ", self.stage, "Loop", condition, "\b, distance =", distance_from_origin, "and", (self.radius + 1.5 * self.min_radius)/1000)
                    index = 0
                    break
                else:
                    """ Process each hexagon in the current stage """
                    self.grid_process_n_check(new_center_x, new_center_y, radius * 1.1, 0)
                    if self.stage > 1:
                        for j in range(self.stage - 1):                                 # Generate hexagons in a straight line within the stage
                            new_center_x, new_center_y = self.coordinates_list_old[index]
                            index += 1
                            self.coordinates_list.append(self.move_external_inline(new_center_x, new_center_y, radius * 1.1, 60 + (60 * i)))
    
    def move_external_inline(self, new_center_x, new_center_y, radius, angle):
        """ Move to the 6 external neighboring hexagons and check them """
        rad_angle = math.radians(angle)
        neighbor_center_x = new_center_x + (radius / 111320) * math.cos(rad_angle)
        neighbor_center_y = new_center_y + (radius / (111320 * math.cos(math.radians(new_center_x)))) * math.sin(rad_angle)
        self.grid_process_n_check(neighbor_center_x, neighbor_center_y, radius * 1.1, 0)
        return (neighbor_center_x, neighbor_center_y)
    
    def grid_process_n_check(self, center_x, center_y, radius, depth):
        """ Process and check if internal divide is needed based on restaurant count """
        temp_result = self.find_restaurants(center_x, center_y, radius)
        print("API called, no. of restaurants =", len(temp_result), "depth =", depth, "\b, radius =", radius, "at (", center_x, center_y, ")")

        if len(temp_result) > 59:                                                       # If restaurant count API limit 59, moves to internal division
            self.internal_divide(center_x, center_y, radius, depth + 1)
        else:
            self.restaurants.extend(temp_result)

    def internal_divide(self, center_x, center_y, radius, depth):
        """ Divide the circle into seven smaller circles and gather results """
        sub_radius = (radius / 3) + (radius / 10)
        self.grid_process_n_check(center_x, center_y, sub_radius, depth)                # Gather results for central grid first
        
        for i in range(6):                                                              # Generate six surrounding hexagon centers
            angle = math.radians(60 * i)
            new_lat = center_x + (sub_radius / 111320) * math.cos(angle)
            new_lon = center_y + (sub_radius / (111320 * math.cos(math.radians(center_x)))) * math.sin(angle)
            self.grid_process_n_check(new_lat, new_lon, sub_radius, depth)

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
        response = requests.get(url, params=params)
        if response.status_code == 200:                                                 # Status code 200 means successful handshake
            data = response.json()
            results = data.get('results', [])
            all_pages.extend(results)
            
            if len(results) > 19:                                                       # If fewer than 20 results, no paging needed
                for _ in range(2):                                                      # Loop to handle pagination of next 2 pages                
                    next_page_token = data.get('next_page_token')                       # Check for the next page token
                    if next_page_token:
                        params['pagetoken'] = next_page_token
                        time.sleep(2)                                                   # Wait for the next page to become available
                        response = requests.get(url, params=params)                     # Make the request for the next page
                        if response.status_code == 200:
                            data = response.json()
                            results = data.get('results', [])
                            all_pages.extend(results)
                        else:
                            break                                                       # Break if there's an issue with the request
                    else:
                        break                                                           # No next page token, so break the loop
        else:
            print("Initial API call failed with status code:", response.status_code)

        unique_restaurants = self.data_dump.filter_restaurants_api(all_pages)           # Process the collected data filter restaurants
        return unique_restaurants
  
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """ Calculate the Haversine distance between two points in kilometers """
        earth_radius = 6371                                                             # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        chord_half_sq = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        angular_distance = 2 * math.atan2(math.sqrt(chord_half_sq), math.sqrt(1 - chord_half_sq))
        return earth_radius * angular_distance