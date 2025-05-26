from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import uuid
from time import time

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
    min_area = int(request.form.get('min_area', 300))

    if file:
        unique_id = str(uuid.uuid4())[:8]
        filename = f'{unique_id}_{secure_filename(file.filename)}'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        result_path, stats = process_image(filepath, filename, min_area)

        return render_template(
            'index.html',
            original_image=url_for('static', filename=f'uploads/{filename}') + f'?t={int(time())}',
            processed_image=url_for('static', filename=f'results/{os.path.basename(result_path)}') + f'?t={int(time())}',
            total_cracks=stats['count'],
            total_area=stats['total_area'],
            severity=stats['severity']
        )
    return redirect(url_for('index'))

def process_image(filepath, filename, min_area):
    image = cv2.imread(filepath)
    resized = cv2.resize(image, (512, 512))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = resized.copy()
    count = 0
    total_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            count += 1
            total_area += area
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if total_area < 40000:
        severity = "Low"
    elif total_area < 80000:
        severity = "Medium"
    else:
        severity = "High"

    result_filename = f'processed_{filename}'
    result_path = os.path.join(RESULT_FOLDER, result_filename)
    cv2.imwrite(result_path, contour_image)

    stats = {
        'count': count,
        'total_area': int(total_area),
        'severity': severity
    }

    return result_path, stats

if __name__ == '__main__':
    app.run(debug=True)