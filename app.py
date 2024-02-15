from flask import Flask, request, render_template, redirect, jsonify
import os
from urllib.parse import urlparse
import requests
import base64
import uuid

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = os.urandom(25)

def get_and_cache_image():
    captcha_image_src = 'https://services.gst.gov.in//services/captcha'
    image_data = requests.get(captcha_image_src).content
    return image_data

cached_images = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        image_id = form_data['image_id']
        captcha_input_value = form_data['captcha_input_value']

        cached_image_data = cached_images.get(image_id)

        captcha_folder = os.path.join(os.getcwd(), 'captcha')
        if not os.path.exists(captcha_folder):
            os.makedirs(captcha_folder)

        with open(os.path.join(captcha_folder, f'{captcha_input_value}.png'), 'wb') as f:
            f.write(cached_image_data)
        return 'Image saved successfully'
    else:
        cached_image_data = get_and_cache_image()
        image_id = str(uuid.uuid4())
        encoded_image_data = base64.b64encode(cached_image_data).decode('utf-8')

        cached_images[image_id] = cached_image_data
        return render_template('index.html', image_data=encoded_image_data, image_id=image_id)

@app.route('/get-progress', methods=['POST'])
def count_capcha_files():
    """
    Counts the number of PNG files in the capcha folder.
    """
    if request.method == 'POST':
        png_files = [file for file in os.listdir('captcha') if file.endswith('.png')]
        return jsonify({'progress':len(png_files)})

if __name__ == '__main__':
    app.run(debug=True,threaded=True, host='0.0.0.0', port='4500')
