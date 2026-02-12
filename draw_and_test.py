# draw_and_test.py
import tkinter as tk
from PIL import Image, ImageDraw
import requests
import io

class DigitDrawer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Draw a Digit")
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, width=280, height=280, bg='white')
        self.canvas.pack()
        
        # Create PIL image for saving
        self.image = Image.new('L', (280, 280), 'white')
        self.draw = ImageDraw.Draw(self.image)
        
        # Bind mouse events
        self.canvas.bind('<B1-Motion>', self.paint)
        
        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()
        
        tk.Button(btn_frame, text='Predict', command=self.predict).pack(side=tk.LEFT)
        tk.Button(btn_frame, text='Clear', command=self.clear).pack(side=tk.LEFT)
        
        self.last_x, self.last_y = None, None
    
    def paint(self, event):
        if self.last_x and self.last_y:
            # Draw on canvas
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                   width=20, fill='black', capstyle=tk.ROUND)
            # Draw on PIL image
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                          fill='black', width=20)
        
        self.last_x = event.x
        self.last_y = event.y
    
    def clear(self):
        self.canvas.delete('all')
        self.image = Image.new('L', (280, 280), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.last_x, self.last_y = None, None
    
    def predict(self):
        # Resize to 28x28
        img = self.image.resize((28, 28))
        
        # Invert (MNIST is white on black)
        img = Image.eval(img, lambda x: 255 - x)
        
        # Send to API
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        url = "http://localhost:8080/predictions/mnist"
        files = {'data': ('image.png', img_bytes, 'image/png')}
        
        try:
            response = requests.post(url, files=files)
            result = response.json()
            print(f"Prediction: {result['digit']}, Confidence: {result['confidence']:.2%}")
            
            # Show in popup
            popup = tk.Toplevel()
            popup.title("Prediction")
            tk.Label(popup, text=f"Predicted Digit: {result['digit']}", 
                    font=('Arial', 24)).pack(padx=20, pady=20)
            tk.Label(popup, text=f"Confidence: {result['confidence']:.2%}",
                    font=('Arial', 14)).pack(padx=20, pady=10)
        except Exception as e:
            print(f"Error: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = DigitDrawer()
    app.run()