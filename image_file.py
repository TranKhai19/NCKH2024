import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

image_path1 = None
image_path2 = None
pixel_to_meter = 0.0002645833  


def load_image(image_path, resize=True):
    """Tải và chuyển đổi hình ảnh để hiển thị trên Tkinter."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if resize:
        image = cv2.resize(image, (250, 250))
    im_pil = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(im_pil)
    return image_tk, image


def select_image1():
    """Chọn ảnh gốc và hiển thị."""
    global image_path1
    path = filedialog.askopenfilename()
    if path:
        image_path1 = path
        img_display, _ = load_image(path)
        lbl_image1.config(image=img_display)
        lbl_image1.image = img_display


def select_image2():
    """Chọn ảnh so sánh và hiển thị."""
    global image_path2
    path = filedialog.askopenfilename()
    if path:
        image_path2 = path
        img_display, _ = load_image(path)
        lbl_image2.config(image=img_display)
        lbl_image2.image = img_display


def compare_images():
    """So sánh hai hình ảnh, hiển thị kết quả và tính diện tích khác biệt."""
    if image_path1 is None or image_path2 is None:
        messagebox.showinfo("Thông báo", "Vui lòng chọn cả hai hình ảnh trước khi so sánh.")
        return

    _, image1 = load_image(image_path1, resize=False)
    _, image2 = load_image(image_path2, resize=False)

    image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    difference = cv2.absdiff(image1, image2)
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    diff_pixels = cv2.countNonZero(thresh)

    # Tính diện tích khác biệt bằng mét vuông
    pixel_to_meter_square = pixel_to_meter ** 2
    diff_area_m2 = diff_pixels * pixel_to_meter_square

    img_display = ImageTk.PhotoImage(image=Image.fromarray(thresh))
    lbl_result.config(image=img_display)
    lbl_result.image = img_display

    messagebox.showinfo("Kết Quả So Sánh", f"Diện tích khác biệt: {diff_pixels} pixel(s)\n"
                                           f"Tương đương: {diff_area_m2:.4f} m^2")


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
