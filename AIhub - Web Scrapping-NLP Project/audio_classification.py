import requests

def classify_audio(model, audio_path):
    # Dosya yolundaki "\" ifadelerini "/" ile değiştir
    audio_path = audio_path.replace("\\", "/")
    
    # Hugging Face API URL'si
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Hugging Face API Token
    headers = {
        "Authorization": "Bearer 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"
    }
    
    # Ses dosyasını aç
    try:
        with open(audio_path, 'rb') as audio_file:
            data = audio_file.read()
    except FileNotFoundError:
        return {"error": "Ses dosyası bulunamadı."}
    
    # API'ye POST isteği gönder
    try:
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()  # HTTPError için
    except requests.exceptions.RequestException as e:
        return {"error": f"API isteğinde bir hata oluştu: {str(e)}"}
    
    # Yanıtı kontrol et ve işle
    if response.status_code == 200:
        output = response.json()
        return output
    else:
        return {"error": f"Bir hata oluştu: {response.status_code}"}