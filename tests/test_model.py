# import pytest
import torch
from model import ImprovedNet

def test_model_initialization():
    """Test that model initializes correctly"""
    model = ImprovedNet()
    assert model is not None

def test_model_forward_pass():
    """Test model forward pass with dummy input"""
    model = ImprovedNet()
    model.eval()
    
    # Create dummy input (batch_size=1, channels=1, height=28, width=28)
    dummy_input = torch.randn(1, 1, 28, 28)
    
    # Forward pass
    output = model(dummy_input)
    
    # Check output shape (batch_size=1, num_classes=10)
    assert output.shape == (1, 10)

def test_model_output_range():
    """Test that model output is log probabilities"""
    model = ImprovedNet()
    model.eval()
    
    dummy_input = torch.randn(1, 1, 28, 28)
    output = model(dummy_input)
    
    # Log probabilities should be negative
    assert torch.all(output <= 0)

def test_model_parameters():
    """Test that model has expected number of parameters"""
    model = ImprovedNet()
    
    total_params = sum(p.numel() for p in model.parameters())
    
    # Should have around 400k parameters
    assert 300000 < total_params < 500000