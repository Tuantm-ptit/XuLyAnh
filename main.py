import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageProcessor:
    def __init__(self, image_path, kernel_size, gamma):
        self.image_path = image_path
        self.kernel_size = kernel_size
        self.gamma = gamma

    def apply_filter(self, filter_function):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        processed_image = filter_function(gray_image)
        return gray_image, processed_image

    def apply_median_filter(self, image):
        return cv2.medianBlur(image, self.kernel_size)

    def apply_noise_reduction(self, image):
        return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)

    def apply_contrast(self, image):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)

    def apply_stretch(self, image):
        stretched_image = np.power(image / float(np.max(image)), self.gamma) * 255.0
        return np.uint8(stretched_image)

    def apply_max_min_filter(self, image):
        max_filtered_image = cv2.dilate(image, np.ones((self.kernel_size, self.kernel_size), np.uint8))
        min_filtered_image = cv2.erode(image, np.ones((self.kernel_size, self.kernel_size), np.uint8))
        return max_filtered_image, min_filtered_image

    def apply_midpoint_filter(self, image):
        max_filtered_image, min_filtered_image = self.apply_max_min_filter(image)
        return (max_filtered_image + min_filtered_image) // 2

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xu ly anh")
        self.root.configure(bg="#336699")  # Background color

        self.image_path = None
        self.kernel_size = 5
        self.gamma = 1.5  # Default gamma value
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Median Filter")  # Default value

        self.create_widgets()

    def create_widgets(self):
        # Frame to hold the widgets
        main_frame = tk.Frame(self.root, padx=40, pady=40, bg="#336699")  # Dark blue background
        main_frame.pack(expand=True)

        # Select Image Button
        select_image_button = tk.Button(main_frame, text="Chon anh", command=self.select_image, bg="#4CAF67", fg="white")  # Green button
        select_image_button.grid(row=0, column=0, pady=10, padx=10)

        # Process Image Button
        process_button = tk.Button(main_frame, text="Xu ly", command=self.process_image, bg="#008CBA", fg="white")  # Blue button
        process_button.grid(row=2, column=0, pady=10, padx=10)

        # Dropdown for choosing algorithm
        algorithms = ["Median Filter", "Noise Reduction", "Contrast", "Stretch", "Max - Min Filter", "Midpoint Filter"]
        algorithm_menu = tk.OptionMenu(main_frame, self.algorithm_var, *algorithms)
        algorithm_menu.config(bg="#4CAF50", fg="white")  # Green dropdown
        algorithm_menu.grid(row=1, column=0, pady=10, padx=10)

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path

    def process_image(self):
        if self.image_path:
            algorithm = self.algorithm_var.get()
            processor = ImageProcessor(self.image_path, self.kernel_size, self.gamma)

            filter_functions = {
                "Median Filter": processor.apply_median_filter,
                "Noise Reduction": processor.apply_noise_reduction,
                "Contrast": processor.apply_contrast,
                "Stretch": processor.apply_stretch,
                "Max - Min Filter": processor.apply_max_min_filter,
                "Midpoint Filter": processor.apply_midpoint_filter,
            }

            gray_image, processed_image = processor.apply_filter(filter_functions[algorithm])
            self.display_processed_image(gray_image, processed_image, f"Processed with {algorithm}")

    def display_processed_image(self, original_image, processed_image, title):
        self.display_images(original_image, "Original Image")
        self.display_images(processed_image, title)

    def display_images(self, image, title):
        image_pil = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image_pil)

        display_window = tk.Toplevel(self.root)
        display_window.title(title)

        label = tk.Label(display_window, image=image_tk)
        label.image = image_tk
        label.pack()

        display_window.geometry(f"{image.shape[1]}x{image.shape[0]}")

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
