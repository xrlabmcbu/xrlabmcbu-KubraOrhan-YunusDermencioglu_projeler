import time
import requests

def generate_text(text_prompt, model):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    api_key = "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"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "inputs": text_prompt,
        "parameters": {
            "max_length": 100,
            "num_return_sequences": 1
        }
    }
    
    # Simulate model loading delay
    delay = 10
    print(f"Model yükleniyor, lütfen {delay} saniye bekleyin...")
    time.sleep(delay)

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        generated_text = response.json()[0]["generated_text"]
        return {"generated_text": generated_text}
    else:
        return {"error": f"Hata: {response.status_code} - {response.text}"}