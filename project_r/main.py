import json
from code_modules.search_area import SearchArea
from code_modules.validation import validate_coordinates

def load_api_key():
    """
    Load the Google API key from the main folder.
    """
    try:
        with open('GoogleApi_Key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("API key file not found. Please ensure the GoogleApi_key.txt file is present.")
        return None

def save_results_to_json(results, filename='restaurants_results.json'):
    """
    Save the restaurant results to a JSON file.
    """
    with open(filename, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Results saved to {filename} successfully!")

def main():
    api_key = load_api_key()
    if not api_key:
        return

    latitude = float(input("Enter your latitude: "))
    longitude = float(input("Enter your longitude: "))
    search_radius = int(input("Enter the search radius (in meters): "))

    # Validate coordinates
    if not validate_coordinates(latitude, longitude):
        print("Bruh! You are in water! Swim out first before we try again!")
        return
    else:
        print("At least you are on land!")
    #     # Proceed with the search if validation passes
    #     search_area = SearchArea(api_key, latitude, longitude, search_radius)   # Initialize the search area
    #     results = search_area.get_restaurants()                                 # Start the search for restaurants

    #     if results:
    #         save_results_to_json(results)
    #     return

if __name__ == "__main__":
    main()