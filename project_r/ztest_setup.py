import requests
import json
from operator import itemgetter
from tqdm import tqdm
import threading
import time

class RestaurantFinder:
    def __init__(self, api_key_file):
        self.api_key = self.load_api_key(api_key_file)
        self.base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.all_restaurants = []
        self.lock = threading.Lock()  # Lock for thread-safe data manipulation

    def load_api_key(self, api_key_file):
        """
        Loads the API key from the specified file.
        """
        try:
            with open(api_key_file, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"Error: The file {api_key_file} was not found.")
            return None

    def fetch_restaurants(self, zip_code):
        """
        Fetch all restaurants from Google Places API using pagination and threading.
        """
        if not self.api_key:
            print("Error: API key is missing.")
            return []

        # Initial query for restaurants in the area
        params = {
            'query': f'restaurants in {zip_code}',
            'key': self.api_key
        }

        response = self.make_api_call(params)
        if not response:
            return []

        # Add first batch of results
        self.all_restaurants.extend(self.parse_response(response))

        # Handle pagination to get all pages of results
        next_page_token = response.get('next_page_token')

        # Progress bar based on pages (each page returns a max of 20 results)
        progress_bar = tqdm(desc="Fetching more restaurants", total=0)
        progress_bar.update(1)  # First page fetched

        while next_page_token:
            # Wait 2-3 seconds for the next_page_token to become valid
            time.sleep(3)

            # Fetch the next page of results
            params = {'pagetoken': next_page_token, 'key': self.api_key}
            response = self.make_api_call(params)
            
            if response:
                # Parse the new results
                self.all_restaurants.extend(self.parse_response(response))

                # Update progress bar
                progress_bar.total += 1
                progress_bar.update(1)

                # Get the next page token, if available
                next_page_token = response.get('next_page_token')
            else:
                next_page_token = None  # No more pages
        
        progress_bar.close()
        return self.all_restaurants

    def make_api_call(self, params):
        """
        Makes the API call and returns the response JSON.
        """
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def parse_response(self, response):
        """
        Parses the response and extracts relevant restaurant information, including types.
        """
        restaurants = []
        for place in response.get('results', []):
            restaurant = {
                'name': place.get('name'),
                'address': place.get('formatted_address'),
                'rating': place.get('rating', 'No rating available'),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'types': place.get('types')             # Storing the types of the place
            }
            restaurants.append(restaurant)
        return restaurants

    def save_to_json(self, restaurants, filename='restaurants.json'):
        """
        Save restaurant data to a JSON file, sorted alphabetically by restaurant name.
        """
        sorted_restaurants = sorted(restaurants, key=itemgetter('name'))
        
        with open(filename, 'w') as json_file:
            json.dump(sorted_restaurants, json_file, indent=4, ensure_ascii=False)
        
        print(f"Data saved to {filename} successfully!")
def main():
    
    api_key_file = 'GoogleApi_Key.txt'                  # API key file
    finder = RestaurantFinder(api_key_file)             # Initialize the RestaurantFinder object

    zip_code = input("Enter the ZIP code: ")            # Asking user for a zip code
    restaurants = finder.fetch_restaurants(zip_code)    # Fetch restaurants based on the zip code
    
    if restaurants:
            finder.save_to_json(restaurants)            # Save the restaurant data to a JSON file
    else:
        print("No restaurants found.")

if __name__ == "__main__":
    main()