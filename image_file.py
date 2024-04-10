import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

image_path1 = None
image_path2 = None
pixel_to_meter = 0.0002645833

def resize_with_aspect_ratio(image, target_width=None, target_height=None):
    (h, w) = image.shape[:2]
    if target_width is None and target_height is None:
        return image
    if target_width is None:
        r = target_height / float(h)
        dim = (int(w * r), target_height)
    else:
        r = target_width / float(w)
        dim = (target_width, int(h * r))
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

def load_image(image_path, max_size=(500, 500)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]
    scale = min(max_size[0] / w, max_size[1] / h)
    if scale < 1:
        new_w, new_h = int(w * scale), int(h * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    im_pil = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(im_pil)
    return image_tk, image

def select_image1():
    global image_path1
    path = filedialog.askopenfilename()
    if path:
        image_path1 = path
        img_display, _ = load_image(path)
        lbl_image1.config(image=img_display)
        lbl_image1.image = img_display

def select_image2():
    global image_path2
    path = filedialog.askopenfilename()
    if path:
        image_path2 = path
        img_display, _ = load_image(path)
        lbl_image2.config(image=img_display)
        lbl_image2.image = img_display

def compare_images():
    if image_path1 is None or image_path2 is None:
        messagebox.showinfo("Thông báo", "Vui lòng chọn cả hai hình ảnh trước khi so sánh.")
        return
    _, image1 = load_image(image_path1)
    _, image2 = load_image(image_path2)
    target_width = image1.shape[1]
    target_height = image1.shape[0]
    image2_resized = resize_with_aspect_ratio(image2, target_width, target_height)
    difference = cv2.absdiff(image1, image2_resized)
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    diff_pixels = cv2.countNonZero(thresh)
    pixel_to_meter_square = pixel_to_meter ** 2
    diff_area_m2 = diff_pixels * pixel_to_meter_square
    img_display = ImageTk.PhotoImage(image=Image.fromarray(thresh))
    lbl_result.config(image=img_display)
    lbl_result.image = img_display
    messagebox.showinfo("Kết Quả So Sánh", f"Diện tích khác biệt: {diff_pixels} pixel(s)\nTương đương: {diff_area_m2:.4f} m^2")

root = tk.Tk()
root.title("So Sánh Hình Ảnh")
frame = tk.Frame(root)
frame.pack(pady=20)
btn_select_image1 = tk.Button(frame, text="Chọn Ảnh Gốc", command=select_image1)
btn_select_image1.pack(side=tk.LEFT, padx=10)
btn_select_image2 = tk.Button(frame, text="Chọn Ảnh So Sánh", command=select_image2)
btn_select_image2.pack(side=tk.RIGHT, padx=10)
btn_compare = tk.Button(root, text="So Sánh Hình Ảnh", command=compare_images)
btn_compare.pack(pady=10)
lbl_image1 = tk.Label(root, text="Ảnh Gốc")
lbl_image1.pack(side=tk.LEFT, padx=10)
lbl_image2 = tk.Label(root, text="Ảnh So Sánh")
lbl_image2.pack(side=tk.LEFT, padx=10)
lbl_result = tk.Label(root, text="Kết Quả So Sánh")
lbl_result.pack(side=tk.LEFT, padx=10)
root.mainloop()
