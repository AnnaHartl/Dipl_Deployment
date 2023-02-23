import requests

files = {
    'file': ('shot.png',open('shot.png', 'rb'),'image/png'),
}

requests.post('http://127.0.0.1:5000/analyse_image', files=files)
#print(response.json())