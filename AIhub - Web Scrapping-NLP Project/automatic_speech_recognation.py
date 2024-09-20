import requests

token = "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"


def transcribe_audio(model, audio_file_path, token):
    # Hugging Face API URL'si
    api_url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Ses dosyasını API'ye gönderme
    with open(audio_file_path, "rb") as audio_file:
        data = audio_file.read()

    # API'ye POST isteği gönder
    response = requests.post(api_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get('text', 'Sonuç bulunamadı.')
    else:
        return f"Bir hata oluştu: {response.status_code}"
