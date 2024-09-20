import requests


def generate_image(model, text_prompt):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": "Bearer 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"
    }
    payload = {"inputs": text_prompt}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # HTTP hataları için exception fırlatır
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'image' in content_type:
                image_path = "static/output_image.png"
                with open(image_path, "wb") as f:
                    f.write(response.content)
                return image_path
            else:
                return None
        else:
            print("Hata: ", response.status_code, response.text)
            return None
    except requests.RequestException as e:
        print("API İsteği Hatası:", str(e))
        return None