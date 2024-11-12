import json

class DbDataProcessor:
    """
    A class to process restaurant data, including deduplication, insert data into DB and retrieve data from DB.
    """
    def __init__(self, latitude, longitude, haversine_distance, request_type):
        self.latitude = latitude
        self.longitude = longitude
        self.haversine_distance = haversine_distance
        self.request_type = request_type

    def filter_restaurants_api(self, all_pages):
        """
        filter restaurants based on name and global code.
        Unique restaurants after deduplication.
        """
        seen = set()
        unique_restaurants = []

        for place in all_pages:
            name = place.get('name')
            plus_code = place.get('plus_code', {}).get('global_code', None)
            identifier = (name, plus_code)

            if identifier not in seen:
                restaurant_data = {
                    'name': name,
                    'business_status': place.get('business_status'),
                    'address': place.get('vicinity'),
                    'types': place.get('types'),
                    'price_level': place.get('price_level'),
                    'rating': place.get('rating'),
                    'user_ratings_total': place.get('user_ratings_total', 0),
                    #'latitude': place_lat,
                    #'longitude': place_lng,
                    'plus_code': plus_code,
                    'distance': round(self.haversine_distance(
                        self.latitude, 
                        self.longitude, 
                        place['geometry']['location']['lat'], 
                        place['geometry']['location']['lng']), 2)
                }
                unique_restaurants.append(restaurant_data)
                seen.add(identifier)

        return unique_restaurants

    def data_deduplicator(self, data):
        """
        Data deduplication of the restaurant data to remove duplicates based on unique identifiers.
        Assuming 'name' and 'plus_code' uniquely identify each restaurant
        """
        seen = set()
        unique_data = []

        for restaurant in data:
            identifier = (restaurant.get('name'), restaurant.get('plus_code'))
            if identifier not in seen:
                unique_data.append(restaurant)
                seen.add(identifier)

        return unique_data                              # This is the final Result @Nathan
