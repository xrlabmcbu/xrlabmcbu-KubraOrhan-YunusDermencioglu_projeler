import requests
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os
import json
import time
from flask import jsonify

def segment_image(image_path, model_name):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {
        "Authorization": "Bearer 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"
    }

    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except OSError as e:
        return jsonify({'error': f"Dosya açılamadı: {e}"}), 500

    # API'ye istekte bulunma
    for attempt in range(5):
        response = requests.post(api_url, headers=headers, data=image_data)
        result = response.json()

        if isinstance(result, list):
            # İlk segmentasyon maskesini işleyelim ve döndürelim
            for idx, item in enumerate(result):
                if 'mask' in item:
                    mask_base64 = item['mask']
                    try:
                        mask_bytes = base64.b64decode(mask_base64)
                        mask_image = Image.open(BytesIO(mask_bytes))

                        # Maskeyi bir dosya olarak kaydet
                        mask_output_path = os.path.join('static', f'mask_segment_{idx}.png')
                        mask_image.save(mask_output_path)

                        return jsonify({'image_url': f'/static/mask_segment_{idx}.png'})

                    except Exception as e:
                        return jsonify({'error': f"Maskeyi işleme sırasında hata: {e}"}), 500
                else:
                    return jsonify({'error': f"Segment {idx} mask içermiyor."}), 500
            break
        else:
            time.sleep(30)  # Bekle ve tekrar dene

    return jsonify({'error': 'Model yüklenmedi, lütfen tekrar deneyin.'}), 503
