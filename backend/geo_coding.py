import requests


def getLatLong(geocode):
    API_KEY = ''
    latLong = [0, 0]

    params = {
        'key': API_KEY,
        'address': geocode
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        print(location['lat'], location['lng'])
        latLong[0] = location['lat']
        latLong[1] = location['lng']

    return latLong
