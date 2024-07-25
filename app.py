from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__, static_folder='static')
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    app.logger.info("Запрошена главная страница")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/v1/get', methods=['GET'])
def api_get():
    url = request.args.get('url')
    app.logger.info(f"Получен API запрос с URL: {url}")
    
    if not url:
        app.logger.warning("Отсутствует URL в запросе")
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        response = requests.get(url)
        app.logger.info(f"Ответ получен: статус {response.status_code}")
        return jsonify({
            "status_code": response.status_code,
            "content": response.text,
            "headers": dict(response.headers)
        })
    except requests.RequestException as e:
        app.logger.error(f"Ошибка при выполнении запроса: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
