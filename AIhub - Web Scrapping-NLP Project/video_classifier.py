import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import requests
import io
from torchvision.models import resnet50, ResNet50_Weights

# Modeli güncel şekilde yükleme
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Sınıf isimlerini yükleme
url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
response = requests.get(url)
labels = response.json()

def process_frame(frame):
    # BGR'yi RGB'ye dönüştürme ve görüntüyü PIL formatına çevirme
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    
    # Görüntüyü ön işleme
    input_tensor = preprocess(pil_image)
    input_batch = input_tensor.unsqueeze(0)
    
    # Model tahmini
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    # En yüksek olasılıklı sınıfları bulma
    top3_prob, top3_catid = torch.topk(probabilities, 3)
    
    # Sonuçları döndürme
    frame_results = {
        "Top 1 Class": labels[top3_catid[0].item()],
        "Top 1 Probability": top3_prob[0].item() * 100,
        "Top 2 Class": labels[top3_catid[1].item()],
        "Top 2 Probability": top3_prob[1].item() * 100,
        "Top 3 Class": labels[top3_catid[2].item()],
        "Top 3 Probability": top3_prob[2].item() * 100
    }
    
    return frame_results

