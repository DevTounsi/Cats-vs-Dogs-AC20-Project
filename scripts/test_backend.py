import sys
import os
# Add root path to sys.path so we can import from workspace root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
import torch.nn as nn
import torchvision.models as tv_models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

# Import GradCAM and hooks finder
from gradcam import GradCAM, find_last_conv_layer, overlay_heatmap_on_image

class UniversalCNN(nn.Module):
    def __init__(self, use_batch_norm=False, dropout_rate=0.0):
        super(UniversalCNN, self).__init__()
        layers = []
        in_channels = 3
        out_channels = 16
        for _ in range(5):
            layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1))
            if use_batch_norm:
                layers.append(nn.BatchNorm2d(out_channels))
            layers.append(nn.ReLU())
            layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            in_channels = out_channels
            out_channels *= 2
        self.features = nn.Sequential(*layers)
        
        classifier_layer = [
            nn.Flatten(),
            nn.Linear((out_channels//2)*8*8, 256),
        ]
        if dropout_rate > 0:
            classifier_layer.append(nn.Dropout(dropout_rate))
        classifier_layer.append(nn.ReLU())
        classifier_layer.append(nn.Linear(256, 2))
        self.classifier = nn.Sequential(*classifier_layer)
        
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def test_models():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=== Testing Backend Models on {device} ===")
    
    # 1. Test Baseline CNN
    try:
        model_basic = UniversalCNN(use_batch_norm=False, dropout_rate=0.0)
        model_basic.load_state_dict(torch.load('models/best_model_epoch_7.pth', map_location=device))
        model_basic.eval()
        print("[OK] Baseline CNN loaded successfully.")
    except Exception as e:
        print("[FAIL] Baseline CNN loading failed:", e)
        return False
        
    # 2. Test Optimized CNN
    try:
        model_opt = UniversalCNN(use_batch_norm=True, dropout_rate=0.5)
        model_opt.load_state_dict(torch.load('models/optimized_model.pth', map_location=device))
        model_opt.eval()
        print("[OK] Optimized CNN loaded successfully.")
    except Exception as e:
        print("[FAIL] Optimized CNN loading failed:", e)
        return False
        
    # 3. Test Transfer Learning (ResNet50)
    try:
        model_tl = tv_models.resnet50()
        model_tl.fc = nn.Linear(model_tl.fc.in_features, 2)
        model_tl.load_state_dict(torch.load('models/tl_model.pth', map_location=device))
        model_tl.eval()
        print("[OK] ResNet50 Transfer Learning loaded successfully.")
    except Exception as e:
        print("[FAIL] ResNet50 loading failed:", e)
        return False
        
    # 4. Test YOLOv8
    try:
        from ultralytics import YOLO
        model_yolo = YOLO('models/yolov8n.pt')
        print("[OK] YOLOv8 loaded successfully.")
    except Exception as e:
        print("[FAIL] YOLOv8 loading failed:", e)
        return False
        
    # 5. Test Grad-CAM Hooks & Heatmap on dummy image
    print("\n--- Testing Grad-CAM hook logic ---")
    dummy_img = torch.randn(1, 3, 256, 256)
    
    # Baseline
    last_conv_basic = find_last_conv_layer(model_basic)
    if last_conv_basic is not None:
        gcam_basic = GradCAM(model_basic, last_conv_basic)
        heatmap = gcam_basic.generate_heatmap(dummy_img, class_idx=0)
        gcam_basic.remove_hooks()
        print(f"[OK] Baseline Grad-CAM hook successful. Heatmap shape: {heatmap.shape}")
        
        # Test image overlay (create a temporary dummy input image)
        temp_img_path = 'temp_test_img.jpg'
        try:
            Image.new('RGB', (256, 256), color='red').save(temp_img_path)
            overlay = overlay_heatmap_on_image(temp_img_path, heatmap)
            print(f"[OK] Overlay helper generated successfully (PIL Image).")
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
        except Exception as overlay_err:
            print(f"[FAIL] Overlay helper failed: {overlay_err}")
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            return False
    else:
        print("[FAIL] Could not find last conv layer in Baseline CNN.")
        return False
        
    print("\n=== All Tests Passed Successfully! ===")
    return True

if __name__ == "__main__":
    test_models()
