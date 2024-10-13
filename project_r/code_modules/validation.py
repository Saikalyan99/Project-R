import requests

class CoordinateValidator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://isitwater-com.p.rapidapi.com/"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "isitwater-com.p.rapidapi.com"
        }

    def validate(self, latitude, longitude):
        """
        Validate the given coordinates using the IsItWater API.
        """
        querystring = {"latitude": latitude, "longitude": longitude}

        try:
            response = requests.get(self.api_url, headers=self.headers, params=querystring)
            data = response.json()

            if data['water'] is False:
                return True     # Damn this dude is on land, more work
            else:
                return False    # Bro went for a swim!

        except Exception as e:
            print(f"An error occurred while validating coordinates: {e}")
            return False