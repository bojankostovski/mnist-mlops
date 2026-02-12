import requests
import base64
from PIL import Image, ImageDraw
import io

# Create a simple test image (a "7")
def create_test_image():
    img = Image.new('L', (28, 28), color=255)  # White background
    draw = ImageDraw.Draw(img)
    
    # Draw a simple "7"
    draw.line((5, 5, 23, 5), fill=0, width=2)  # Top horizontal
    draw.line((18, 5, 10, 23), fill=0, width=2)  # Diagonal
    
    return img

# Convert image to base64
img = create_test_image()
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_byte_arr = img_byte_arr.getvalue()
img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

# Test the API
url = "http://localhost:8080/predictions/mnist"

payload = {
    "data": img_base64
}

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print(f"Error: {e}")
