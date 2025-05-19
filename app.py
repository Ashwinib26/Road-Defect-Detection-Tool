import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Load image
image = cv2.imread('images/road_sample.jpg')
resized = cv2.resize(image, (512, 512))
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Morphological Gradient to highlight cracks
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

# Closing to fill gaps and shadows
closed = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, kernel, iterations=2)

# Optional Opening to remove small debris
opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)

# Save results
os.makedirs("results", exist_ok=True)
cv2.imwrite("results/gray.jpg", gray)
cv2.imwrite("results/thresh.jpg", thresh)
cv2.imwrite("results/gradient.jpg", gradient)
cv2.imwrite("results/closed.jpg", closed)
cv2.imwrite("results/opened.jpg", opened)

# Show comparison
titles = ["Gray", "Threshold", "Gradient", "Closed", "Opened"]
images = [gray, thresh, gradient, closed, opened]

plt.figure(figsize=(12, 6))
for i in range(len(images)):
    plt.subplot(2, 3, i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
plt.tight_layout()
plt.show()
