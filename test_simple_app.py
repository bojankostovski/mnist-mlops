# test_simple_web.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/test')
def test():
    try:
        # Test calling TorchServe
        response = requests.get('http://localhost:8080/ping', timeout=5)
        return jsonify({
            'torchserve_status': response.status_code,
            'torchserve_response': response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, port=5001)
