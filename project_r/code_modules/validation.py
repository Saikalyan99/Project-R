import requests

def validate_coordinates(latitude, longitude):
    """
    Validate the given coordinates using an open-source API (e.g., OpenCage).
    """
    url = "https://isitwater-com.p.rapidapi.com/"
    querystring = {"latitude":latitude,"longitude":longitude}

    headers = {
        "x-rapidapi-key": "8826c191c0msh5595428de25ba9ap1c69acjsnf442cc8cc26d",
        "x-rapidapi-host": "isitwater-com.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        if data['water'] is False:
            return True     # Damn this dude is on land, more work
        else:
            return False    # Bro went for a swim!!

    except Exception as e:
        print(f"An error occurred while validating coordinates: {e}")
        return False