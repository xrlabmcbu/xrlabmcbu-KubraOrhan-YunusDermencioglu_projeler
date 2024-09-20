from gtts import gTTS

def convert_text_to_speech(text, lang='en'):
    try:
        # Metni ses dosyasına dönüştür
        tts = gTTS(text=text, lang=lang)

        # Ses dosyasını kaydet
        output_path = "static/text-to-speech(Google).mp3"
        tts.save(output_path)

        # Ses dosyasını döndür
        return output_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
