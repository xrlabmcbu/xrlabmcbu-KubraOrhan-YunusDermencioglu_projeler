import os
import base64
import json
import requests
import time
from flask import jsonify

def process_image(file_path, text_description, model_name):
    # Görseli base64 formatına dönüştürme
    with open(file_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

    # API'ye istek gönderme
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": image_base64,
        "parameters": {
            "text": text_description
        }
    }

    for attempt in range(5):  # Try up to 5 times
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))

            if response.status_code == 503:
                # Model yükleniyorsa bekleme süresi
                error_info = response.json()
                print(f"Model yükleniyor, tahmini süre: {error_info.get('estimated_time', 'bilinmiyor')} saniye")
                time.sleep(30)  # Modelin yüklenmesini bekle ve tekrar dene
                continue

            if response.status_code == 200:
                # Yanıtı bir dosya olarak kaydetme
                output_image_path = os.path.join('static', 'output_image.jpg')
                with open(output_image_path, "wb") as f:
                    f.write(response.content)
                return jsonify({'image_url': '/static/output_image.jpg', 'message': ''})

            else:
                return jsonify({'error': f'Error: {response.status_code} - {response.text}'}), response.status_code

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            time.sleep(30)  # Gecikme süresi

    return jsonify({'error': 'Model yüklenmedi, lütfen tekrar deneyin.'}), 503
