import requests

def classify_text(text_prompt, model):
    
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer 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"
    }
    data = {
        "inputs": text_prompt
    }
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        output = response.json()
        top_results = sorted(output[0], key=lambda x: x['score'], reverse=True)[:5]
        results = [{"label": item['label'], "score": f"{item['score'] * 100:.2f}%"} for item in top_results]
        return results
    else:
        return {"error": f"Bir hata oluştu: {response.status_code}"}