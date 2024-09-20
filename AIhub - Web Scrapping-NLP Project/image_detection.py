import requests
import time
from flask import jsonify

# Hugging Face API Token
headers = {
    "Authorization": f"Bearer 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"
}

def detect_objects(model, image_path):
    api_url = f"https://api-inference.huggingface.co/models/{model}"

    # Görsel dosyasını yükleme
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except OSError as e:
        return jsonify({"error": f"Dosya açılamadı: {e}"}), 400

    # API'ye istekte bulunma
    for attempt in range(5):  # Try up to 5 times
        response = requests.post(api_url, headers=headers, data=image_data)
        
        # Yanıtı kontrol et
        try:
            result = response.json()
        except ValueError as e:
            return jsonify({"error": f"Yanıt JSON formatında değil: {e}"}), 500

        if 'error' in result:
            if result['error'].startswith('Model'):
                time.sleep(18)  # Model yükleniyor, biraz bekleyin ve tekrar deneyin
            else:
                return jsonify({"error": result['error']}), 500
        else:
            if result:
                # İlk 10 tespiti sıralama ve yüzdelik formatta sonuçları döndürme
                sorted_result = sorted(result, key=lambda x: x.get('score', 0), reverse=True)[:10]
                return jsonify({"results": sorted_result}), 200
            else:
                return jsonify({"error": "Tespit sonuçları bulunamadı. Görseli ve modeli kontrol edin."}), 400
