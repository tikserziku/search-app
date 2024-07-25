from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='static')
CORS(app)

FOURSQUARE_API_KEY = os.environ.get('FOURSQUARE_API_KEY', 'YOUR_API_KEY_HERE')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search')
def search():
    query = request.args.get('query', '')
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
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
