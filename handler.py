# handler.py
import torch
import logging
from torchvision import transforms
from ts.torch_handler.base_handler import BaseHandler
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)

class MNISTDigitHandler(BaseHandler):
    
    def initialize(self, context):
        """Load the model"""
        logger.info("Initializing MNIST handler...")
        
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        
        # Import model class
        from model import ImprovedNet
        
        # Create model
        self.model = ImprovedNet()
        
        # Load weights
        state_dict_path = f"{model_dir}/mnist_model_best.pt"
        logger.info(f"Loading model from {state_dict_path}")
        
        self.model.load_state_dict(
            torch.load(state_dict_path, map_location='cpu')
        )
        self.model.eval()
        
        # Preprocessing
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        self.initialized = True
        logger.info("MNIST handler initialized successfully")
    
    def preprocess(self, data):
        """Preprocess the input data - handle multiple input formats"""
        logger.info(f"Received {len(data)} requests")
        images = []
        
        for idx, row in enumerate(data):
            try:
                image_bytes = None
                
                # Try different ways to get the image data
                if isinstance(row, dict):
                    # Try 'body' first (file upload)
                    image_bytes = row.get("body")
                    logger.info(f"Got from body: {type(image_bytes)}")
                    
                    # If body is None or not bytes, try 'data'
                    if not image_bytes:
                        image_bytes = row.get("data")
                        logger.info(f"Got from data: {type(image_bytes)}")
                elif isinstance(row, bytes):
                    # Raw bytes
                    image_bytes = row
                    logger.info(f"Got raw bytes: {len(image_bytes)}")
                
                # If still None, log all keys
                if image_bytes is None:
                    logger.error(f"Could not find image data. Row keys: {row.keys() if isinstance(row, dict) else type(row)}")
                    logger.error(f"Row content: {row}")
                    raise ValueError("No image data found in request")
                
                # Handle base64 if it's a string
                if isinstance(image_bytes, str):
                    logger.info("Decoding base64")
                    image_bytes = base64.b64decode(image_bytes)
                
                # Open image
                image = Image.open(io.BytesIO(image_bytes))
                logger.info(f"Image loaded: mode={image.mode}, size={image.size}")
                
                # Transform
                image_tensor = self.transform(image)
                images.append(image_tensor)
                
            except Exception as e:
                logger.error(f"Error preprocessing: {e}", exc_info=True)
                raise
        
        batch = torch.stack(images)
        logger.info(f"Batch shape: {batch.shape}")
        return batch
    
    def inference(self, data):
        """Run inference"""
        with torch.no_grad():
            outputs = self.model(data)
            probabilities = torch.softmax(outputs, dim=1)
        return probabilities
    
    def postprocess(self, inference_output):
        """Post-process predictions"""
        predictions = []
        for output in inference_output:
            digit = output.argmax().item()
            confidence = output[digit].item()
            predictions.append({
                "digit": int(digit),
                "confidence": float(confidence)
            })
        return predictions