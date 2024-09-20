import requests
import time

# Hugging Face API ile görsel sınıflandırma fonksiyonu
def classify_image(model_name, image_path):
    # Hugging Face API URL
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    # Hugging Face API Token
    headers = {
        "Authorization": f"Bearer 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"
    }

    # Görsel dosyasını yükleme
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except OSError as e:
        return {'error': f'Dosya açılamadı: {e}'}

    # API'ye istekte bulunma
    for attempt in range(5):  # Try up to 5 times
        response = requests.post(api_url, headers=headers, data=image_data)
        result = response.json()

        if 'error' in result:
            if result['error'].startswith('Model'):
                print(f"Model yükleniyor, tahmini süre: {result.get('estimated_time', 'bilinmiyor')} saniye")
                time.sleep(30)  # Wait before retrying
            else:
                return {'error': f'Bir hata oluştu: {result["error"]}'}
        else:
            # Sonuçları yüzdelik formatta döndür
            return [{"label": item['label'], "score": item['score'] * 100} for item in result]

    return {'error': 'Model yüklenmedi, lütfen tekrar deneyin.'}
