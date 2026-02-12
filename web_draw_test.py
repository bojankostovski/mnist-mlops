from flask import Flask, request, jsonify, render_template  # Changed: added render_template
import requests
import base64
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # FIX: Use template file

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Process image
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('L')
        image = image.resize((28, 28))
        
        # Invert colors (MNIST is white on black)
        image = Image.eval(image, lambda x: 255 - x)
        
        # Send to Kubernetes deployment
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        # Call the Kubernetes service
        url = "http://localhost:8080/predictions/mnist"
        files = {'data': ('image.png', img_bytes, 'image/png')}
        
        response = requests.post(url, files=files, timeout=10)
        result = response.json()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎨 MNIST Drawing App")
    print("=" * 60)
    print("1. Make sure port-forward is running:")
    print("   kubectl port-forward -n kubeflow svc/mnist-torchserve 8080:8080")
    print()
    print("2. Open your browser to: http://localhost:5001")
    print("=" * 60)
    
    # FIX: Use environment variables for configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # Default to localhost only
    
    app.run(debug=debug_mode, host=host, port=5001)