import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

def open_file(image_num):
    file_path = filedialog.askopenfilename(title=f"Select image file {image_num}",
                                           filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        image = cv2.imread(file_path)
        if image is not None:
            if image_num == 1:
                global image1
                image1 = image
                display_image(image1, image1_label)
            else:
                global image2
                image2 = image
                display_image(image2, image2_label)
        else:
            print(f"Cannot read image file {image_num}.")

def display_image(image, label):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    label.configure(image=image)
    label.image = image

def calculate_area_in_meters(pixels, ppm):
    return pixels / (ppm ** 2)

def compare_images(image1, ppm1, image2, ppm2):
    if image1 is None or image2 is None:
        print("Please select both images.")
        return

    def calculate_area(image):
        return image.shape[0] * image.shape[1]

    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(gray_image1, gray_image2)
    _, difference_threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

    area_of_differences_pixels = cv2.countNonZero(difference_threshold)
    area_of_differences_meters = calculate_area_in_meters(area_of_differences_pixels, min(ppm1, ppm2))
    print(f"Area of Differences: {area_of_differences_pixels} pixels")
    print(f"Area of Differences: {area_of_differences_meters} square meters")

    area_image1_pixels = calculate_area(image1)
    area_image1_meters = calculate_area_in_meters(area_image1_pixels, ppm1)
    area_image2_pixels = calculate_area(image2)
    area_image2_meters = calculate_area_in_meters(area_image2_pixels, ppm2)
    print(f"Area of Image 1: {area_image1_pixels} pixels, {area_image1_meters} square meters")
    print(f"Area of Image 2: {area_image2_pixels} pixels, {area_image2_meters} square meters")

    plt.imshow(difference_threshold, cmap='gray')
    plt.axis('off')
    plt.title("Differences")
    plt.show()

# Define constant ppm values for both images
ppm1 = 100
ppm2 = 100

root = tk.Tk()
root.title("So sánh hình ảnh (Compare images)")

image1_label = tk.Label(root)
image1_label.pack(side="left", padx=10, pady=10)

image2_label = tk.Label(root)
image2_label.pack(side="right", padx=10, pady=10)

open_button1 = tk.Button(root, text="Mở hình ảnh 1 (Open image 1)", command=lambda: open_file(1))
open_button1.pack(pady=10)

open_button2 = tk.Button(root, text="Mở hình ảnh 2 (Open image 2)", command=lambda: open_file(2))
open_button2.pack(pady=10)

# Adjust the command for compare_button to include the ppm values directly
compare_button = tk.Button(root, text="So sánh hình ảnh (Compare images)",
                           command=lambda: compare_images(image1, ppm1, image2, ppm2) if image1 is not None and image2 is not None else print("Please select both images before comparing."))
compare_button.pack(pady=20)

image1 = None
image2 = None

root.mainloop()
