from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import requests
import os
import logging

app = Flask(__name__, static_folder='static')
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

FOURSQUARE_API_KEY = os.environ.get('FOURSQUARE_API_KEY', 'YOUR_API_KEY_HERE')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search')
def search():
    query = request.args.get('query', '')
    app.logger.info(f"Получен запрос на поиск: {query}")
    
    url = 'https://api.foursquare.com/v3/places/search'
    params = {
        'query': query,
        'near': 'Висагинас,LT',
        'limit': 10
    }
    headers = {
        'Accept': 'application/json',
        'Authorization': FOURSQUARE_API_KEY
    }
    
    try:
        app.logger.info(f"Отправка запроса к Foursquare API: {url}")
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        app.logger.info(f"Получен ответ от Foursquare API: {response.status_code}")
        return jsonify(data)
    except requests.RequestException as e:
        app.logger.error(f"Ошибка при запросе к Foursquare API: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error(f"Неожиданная ошибка: {str(e)}")
        return jsonify({'error': 'Произошла неожиданная ошибка'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
