import requests

def classify_token(model_name, text_prompt):
    # Hugging Face API URL'si
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    # Hugging Face API Token
    headers = {
        "Authorization": "Bearer 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"
    }

    # Metni API'ye gönderme
    data = {
        "inputs": text_prompt
    }

    # API'ye POST isteği gönder
    response = requests.post(api_url, headers=headers, json=data)

    # Yanıtı kontrol et ve işle
    if response.status_code == 200:
        output = response.json()
        # Sonuçları işleyin
        top_results = [
            {
                'word': entity['word'],
                'entity_type': entity['entity_group'],
                'score': entity['score'] * 100  # Yüzdelik formata dönüştürme
            }
            for entity in output
        ]
        return top_results
    else:
        return {"error": f"Bir hata oluştu: {response.status_code}"}
