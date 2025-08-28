import requests
api_key="d51c821afa00e0f1da48cba19ee693e1"
api_url= f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"
def fetcha_data():
    print("Fetching data from the API...")
    try:
        response = requests.get(api_url)
        print(response.json())
        response.raise_for_status()
        print("API response received sucessfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error ocurred: {e}")

    return fetcha_data()

#def mock_fetch_data():
#    return {
#        'request': {
#            'type': 'City',
#            'query': 'New York, United States of America',
#            'language': 'en',
#            'unit': 'm'
#        },
#        'location': {
#            'name': 'New York',
#            'country': 'United States of America',
#            'region': 'New York',
#            'lat': '40.714',
#            'lon': '-74.006',
#            'timezone_id': 'America/New_York',
#            'localtime': '2025-08-13 03:40',
#            'localtime_epoch': 1755056400,
#            'utc_offset': '-4.0'
#        },
#        'current': {
#            'observation_time': '07:40 AM',
#            'temperature': 26,
#            'weather_code': 116,
#            'weather_icons': [
#                'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'
#            ],
#            'weather_descriptions': ['Partly Cloudy '],
#            'astro': {
#                'sunrise': '06:05 AM',
#                'sunset': '07:56 PM',
#                'moonrise': '10:06 PM',
#                'moonset': '10:55 AM',
#                'moon_phase': 'Waning Gibbous',
#                'moon_illumination': 84
#            },
#            'air_quality': {
#                'co': '412.55',
#                'no2': '54.76',
#                'o3': '35',
#                'so2': '19.055',
#                'pm2_5': '20.535',
#                'pm10': '20.72',
#                'us-epa-index': '2',
#                'gb-defra-index': '2'
#            },
#            'wind_speed': 8,
#            'wind_degree': 229,
#            'wind_dir': 'SW',
#            'pressure': 1015,
#            'precip': 0,
#            'humidity': 71,
#            'cloudcover': 0,
#            'feelslike': 29,
#            'uv_index': 0,
#            'visibility': 16,
#            'is_day': 'no'
#        }
#    }
