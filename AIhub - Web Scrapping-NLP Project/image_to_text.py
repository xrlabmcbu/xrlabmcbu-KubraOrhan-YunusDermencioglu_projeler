import requests
from PIL import Image
import os

API_TOKEN = "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"

def process_image_with_model(image_path, model_name, api_token):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    # Dönüştürülmüş görselin yolunu oluştur
    base, ext = os.path.splitext(image_path)
    converted_image_path = f"{base}_converted.png"
    
    # Görseli dönüştürme
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.save(converted_image_path, format="PNG")
    
    if not os.path.isfile(converted_image_path):
        raise FileNotFoundError(f"Dosya bulunamadı: {converted_image_path}")
    
    # API'ye istekte bulunma
    for attempt in range(5):  # Try up to 5 times
        try:
            with open(converted_image_path, "rb") as f:
                image_data = f.read()
                response = requests.post(api_url, headers=headers, data=image_data)
            
            if response.status_code == 503:
                error_info = response.json()
                print(f"Model yükleniyor, tahmini süre: {error_info.get('estimated_time', 'bilinmiyor')} saniye")
                continue
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("generated_text", "Yanıtta metin bulunamadı.")
                    else:
                        return f"Yanıt beklenen formatta değil: {result}"
                except requests.exceptions.JSONDecodeError:
                    return f"JSON decode hatası. Yanıt JSON formatında değil. Yanıt içeriği: {response.text}"
            else:
                if "Internal Server Error" in response.text:
                    return "Bir hata oluştu: Sunucu hatası."
                else:
                    return f"Bir hata oluştu: {response.text}"
                
        except Exception as e:
            return f"Bir hata oluştu: {e}"
        
    return "İstek başarıyla tamamlanamadı."

def remove_converted_image(image_path):
    base, ext = os.path.splitext(image_path)
    converted_image_path = f"{base}_converted.png"
    
    if os.path.isfile(converted_image_path):
        os.remove(converted_image_path)
