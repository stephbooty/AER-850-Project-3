# -*- coding: utf-8 -*-
"""AER850_StevenButt_Project3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1obJTSowFdJB5iHsLrTRXPkXRkDf43Eug
"""

#Steven Butt
#AER Project 3

from google.colab import drive
drive.mount('/content/drive')

data_path = "/content/drive/My Drive/aer 850/project 3/data"

import cv2
import matplotlib.pyplot as plt


image_path = "/content/drive/My Drive/aer 850/project 3/data/motherboard_image.JPEG"
original_image = cv2.imread(image_path)

image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(8, 8))
plt.title("Original Motherboard Image")
plt.imshow(image_rgb)
plt.axis("off")
plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt

gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

adaptive_thresh = cv2.adaptiveThreshold(
    gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 2
)

contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 5000]
largest_contour = max(filtered_contours, key=cv2.contourArea)

mask = np.zeros_like(gray_image)
cv2.drawContours(mask, [largest_contour], -1, color=255, thickness=cv2.FILLED)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

masked_image = cv2.bitwise_and(original_image, original_image, mask=cleaned_mask)

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.title("Adaptive Thresholding")
plt.imshow(adaptive_thresh, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Cleaned Contour Mask")
plt.imshow(cleaned_mask, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Final Masked PCB Image")
plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.show()

norm_image = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX)

kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
sharpened_image = cv2.filter2D(norm_image, -1, kernel)

#Gaussian Blur to suppress noise
smoothed_image = cv2.GaussianBlur(sharpened_image, (7, 7), 0)

#Canny Edge Detection with refined thresholds
low_threshold = 80
high_threshold = 180
edges = cv2.Canny(smoothed_image, low_threshold, high_threshold)

# Strengthen edges using Dilation
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
dilated_edges = cv2.dilate(edges, kernel, iterations=1)

plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title("Normalized Image")
plt.imshow(norm_image, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Sharpened Image")
plt.imshow(sharpened_image, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Dilated Edges (Refined)")
plt.imshow(dilated_edges, cmap="gray")
plt.axis("off")

plt.show()

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

eroded_mask = cv2.erode(cleaned_mask, kernel, iterations=1)

refined_masked_image = cv2.bitwise_and(original_image, original_image, mask=eroded_mask)

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.title("Cleaned and Eroded Mask")
plt.imshow(eroded_mask, cmap="gray")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Refined Masked PCB Image")
plt.imshow(cv2.cvtColor(refined_masked_image, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.show()

cv2.imwrite("cleaned_mask.png", eroded_mask)
cv2.imwrite("refined_masked_pcb.png", refined_masked_image)

cv2.imwrite("cleaned_mask.png", eroded_mask)

cv2.imwrite("refined_masked_pcb.png", cv2.cvtColor(refined_masked_image, cv2.COLOR_BGR2RGB))

print("Outputs saved successfully!")

pip install ultralytics

from ultralytics import YOLO

model = YOLO('yolov8n.pt')

# Train the model
results = model.train(
    data='/content/drive/My Drive/aer 850/project 3/data/data.yaml',
    epochs=50,         # Number of training epochs
    imgsz=640,         # Image size
    batch=16,          # Batch size
    name='pcb_yolov8'  # Save model checkpoints under this name
)

from ultralytics import YOLO

#Load
model = YOLO('runs/detect/pcb_yolov8/weights/best.pt')

#Path to test images
test_images_path = "/content/drive/My Drive/aer 850/project 3/data/test/images"

# Predict
results = model.predict(source=test_images_path, save=True)

from IPython.display import Image, display
import glob

#Display
predicted_images = glob.glob('runs/detect/predict/*.jpg')
for img_path in predicted_images:
    display(Image(filename=img_path))

#Validate
metrics = model.val(data="/content/drive/My Drive/aer 850/project 3/data/data.yaml")
print(metrics)

from ultralytics import YOLO
from PIL import Image
import os

model = YOLO('runs/detect/pcb_yolov8/weights/best.pt')
image_paths = [
    '/content/drive/My Drive/aer 850/project 3/data/evaluation/rasppi.jpg',
    '/content/drive/My Drive/aer 850/project 3/data/evaluation/arduno.jpg',
    '/content/drive/My Drive/aer 850/project 3/data/evaluation/ardmega.jpg'
]

for img_path in image_paths:
    results = model.predict(source=img_path, save=True, save_txt=False)
    save_dir = results[0].save_dir
    print(f"Prediction completed for {img_path}. Results saved to {save_dir}")

for img_path in image_paths:
    annotated_image_path = os.path.join(save_dir, os.path.basename(img_path))  # Construct the annotated image path
    img = Image.open(annotated_image_path)
    img.show()

from IPython.display import Image, display
import os

output_folder = 'runs/detect/predict6'

if os.path.exists(output_folder):
    images = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for img_path in images:
        print(f"Displaying: {img_path}")
        display(Image(filename=img_path))
else:
    print(f"Folder not found: {output_folder}")

'''
WRITTEN
3.1
To detect the PCB edges and extract it from the background, First, the image was
 converted to grayscale.Adaptive thresholding was applied to help variations in
 light across the PCB. This method was chosen because a global threshold was
 failing in spots with poor brightness, which was an problem with the original
  image. Adaptive thresholding made the detection of finer detail while allowi
  g to local pixel intensities, but it introduced noise.

the contours were extracted and only the largest contour, thought to be the
PCB, was kept. To make sure the contour captured the PCB completely i used
morphological operations. Dilation was used ti strengthen weak edges,
closing filled in small gaps in the boundary, and the erosion tightned the
mask by removing the noise. without these extra bits, the mask was
fragmented and poor, leaving portions of the PCB boundary incomplete or kept
background.

The mask was then applied to isolate the PCB from the background. though
this helped, it didnt fix everything like noise from overlapping
components or fine details not being picked. Improvements could be
bettering the preprocessing phase, like histogram equalization to better
normalize lighting. These approaches would address limitations in
traditional edge and contour-based methods, ensuring a more precise
extraction.

images can be seen above in the code output


3.2

The YOLOv8 model was trained on the PCB dataset using 50 epochs, a batch size of
 16, and a 640x640 image size. Training included data augmentation techniques
 like flipping and scaling to improve the model against variations. The
 confusion matrix revealed that most components were accurately classified,
 though there was occasional confusion between the visually similar items, like
 capacitors and electrolytic capacitors. The precision-confidence curve
 indicated good precision for confidence thresholds above 0.5. but lower
 thresholds had uncertainty. Precision-recall curve had strong performance but
 showed a slight problem for components that overlapped. During testing, diodes
 on the Raspberry Pi, were missed, and dense regions on the Arduino had minor
 detection error. The Ardmega image had small overestimations in connector
 counts and missed some edge components. Improvements could be further dataset
 expansion with different edge cases also data augmentation, and hyperparameter
 tuning to better detection accuracy and lower errors.
'''