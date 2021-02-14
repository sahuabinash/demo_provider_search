from annoy import AnnoyIndex
from pathlib import Path
import requests
import json

# Set up
state = 'CT'
data_path = Path('.').absolute().parent / 'data'
file_name = f'{data_path}\prov_{state}_addr_index.ann'

# Search
f = 2 # number of features. for us its just LAT, LONG
u = AnnoyIndex(f, 'euclidean')
u.load(file_name)
# Provide coordinates of origin
o_lat = 41.60
o_long = -72.72
match = u.get_nns_by_vector([o_lat,o_long], 5) # will find the 5 nearest neighbors


# Define a function to return driving distance and time
def calc_drive_distance_time(o_lat,o_long,d_lat,d_long):
    """
    Calculates the distance and duration from origin to destination using OSRM API
    :param o_lat: Lat of Origin
    :param o_long: Long of Origin
    :param d_lat: Lat of Destination
    :param d_long: Long of Destination
    :return: distance(miles), duration(minutes)
    """
    r = requests.get(f"http://router.project-osrm.org/route/v1/car/{o_long},{o_lat};{d_long},{d_lat}?overview=false""")
    routes = json.loads(r.content)
    route_1 = routes.get("routes")[0]
    distance = round(route_1["distance"] / 1609.34, 2)
    duration = round(route_1['duration'] / 60, 2)

    return distance, duration

# Print the 5 best closest match and the corresponding driving distance & duration
for i in match:
    print('*************************************************************************')
    print(f'lat,long for neighbors in index {i} are {u.get_item_vector(i)}')
    d_lat,d_long = u.get_item_vector(i)
    miles, time = calc_drive_distance_time(o_lat,o_long,d_lat,d_long)
    print(f'Distance of travel:{miles} miles')
    print(f'Duration of travel:{time} minutes')

