import numpy as np
import torch
import torch.nn as nn
from PIL import Image
import matplotlib.pyplot as plt

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.activations = None
        self.gradients = None
        
        # Register hooks
        self.forward_hook = target_layer.register_forward_hook(self.save_activation)
        try:
            self.backward_hook = target_layer.register_full_backward_hook(self.save_gradient)
        except AttributeError:
            # Fallback for older PyTorch versions
            self.backward_hook = target_layer.register_backward_hook(self.save_gradient)
            
    def save_activation(self, module, input, output):
        self.activations = output
        
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]
        
    def generate_heatmap(self, input_tensor, class_idx):
        # Ensure gradients are cleared
        self.model.zero_grad()
        
        # Forward pass
        output = self.model(input_tensor)
        
        # If class_idx is None, use the predicted class
        if class_idx is None:
            class_idx = torch.argmax(output, dim=1).item()
            
        # Backward pass
        score = output[0, class_idx]
        score.backward()
        
        # Get activations and gradients
        if self.gradients is None or self.activations is None:
            # Return empty heatmap if hooks failed to capture
            return np.zeros((input_tensor.shape[2], input_tensor.shape[3]), dtype=np.float32)
            
        gradients = self.gradients.detach()
        activations = self.activations.detach()
        
        # GAP (Global Average Pooling) over gradients
        weights = torch.mean(gradients, dim=(2, 3), keepdim=True)
        
        # Weighted combination of activation channels
        heatmap = torch.sum(weights * activations, dim=1).squeeze()
        
        # ReLU on heatmap
        heatmap = torch.clamp(heatmap, min=0)
        
        # Normalize
        heatmap_max = torch.max(heatmap)
        if heatmap_max > 0:
            heatmap = heatmap / heatmap_max
            
        return heatmap.cpu().numpy()
        
    def remove_hooks(self):
        self.forward_hook.remove()
        self.backward_hook.remove()

def find_last_conv_layer(model):
    """
    Traverses the model in reverse to find the last Conv2d layer.
    """
    for name, module in reversed(list(model.named_modules())):
        if isinstance(module, nn.Conv2d):
            return module
    return None

def overlay_heatmap_on_image(original_image_path, heatmap, alpha=0.5):
    """
    Overlays a Grad-CAM heatmap on the original image using PIL and Matplotlib.
    original_image_path: Path to the original image
    heatmap: 2D numpy array (normalized 0 to 1) representing the heatmap
    """
    # Open original image with PIL
    img_pil = Image.open(original_image_path).convert('RGB')
    w, h = img_pil.size
    
    # Resize heatmap to match original image size using PIL
    # We convert heatmap to PIL Image first
    heatmap_pil = Image.fromarray((heatmap * 255).astype(np.uint8))
    heatmap_pil_resized = heatmap_pil.resize((w, h), Image.Resampling.BILINEAR)
    heatmap_resized = np.array(heatmap_pil_resized) / 255.0
    
    # Apply matplotlib colormap (jet)
    cm = plt.get_cmap('jet')
    heatmap_colored = cm(heatmap_resized)  # Shape (h, w, 4), values in [0, 1]
    
    # Remove alpha channel and scale to 255
    heatmap_colored_rgb = (heatmap_colored[:, :, :3] * 255).astype(np.uint8)
    
    # Mix the original image and colored heatmap
    original_np = np.array(img_pil)
    overlay_np = (original_np * (1.0 - alpha) + heatmap_colored_rgb * alpha).astype(np.uint8)
    
    # Convert back to PIL Image
    overlay_pil = Image.fromarray(overlay_np)
    return overlay_pil
