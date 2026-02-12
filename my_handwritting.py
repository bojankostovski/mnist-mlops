# test_my_handwriting.py
import requests
from PIL import Image
import io

# 1. Draw a digit on white paper with black pen
# 2. Take a photo or scan it
# 3. Crop to just the digit
# 4. Save as 'my_digit.jpg'

# Load your handwritten digit
img = Image.open('my_digit.jpg')

# Convert to grayscale and resize to 28x28
img = img.convert('L')
img = img.resize((28, 28))

# Optionally invert if your digit is black on white
# (MNIST expects white digit on black background)
# img = Image.eval(img, lambda x: 255 - x)

# Save to see what the model will see
img.save('processed_digit.png')
print("Saved processed image to processed_digit.png - check if it looks right!")

# Send to API
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_bytes = img_byte_arr.getvalue()

url = "http://localhost:8080/predictions/mnist"
files = {'data': ('image.png', img_bytes, 'image/png')}

response = requests.post(url, files=files)
print(f"Prediction: {response.json()}")