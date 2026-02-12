import pytest
from unittest.mock import Mock, patch
import io
from PIL import Image

# Mock Flask app for testing
@pytest.fixture
def mock_model():
    with patch('torch.load') as mock_load:
        mock_load.return_value = {}
        yield mock_load

def test_image_preprocessing():
    """Test image preprocessing pipeline"""
    # Create test image
    img = Image.new('L', (28, 28), color=128)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Load and verify
    loaded_img = Image.open(img_bytes)
    assert loaded_img.size == (28, 28)
    assert loaded_img.mode == 'L'

def test_image_inversion():
    """Test image color inversion for MNIST"""
    img = Image.new('L', (28, 28), color=255)  # White
    
    # Invert
    inverted = Image.eval(img, lambda x: 255 - x)
    
    # Check inversion
    assert inverted.getpixel((0, 0)) == 0  # Should be black