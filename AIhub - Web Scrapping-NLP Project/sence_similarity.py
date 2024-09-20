import time
import requests

def get_similarity_score(original_sentence, sentences, model):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": "Bearer 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"
    }
    payload = {
        "inputs": {
            "source_sentence": original_sentence,
            "sentences": sentences
        }
    }
    
    while True:
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 503:
            error_message = response.json().get("error", "")
            if "currently loading" in error_message:
                print(f"Model yükleniyor, tahmini süre: {error_message.split(' ')[-1]} saniye. Tekrar deneniyor...")
                time.sleep(30)
            else:
                return {"error": f"Model yüklenirken hata oluştu: {error_message}"}
        elif response.status_code != 200:
            return {"error": f"API çağrısı başarısız oldu. Durum Kodu: {response.status_code}"}
        
        try:
            result = response.json()
            if isinstance(result, list):
                return [score * 100 for score in result]
            else:
                return {"error": "Beklenmeyen yanıt formatı veya benzerlik skoru bulunamadı."}
        except ValueError as e:
            return {"error": f"Yanıt JSON formatında değil: {e}"}
        except Exception as e:
            return {"error": f"Bir hata oluştu: {e}"}