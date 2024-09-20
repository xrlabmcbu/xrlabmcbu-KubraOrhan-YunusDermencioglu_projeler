import requests

# Hugging Face API URL ve Token
API_TOKEN = "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"

def summarize_text(model, text):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # API'ye istekte bulunma
    response = requests.post(api_url, headers=headers, json={"inputs": text})

    try:
        result = response.json()
        # Sonuçları yazdırma
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get('summary_text', 'Özet bulunamadı.')
            return summary
        else:
            return "Beklenmeyen yanıt formatı veya özet bulunamadı."
    except ValueError as e:
        return f"Yanıt JSON formatında değil: {e}"
    except Exception as e:
        return f"Bir hata oluştu: {e}"
