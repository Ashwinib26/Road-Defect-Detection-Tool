## 🛣️ Road Crack Detection System

A web-based application that enables users to upload road images and detect cracks based on image processing techniques using OpenCV. The app highlights crack regions, counts them, calculates the total cracked area, and provides a severity level.

---

### 🧰 Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS, JavaScript
* **Image Processing**: OpenCV
* **File Handling**: `werkzeug`, `uuid`, `os`, `cv2`

---

### 📁 Project Structure

```
road-crack-detection/
├── static/
│   ├── uploads/          # Stores original uploaded images
│   ├── results/          # Stores processed images
│   ├── styles.css        # (Optional) Custom CSS
├── templates/
│   └── index.html        # HTML frontend with form and image display
├── app.py                # Main Flask application
├── README.md             # This file
```

---

### 🚀 Features

* Upload an image of a road.
* Set a **minimum crack area** threshold using a slider.
* Displays:

  * Original Image
  * Processed Image with detected crack regions highlighted
  * Total number of detected cracks
  * Total crack area in pixels
  * Severity level (`Low`, `Medium`, `High`)
* Reset button to clear results and upload a new image.

---

### ⚙️ How It Works

1. Upload a road image (`.jpg`, `.png`, etc.).
2. Backend:

   * Resizes image to 512x512.
   * Applies grayscale conversion, Gaussian blur, and edge detection(Erosion and Dilation).
   * Uses dilation and contour detection to identify crack areas.
3. Filters cracks based on area threshold.
4. Draws bounding boxes around cracks and computes statistics.

---

### 🧪 Installation & Running Locally

#### 📦 Installation

```bash
git clone https://github.com/Ashwinib26/Road-Defect-Detection-Tool.git
pip install Flask opencv-python numpy
```

#### ▶️ Run the Application

```bash
python app.py
```

Go to `http://127.0.0.1:5000` in your browser.

* The **Reset** button reloads the page, allowing you to clear results and upload a new image.

---

### 📝 Future Improvements

* Integrate deep learning (CNN) models for more accurate crack detection.
* Export results as PDF report.
* Support for batch image uploads.
* Mobile responsiveness and drag-and-drop upload.

---

### 🤝 Contributing

1. Fork the repo
2. Create a new branch (`feature/my-feature`)
3. Commit your changes
4. Push to the branch
5. Create a pull request

---

### 🙋‍♀️ Support

For questions or suggestions, open an [Issue](https://github.com/your-username/medical-image-preprocessor/issues) or contact [ashwinisbisen@gmail.com](mailto:ashwinisbisen@gmail.com).

---

###💡 Acknowledgments

* [Flask Documentation](https://flask.palletsprojects.com/)
* [OpenCV Tutorials](https://docs.opencv.org/)

---
