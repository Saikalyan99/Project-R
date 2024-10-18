import math

def calculate_next_coordinate(lat, lng, distance, angle):
    """
    Calculate the next coordinate for perimeter search using polar coordinates.
    """
    angle_radians = math.radians(angle)
    new_lat = lat + (distance * math.cos(angle_radians) / 111320)  # Convert meters to degrees
    new_lng = lng + (distance * math.sin(angle_radians) / (40075000 * math.cos(lat * math.pi / 180) / 360))
    return new_lat, new_lng