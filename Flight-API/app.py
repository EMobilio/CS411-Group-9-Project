import requests

def get_flight_info(flight_code):
    access_key = '45113167e44472815d4c34fe415a53ba' 
    url = f"https://api.aviationstack.com/v1/flights"
    params = {
        'access_key': access_key,
        'flight_icao': flight_code
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['pagination']['total'] > 0:
                flight = data['data'][0]
                arrival = flight['arrival']
                return {
                    'flight': flight_code,
                    'destination': arrival['airport'],
                    'duration': arrival['estimated_runway']
                }
            else:
                return {"error": "Flight not found"}
        else:
            return {"error": "Failed to fetch data"}
    except Exception as e:
        return {"error": f"An exception occurred: {str(e)}"}


flight_code = "UA2402"  # Uçuş kodunu buraya yaz
flight_info = get_flight_info(flight_code)
print(flight_info)
