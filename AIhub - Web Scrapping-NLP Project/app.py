import base64
import io
import json
import os
import time
import cv2
from flask import Flask, request, jsonify, render_template, send_file
import requests
from werkzeug.utils import secure_filename
from audio_classification import classify_audio
from automatic_speech_recognation import transcribe_audio
from image_classification import classify_image
from image_detection import detect_objects
from image_segmentation import segment_image
from image_to_image import process_image
from image_to_text import API_TOKEN, process_image_with_model, remove_converted_image
from sence_similarity import get_similarity_score
from text_generator import generate_text
from text_summarization import summarize_text
from text_classification import classify_text
import text_summarization
import text_to_audio
import text_to_image
from text_to_speech import convert_text_to_speech
from token_classification import classify_token
###from video_classifier import process_frame  


app = Flask(__name__)


########## DETAIL ROUTES ##########

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail_summarization')
def detail_sum():
    return render_template('detail_summarization.html')

@app.route('/detail_classification')
def detail_classification():
    return render_template('detail_classification.html')

@app.route('/detail_sentence_similarity')
def detail_sence_similarity():
    return render_template('detail_sentence_similarity.html')

@app.route('/detail_token_classification')
def detail_token_classification():
    return render_template('detail_token_classification.html')

@app.route('/detail_text_generator')
def detail_text_generation():
    return render_template('detail_text_generator.html')

@app.route('/detail_image_to_image')
def detail_image_to_image():
    return render_template('detail_image_to_image.html')

@app.route('/detail_image_classification')
def detail_image_classification():
    return render_template('detail_image_classification.html')

@app.route('/detail_image_detection')
def detail_image_detection():
    return render_template('detail_image_detection.html')

@app.route('/detail_image_to_text')
def detail_image_to_text():
    return render_template('detail_image_to_text.html')

@app.route('/detail_text_to_image')
def detail_text_to_image():
    return render_template('detail_text_to_image.html')

@app.route('/detail_image_segmentation')
def detail_image_segmentation():
    return render_template('detail_image_segmentation.html')

@app.route('/detail_video_classificaton')
def detail_video_classificaton():
    return render_template('detail_video_classificaton.html')

@app.route('/detail_text_to_speech')
def detail_text_to_speech():
    return render_template('detail_text_to_speech.html')

@app.route('/detail_text_to_audio')
def detail_text_to_audio():
    return render_template('detail_text_to_audio.html')

@app.route('/detail_audio_classification')
def detail_audio_classification():
    return render_template('detail_audio_classification.html')

@app.route('/detail_automatic_speech_recognation')
def detail_automatic_speech_recognation():
    return render_template('detail_automatic_speech_recognation.html')

########### API ROUTES ###########

@app.route('/summarize', methods=['POST'])
def summarize():
    model = request.form['model']
    text = request.form['text']
    
    # text_summarization.py dosyasındaki summarize_text fonksiyonunu çağır
    summary = text_summarization.summarize_text(model, text)
    
    return jsonify({"summary": summary})

@app.route('/classifyText', methods=['POST'])
def classify_text_route():
    data = request.get_json()
    model_name = data.get('model')
    text_prompt = data.get('text')
    results = classify_text(text_prompt, model_name)
    if isinstance(results, dict) and 'error' in results:
        return jsonify(results), 400
    return jsonify({'results': results})

@app.route('/getSimilarityScore', methods=['POST'])
def similarity_score():
    data = request.get_json()
    model_name = data.get('model')
    original_sentence = data.get('original_sentence')
    sentences = data.get('sentences')
    scores = get_similarity_score(original_sentence, sentences, model_name)
    if isinstance(scores, dict) and 'error' in scores:
        return jsonify(scores), 400
    return jsonify({'scores': scores})


@app.route('/tokenClassification', methods=['POST'])
def get_token_classification():
    data = request.get_json()
    model_name = data.get('model')
    text_prompt = data.get('text')
    # Sınıflandırma fonksiyonunu çağır ve sonuçları al
    top_results = classify_token(model_name, text_prompt)
    return jsonify({'Results': top_results})

@app.route('/generateText', methods=['POST'])
def generate_text_route():
    data = request.get_json()
    model_name = data.get('model')
    text_prompt = data.get('text')
    result = generate_text(text_prompt, model_name)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)


@app.route('/classifyImage', methods=['POST'])
def classify_image_route():
    if 'file' not in request.files or 'model' not in request.form:
        return jsonify({'error': 'No file or model provided'}), 400

    file = request.files['file']
    model_name = request.form.get('model')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # `image_classification.py` dosyasındaki fonksiyonu çağırma
        results = classify_image(model_name, file_path)
        return jsonify({'results': results}) if 'error' not in results else jsonify(results), 500

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/detectObjects', methods=['POST'])
def detect_objects_route():
    model = request.form['model']
    file = request.files['file']

    if not file:
        return jsonify({"error": "Görsel dosyası yüklenmedi."}), 400

    # Görseli geçici bir dosyaya kaydet
    temp_file_path = os.path.join("static", file.filename)
    file.save(temp_file_path)

    # Görseldeki nesneleri tespit et
    result, status_code = detect_objects(model, temp_file_path)

    # Geçici dosyayı sil
    os.remove(temp_file_path)

    return result, status_code


###image to image ###
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadImage', methods=['POST'])
def upload_image():
    if 'file' not in request.files or 'text' not in request.form or 'model' not in request.form:
        return jsonify({'error': 'No file part or text/model not provided'}), 400

    file = request.files['file']
    text_description = request.form.get('text')
    model_name = request.form.get('model')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return process_image(file_path, text_description, model_name)

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/process_image_with_model', methods=['POST'])
def process_image_with_model_route():
    if 'image' not in request.files:
        return jsonify({"error": "Görsel yüklenmedi."})
    
    file = request.files['image']
    model_name = request.form['model']
    
    if not file or not model_name:
        return jsonify({"error": "Gerekli bilgiler eksik."})
    
    file_path = f"./static/{file.filename}"
    file.save(file_path)
    
    try:
        result = process_image_with_model(file_path, model_name, API_TOKEN)
    finally:
        remove_converted_image(file_path)
    
    return jsonify({"result": result})


#image segmentation###
@app.route('/segment', methods=['POST'])
def segment():
    if 'file' not in request.files or 'model' not in request.form:
        return jsonify({'error': 'No file part or model not provided'}), 400

    file = request.files['file']
    model_name = request.form.get('model')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Segment görüntü
        return segment_image(file_path, model_name)

    return jsonify({'error': 'File type not allowed'}), 400



###text to image ### 
@app.route('/generate', methods=['POST'])
def generate():
    model = request.form['model']
    text_prompt = request.form['text_prompt']
    image_path = text_to_image.generate_image(model, text_prompt)
    return jsonify({'image_path': image_path})

"""##video classification##    
@app.route('/classify_video', methods=['POST'])
def classify_video():
    file = request.files['video']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Video dosyasını okuma
    video_bytes = file.read()
    video = cv2.VideoCapture(io.BytesIO(video_bytes))

    results = []

    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_results = process_frame(frame)
        results.append(frame_results)

    video.release()

    return jsonify(results)
"""
### text to speech ###
@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    lang = request.form.get('lang', 'en')  # Varsayılan dil İngilizce
    
    if not text:
        return "Lütfen metin girin", 400
    
    output_path = convert_text_to_speech(text, lang)
    if output_path:
        return send_file(output_path, as_attachment=False)
    else:
        return "Ses dosyası oluşturulurken bir hata oluştu.", 500

##text_to_audio
@app.route('/convert_text_to_audio', methods=['POST'])
def convert_text_to_audio():
    model = request.form['model']
    text_prompt = request.form['text']
    
    # Ses dosyasını oluştur
    file_path = text_to_audio.generate_audio(model, text_prompt)
    
    return send_file(file_path, mimetype='audio/mpeg', as_attachment=False)



####audio classification####
@app.route('/classify', methods=['POST'])
def classify():
    model = request.form.get('model')
    audio = request.files.get('audio')
    
    if not audio:
        return jsonify({"error": "Ses dosyası yüklenmedi."}), 400
    
    audio_path = 'uploads/' + audio.filename
    
    try:
        audio.save(audio_path)
    except Exception as e:
        return jsonify({"error": f"Dosya kaydetme hatası: {str(e)}"}), 500
    
    results = classify_audio(model, audio_path)
    
    return jsonify(results)


###automatic speech recognation###

@app.route('/asr', methods=['POST'])
def asr():
    model = request.form.get('model')
    audio_file = request.files.get('audio_file')

    if not model or not audio_file:
        return jsonify({"error": "Model veya ses dosyası sağlanmadı!"}), 400

    # Ses dosyasını geçici bir dosyaya kaydet
    audio_file_path = "temp_audio.wav"
    audio_file.save(audio_file_path)

    # Fonksiyonu çağır ve yanıtı al
    token = "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"
    result = transcribe_audio(model, audio_file_path, token)

    # Geçici dosyayı temizle
    os.remove(audio_file_path)

    return jsonify({"text": result})


if __name__ == '__main__':
    app.run(debug=True)
