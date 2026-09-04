# api.py
import requests

def get_diseases():
    response = requests.get('http://127.0.0.1:8000/api/diseases')
    response.raise_for_status()  # magra-raise ng error kung hindi 200 OK

    json_data = response.json()

    if not json_data.get('success'):
        raise Exception('API returned success: false')

    return json_data['data']