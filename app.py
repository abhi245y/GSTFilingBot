from flask import Flask, request, render_template, redirect, jsonify
import os
from urllib.parse import urlparse
import requests

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = os.urandom(25)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        captcha_image_src = request.form['captcha_image_src']
        captcha_input_value = request.form['captcha_input_value']

        captcha_folder = os.path.join(os.getcwd(), 'captcha')
        if not os.path.exists(captcha_folder):
            os.makedirs(captcha_folder)

        with open(os.path.join(captcha_folder, f'{captcha_input_value}.png'), 'wb') as f:
            f.write(requests.get(captcha_image_src).content)

        return 'Form submitted successfully'
    return render_template('index.html')

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
