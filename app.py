import sys
import os
import time
import base64
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

import torch
import torch.nn as nn
import torchvision.models as tv_models
import torchvision.transforms as transforms
from ultralytics import YOLO

# Import Grad-CAM utilities from gradcam.py
from gradcam import GradCAM, find_last_conv_layer, overlay_heatmap_on_image

# 1. Define model architecture class UniversalCNN (same as in notebooks)
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

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Load device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Loading PyTorch models on: {device}")

# Load models
# Baseline CNN
model_basic = UniversalCNN(use_batch_norm=False, dropout_rate=0.0)
model_basic.load_state_dict(torch.load('models/best_model_epoch_7.pth', map_location=device))
model_basic.to(device)
model_basic.eval()

# Optimized CNN
model_opt = UniversalCNN(use_batch_norm=True, dropout_rate=0.5)
model_opt.load_state_dict(torch.load('models/optimized_model.pth', map_location=device))
model_opt.to(device)
model_opt.eval()

# ResNet50 Transfer Learning
model_tl = tv_models.resnet50()
model_tl.fc = nn.Linear(model_tl.fc.in_features, 2)
model_tl.load_state_dict(torch.load('models/tl_model.pth', map_location=device))
model_tl.to(device)
model_tl.eval()

# YOLOv8
print("Loading YOLOv8 model...")
model_yolo = YOLO('models/yolov8n.pt')
model_yolo.to(device)
print("Models loaded successfully!")

# Define transforms
transform_cnn = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

transform_tl = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Veuillez uploader une image.'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné.'}), 400
        
    # Get ground truth label to mark prediction errors
    true_class = request.form.get('true_class', '').strip().lower() # 'cat' or 'dog' or 'none'
    
    if not os.path.exists('temp'):
        os.makedirs('temp')
        
    filename = secure_filename(file.filename)
    img_path = os.path.join('temp', f"{int(time.time())}_{filename}")
    file.save(img_path)
    
    try:
        # Load image with PIL
        img_pil = Image.open(img_path).convert('RGB')
        results = {}
        
        # 1. Baseline CNN Infe & Grad-CAM
        t_start = time.time()
        img_tensor = transform_cnn(img_pil).unsqueeze(0).to(device)
        
        last_conv = find_last_conv_layer(model_basic)
        gcam = GradCAM(model_basic, last_conv)
        
        with torch.enable_grad(): # Grad-CAM needs gradients
            output = model_basic(img_tensor)
            probs = torch.softmax(output, dim=1).squeeze()
            pred_idx = torch.argmax(probs).item()
            pred_prob = probs[pred_idx].item()
            heatmap = gcam.generate_heatmap(img_tensor, pred_idx)
            gcam.remove_hooks()
            
        overlay_pil = overlay_heatmap_on_image(img_path, heatmap)
        buffered = BytesIO()
        overlay_pil.save(buffered, format="JPEG")
        basic_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        t_end = time.time()
        
        pred_label = "cat" if pred_idx == 0 else "dog"
        is_error = (pred_label != true_class) if true_class in ['cat', 'dog'] else False
        
        results['baseline'] = {
            'label': 'Chat' if pred_label == 'cat' else 'Chien',
            'confidence': float(pred_prob * 100),
            'time_ms': float((t_end - t_start) * 1000),
            'is_error': bool(is_error),
            'image_b64': basic_b64
        }
        
        # 2. Optimized CNN Infe & Grad-CAM
        t_start = time.time()
        img_tensor = transform_cnn(img_pil).unsqueeze(0).to(device)
        
        last_conv = find_last_conv_layer(model_opt)
        gcam = GradCAM(model_opt, last_conv)
        
        with torch.enable_grad():
            output = model_opt(img_tensor)
            probs = torch.softmax(output, dim=1).squeeze()
            pred_idx = torch.argmax(probs).item()
            pred_prob = probs[pred_idx].item()
            heatmap = gcam.generate_heatmap(img_tensor, pred_idx)
            gcam.remove_hooks()
            
        overlay_pil = overlay_heatmap_on_image(img_path, heatmap)
        buffered = BytesIO()
        overlay_pil.save(buffered, format="JPEG")
        opt_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        t_end = time.time()
        
        pred_label = "cat" if pred_idx == 0 else "dog"
        is_error = (pred_label != true_class) if true_class in ['cat', 'dog'] else False
        
        results['optimized'] = {
            'label': 'Chat' if pred_label == 'cat' else 'Chien',
            'confidence': float(pred_prob * 100),
            'time_ms': float((t_end - t_start) * 1000),
            'is_error': bool(is_error),
            'image_b64': opt_b64
        }
        
        # 3. ResNet50 TL Infe & Grad-CAM
        t_start = time.time()
        img_tensor_tl = transform_tl(img_pil).unsqueeze(0).to(device)
        
        # Find ResNet50's last conv layer
        last_conv_resnet = None
        for name, module in reversed(list(model_tl.named_modules())):
            if isinstance(module, nn.Conv2d):
                last_conv_resnet = module
                break
                
        gcam = GradCAM(model_tl, last_conv_resnet)
        
        with torch.enable_grad():
            output = model_tl(img_tensor_tl)
            probs = torch.softmax(output, dim=1).squeeze()
            pred_idx = torch.argmax(probs).item()
            pred_prob = probs[pred_idx].item()
            heatmap = gcam.generate_heatmap(img_tensor_tl, pred_idx)
            gcam.remove_hooks()
            
        overlay_pil = overlay_heatmap_on_image(img_path, heatmap)
        buffered = BytesIO()
        overlay_pil.save(buffered, format="JPEG")
        tl_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        t_end = time.time()
        
        pred_label = "cat" if pred_idx == 0 else "dog"
        is_error = (pred_label != true_class) if true_class in ['cat', 'dog'] else False
        
        results['resnet'] = {
            'label': 'Chat' if pred_label == 'cat' else 'Chien',
            'confidence': float(pred_prob * 100),
            'time_ms': float((t_end - t_start) * 1000),
            'is_error': bool(is_error),
            'image_b64': tl_b64
        }
        
        # 4. YOLOv8 Detection
        t_start = time.time()
        # Run YOLOv8 on original resolution
        yolo_results = model_yolo(img_path, verbose=False)
        t_end = time.time()
        
        # Draw bounding boxes (YOLOv8 can automatically draw on the image with results[0].plot())
        plot_arr = yolo_results[0].plot()
        # OpenCV plot returns BGR array, convert to RGB
        plot_arr_rgb = plot_arr[:, :, ::-1]
        yolo_pil = Image.fromarray(plot_arr_rgb)
        
        # Convert to Base64
        buffered = BytesIO()
        yolo_pil.save(buffered, format="JPEG")
        yolo_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Check detections
        boxes = yolo_results[0].boxes
        best_conf = -1
        best_cls = -1
        
        # 15: cat, 16: dog in COCO
        for box in boxes:
            cls = int(box.cls.item())
            conf = box.conf.item()
            if cls in [15, 16]:
                if conf > best_conf:
                    best_conf = conf
                    best_cls = cls
                    
        yolo_label = "none"
        if best_cls == 15:
            yolo_label = "cat"
        elif best_cls == 16:
            yolo_label = "dog"
            
        yolo_error = False
        if true_class in ['cat', 'dog']:
            if yolo_label != true_class:
                yolo_error = True
                
        results['yolo'] = {
            'label': 'Chat' if yolo_label == 'cat' else ('Chien' if yolo_label == 'dog' else 'Aucun (Non détecté)'),
            'confidence': float(best_conf * 100) if best_conf != -1 else 0.0,
            'time_ms': float((t_end - t_start) * 1000),
            'is_error': bool(yolo_error),
            'image_b64': yolo_b64
        }
        
        # Cleanup temp file
        if os.path.exists(img_path):
            os.remove(img_path)
            
        return jsonify(results)
        
    except Exception as e:
        if os.path.exists(img_path):
            os.remove(img_path)
        print("API Error:", str(e))
        return jsonify({'error': f"Erreur pendant l'analyse : {str(e)}"}), 500

if __name__ == '__main__':
    # Run server on port 7860 (default for Hugging Face Spaces)
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port, debug=True)
