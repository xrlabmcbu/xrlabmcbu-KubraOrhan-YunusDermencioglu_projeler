import requests

def generate_audio(model, text_prompt):
    # Hugging Face API URL'si
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Hugging Face API Token
    headers = {
        "Authorization": f"Bearer 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"
    }
    
    # Metni API'ye gönderme
    data = {
        "inputs": text_prompt
    }
    
    # API'ye POST isteği gönder
    response = requests.post(api_url, headers=headers, json=data)
    
    # Yanıtı kontrol et ve işle
    if response.status_code == 200:
        # Yanıtı 'text-to-audio.mp3' dosyasına kaydet
        file_path = "static/text-to-audio.mp3"
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        raise Exception(f"Bir hata oluştu: {response.status_code}, {response.text}")
