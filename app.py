# app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', original_image=None, processed_image=None)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        # Save original
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads', filename)
        file.save(filepath)

        # Process the image
        result_path = process_image(filepath,filename)

        # Show both images on the same page
        return render_template(
            'index.html',
            original_image=url_for('static', filename='uploads/' + filename),
            processed_image=url_for('static', filename='results/' + os.path.basename(result_path))
        )
    else:
        return redirect(url_for('index'))

def process_image(filepath, filename):
    image = cv2.imread(filepath)
    resized = cv2.resize(image, (512, 512))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)
    closed = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, kernel, iterations=2)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)

    result_path = os.path.join(RESULT_FOLDER, f'processed_{filename}')
    cv2.imwrite(result_path, opened)
    return result_path

if __name__ == '__main__':
    app.run(debug=True)
