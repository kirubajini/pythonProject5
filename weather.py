from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = 'aca0a8a301d610ce3d6188ba4a880140'


@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    print("data: ", data)
    city_name = data.get('city', '')

    if not city_name:
        return jsonify({"error": "City not specified"}), 400

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric'

    try:
        response = requests.get(url)
        response_data = response.json()

        if response.status_code == 200:
            weather_info = {
                "temperature": response_data['main']['temp'],
                "description": response_data['weather'][0]['description']
            }
            print("weather_info: ", weather_info)
            return jsonify(weather_info)

        error_message = response_data.get('message', 'An error occurred.')
        return jsonify({"error": error_message}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while making the request"}), 500


if __name__ == "__main__":
    app.run("localhost", 90)