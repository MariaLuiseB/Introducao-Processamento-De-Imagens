import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.image = None
        self.modified_image = None

        self.frame = tk.Frame(root)
        self.frame.pack()
        self.labels = tk.Label(self.frame, text="ORIGINAL:\t\t\t\t\t\t\t\t\t\t\t\tMODIFICADA:", justify="center", height=10, width=150).pack(side=tk.TOP, anchor=tk.N)
        self.canvas_original = tk.Canvas(self.frame, width=800, height=800)
        self.canvas_original.pack(side=tk.LEFT, anchor=tk.W)
        self.canvas_modified = tk.Canvas(self.frame, width=800, height=800)
        self.canvas_modified.pack(side=tk.RIGHT, anchor=tk.E)
        
        
        self.create_menu()

    def create_menu(self):

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(
            label="Abrir Imagem", command=self.open_image)
        self.file_menu.add_command(
            label="Salvar Imagem", command=self.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.root.quit)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(
            label="Mostrar histograma colorido", command=self.show_histogram)
        self.edit_menu.add_command(
            label="Equalizar histograma", command=self.equalize_histogram)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Aumentar imagem", command=self.enlarge_image)
        self.edit_menu.add_command(
            label="Reduzir imagem", command=self.reduce_image)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Filtro Gaussiano", command=self.apply_gauss_filter)
        self.edit_menu.add_command(
            label="Filtro Box (9 x 9)", command=self.apply_box_filter)
        self.edit_menu.add_command(
            label="Filtro Mediano", command=self.apply_median_filter)
        self.edit_menu.add_command(
            label="Filtro Laplaciano", command=self.apply_laplace_filter)
        self.edit_menu.add_command(
            label="Filtro Sobel", command=self.apply_sobel_filter)
        self.edit_menu.add_command(
            label="Filtro Negativo", command=self.apply_negative)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Mais Brilho", command=self.apply_more_brightness)

        self.edit_menu.add_command(
            label="Menos Brilho", command=self.apply_less_brightness)

        self.edit_menu.add_command(
            label="Mais Contraste", command=self.apply_more_contrast)
        
        self.edit_menu.add_command(
            label="Aguçamento & Suavização (Unsharp)", command=self.apply_unsharp_mask)
        

        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.modified_image = None
            self.show_images(self.image)
            
    def show_images(self, img_modified, img_original=None):
        if img_original is None:
            img_original = self.image
        if img_modified is not None:
            img_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)
            img_modified = cv2.cvtColor(img_modified, cv2.COLOR_BGR2RGB)
            img_original = Image.fromarray(img_original)
            img_modified = Image.fromarray(img_modified)
            img_original = ImageTk.PhotoImage(img_original)
            img_modified = ImageTk.PhotoImage(img_modified)
            self.canvas_original.create_image(0, 0, image=img_original, anchor=tk.NW)
            self.canvas_modified.create_image(0, 0, image=img_modified, anchor=tk.NW)
            self.canvas_original.image = img_original
            self.canvas_modified.image = img_modified

    def save_image(self):
        if self.modified_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                cv2.imwrite(file_path, self.modified_image)

    def show_histogram(self):
        if self.modified_image is not None:
            # Histograma mostrando cada canal de cor
            b, g, r = cv2.split(self.modified_image)
            red = plt.subplot(331)
            red = plt.hist(r.ravel(), 256, [0, 256], color="red")
            green = plt.subplot(332)
            green = plt.hist(g.ravel(), 256, [0, 256], color="green")
            blue = plt.subplot(333)
            blue = plt.hist(b.ravel(), 256, [0, 256], color="blue")
            rgb = plt.subplot(212)
            rgb = plt.hist(r.ravel(), 256, [0, 256], color="red") + plt.hist(g.ravel(), 256, [
                0, 256], color="green") + plt.hist(b.ravel(), 256, [0, 256], color="blue")
            plt.show()

    def equalize_histogram(self):
        if self.image is not None:
            gray_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.modified_image = cv2.equalizeHist(gray_img)
            hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])

            import matplotlib.pyplot as plt
            plt.plot(hist)
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.title('Histogram')
            plt.show()
            self.show_images(self.modified_image)

    def enlarge_image(self):
        if self.image is not None:
            self.modified_image = cv2.resize(
                self.image, None, fx=1.25, fy=1.25, interpolation=cv2.INTER_CUBIC)
            self.show_images(self.modified_image)

    def reduce_image(self):
        if self.image is not None:
            self.modified_image = cv2.resize(
                self.image, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_CUBIC)
            # self.modified_image = cv2.resize(self.image, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
            self.show_images(self.modified_image)

    def apply_gauss_filter(self):
        if self.image is not None:
            self.modified_image = cv2.GaussianBlur(self.image, (3, 3), 0)
            self.show_images(self.modified_image)

    def apply_box_filter(self):
        if self.image is not None:
            self.modified_image = cv2.blur(self.image, (9, 9))
            self.show_images(self.modified_image)

    def apply_median_filter(self):
        if self.image is not None:
            self.modified_image = cv2.medianBlur(self.image, 3)
            self.show_images(self.modified_image)

    def apply_laplace_filter(self):
        if self.image is not None:
            self.modified_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.modified_image = cv2.Laplacian(
                self.modified_image, cv2.CV_8U, ksize=5)
            self.show_images(self.modified_image)

    def apply_sobel_filter(self):
        if self.image is not None:
            self.modified_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.modified_imageX = cv2.Sobel(
                self.modified_image, cv2.CV_8U, 0, 1, ksize=3)
            self.modified_imageY = cv2.Sobel(
                self.modified_image, cv2.CV_8U, 1, 0, ksize=3)
            self.modified_image = cv2.addWeighted(
                self.modified_imageX, 0.5, self.modified_imageY, 0.5, 0)
            self.show_images(self.modified_image)

    def apply_negative(self):
        if self.image is not None:
            self.modified_image = cv2.bitwise_not(self.image)
            self.show_images(self.modified_image)

    def apply_more_brightness(self):
        if self.image is not None:
            self.modified_image = cv2.addWeighted(self.image, 1.5, 0, 0, 0)
            self.show_images(self.modified_image)

    def apply_less_brightness(self):
        if self.image is not None:
            self.modified_image = cv2.addWeighted(self.image, 0.5, 0, 0, 0)
            self.show_images(self.modified_image)

    def apply_more_contrast(self):
        if self.image is not None:
            self.modified_image = cv2.addWeighted(self.image, 1.5, 0, 0, 0)
            self.show_images(self.modified_image)

    def apply_unsharp_mask(self):
        if self.image is not None:
            self.modified_image = cv2.GaussianBlur(self.image, (5, 5), 10)
            self.modified_image = cv2.addWeighted(
                self.image, 1.5, self.modified_image, -0.5, 0)
            self.show_images(self.modified_image)
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
