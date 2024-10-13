import json
from code_modules.search_area import SearchArea
from code_modules.validation import validate_coordinates

class RestaurantSearchApp:
    def __init__(self):
        self.api_key = self.load_api_key()
        self.latitude = None
        self.longitude = None
        self.search_radius = None

    def load_api_key(self):
        """
        Load the Google API key from the main folder.
        """
        try:
            with open('GoogleApi_Key.txt', 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            print("API key file not found. Please ensure the GoogleApi_key.txt file is present.")
            return None

    def get_user_input(self):
        """
        Get user input for latitude, longitude, and search radius.
        """
        self.latitude = float(input("Enter your latitude: "))
        self.longitude = float(input("Enter your longitude: "))
        self.search_radius = int(input("Enter the search radius (in meters): "))

    def validate_location(self):
        """
        Validate the user's coordinates using the IsItWater API.
        """
        if not validate_coordinates(self.latitude, self.longitude):
            print("Bruh! You are in water! Swim out first before we try again!")
            return False
        print("At least you are on land!")
        return True

    def save_results_to_json(self, results, filename='restaurants_results.json'):
        """
        Save the restaurant results to a JSON file.
        """
        with open(filename, 'w') as json_file:
            json.dump(results, json_file, indent=4)
        print(f"Results saved to {filename} successfully!")

    def search_restaurants(self):
        """
        Perform the restaurant search after validation.
        """
        if not self.api_key:
            return

        # Get user input
        self.get_user_input()

        # Validate coordinates
        if not self.validate_location():
            return

        # Proceed with the search if validation passes
        search_area = SearchArea(self.api_key, self.latitude, self.longitude, self.search_radius)
        results = search_area.get_restaurants()

        # Save results if found
        if results:
            self.save_results_to_json(results)

def main():
    app = RestaurantSearchApp()
    app.search_restaurants()

if __name__ == "__main__":
    main()
