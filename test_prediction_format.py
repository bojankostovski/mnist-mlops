# test_prediction_format.py
import requests
from PIL import Image, ImageDraw
import io

def draw_digit(digit):
    """Draw different digits"""
    img = Image.new('L', (28, 28), color=255)
    draw = ImageDraw.Draw(img)
    
    if digit == 0:
        # Draw a circle
        draw.ellipse([5, 5, 23, 23], outline=0, width=3)
    elif digit == 1:
        # Draw vertical line
        draw.line([(14, 5), (14, 23)], fill=0, width=3)
    elif digit == 2:
        # Draw a "2"
        draw.arc([5, 5, 20, 15], 0, 180, fill=0, width=3)
        draw.line([(20, 10), (5, 23)], fill=0, width=3)
        draw.line([(5, 23), (23, 23)], fill=0, width=3)
    elif digit == 3:
        # Draw two curves
        draw.arc([5, 5, 20, 15], 0, 180, fill=0, width=3)
        draw.arc([5, 13, 20, 23], 0, 180, fill=0, width=3)
    elif digit == 4:
        # Draw a "4"
        draw.line([(5, 5), (5, 15)], fill=0, width=3)
        draw.line([(5, 15), (20, 15)], fill=0, width=3)
        draw.line([(18, 5), (18, 23)], fill=0, width=3)
    elif digit == 5:
        # Draw a "5"
        draw.line([(5, 5), (20, 5)], fill=0, width=3)
        draw.line([(5, 5), (5, 14)], fill=0, width=3)
        draw.arc([5, 10, 20, 23], 0, 180, fill=0, width=3)
    elif digit == 7:
        # Draw a "7"
        draw.line([(5, 5), (23, 5)], fill=0, width=2)
        draw.line([(18, 5), (10, 23)], fill=0, width=2)
    elif digit == 8:
        # Draw two circles (8)
        draw.ellipse([7, 5, 21, 14], outline=0, width=3)
        draw.ellipse([7, 14, 21, 23], outline=0, width=3)
    elif digit == 9:
        # Draw a "9"
        draw.ellipse([7, 5, 21, 15], outline=0, width=3)
        draw.line([(20, 10), (20, 23)], fill=0, width=3)
    else:
        # Default to simple vertical line
        draw.line([(14, 5), (14, 23)], fill=0, width=3)
    
    return img

# Test different digits
for test_digit in [0, 1, 2, 3, 4, 5, 7, 8, 9]:
    img = draw_digit(test_digit)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    # Send to TorchServe
    url = "http://localhost:8080/predictions/mnist"
    files = {'data': ('image.png', img_bytes, 'image/png')}
    
    response = requests.post(url, files=files)
    result = response.json()
    
    print(f"Drew: {test_digit} → Predicted: {result['digit']} (confidence: {result['confidence']:.2%})")
    
    # Save image to see what was sent
    img.save(f'test_digit_{test_digit}.png')

print("\nSaved test images as test_digit_X.png - check them out!")