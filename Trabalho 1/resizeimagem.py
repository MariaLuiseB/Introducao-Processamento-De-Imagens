import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class EditorImagem:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imagens")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.minsize(800, 600)

        self.tk_image = None

        # Crie um frame para o menu lateral
        self.menu_frame1 = tk.Frame(root, bg="gray")
        self.menu_frame1.grid(row=0, column=0, padx=(0,0), pady=(0,5), sticky="nsew", columnspan=2)  # Coloque-o à direita com sticky="ns"

        self.menu_frame2 = tk.Frame(root, bg="gray")
        self.menu_frame2.grid(row=1, column=1, padx=3, pady=(0,0.5), sticky="nsew")

        self.image_frame = tk.Frame(root, bg="white")
        self.image_frame.grid(row=1, column=0, padx=0.8, pady=(0,10), sticky="nsew")


        # Crie botões no menu de cima
        self.botao1 = tk.Button(self.menu_frame1, text="Abrir", command=self.abrir_imagem)
        self.botao2 = tk.Button(self.menu_frame1, text="Salvar", command=self.salvar)
        self.botao3 = tk.Button(self.menu_frame1, text="Sair", command=self.sair)
        # Coloque os botões no menu de cima
        self.botao1.grid(row=0, column=0,pady=10, padx=10)
        self.botao2.grid(row=0, column=1,pady=10, padx=10)
        self.botao3.grid(row=0, column=2,pady=10, padx=10)

        # Crie botões no menu do lado
        self.botao4 = tk.Button(self.menu_frame2, text="Filtro Negativo")
        # Coloque os botões no menu lateral
        self.botao4.grid(row=0, column=0,pady=10, padx=10)

        self.canvas = tk.Canvas(self.image_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def abrir_imagem(self):
         # Abra um diálogo de seleção de arquivo para que o usuário possa escolher uma imagem
            filepath = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

            if filepath:
                # Carregue a imagem selecionada usando o Pillow
                pil_image = Image.open(filepath)

                self.redimensionar_imagem(pil_image)
    

    def redimensionar_imagem(self, pil_image):
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            image_width, image_height = pil_image.size
            aspect_ratio = image_width / image_height

            if image_width > canvas_width or image_height > canvas_height:
                if canvas_width / aspect_ratio > canvas_height:
                    new_width = int(canvas_height * aspect_ratio)
                    new_height = canvas_height
                else:
                    new_width = canvas_width
                    new_height = int(canvas_width / aspect_ratio)

                pil_image = pil_image.resize((new_width, new_height))

            self.tk_image = ImageTk.PhotoImage(pil_image)

            self.canvas.delete("all")  # Limpa o conteúdo do canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

                    

    def mostrar_imagem(self, pil_image):
        # Converte a imagem Pillow em um formato Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)

        # Crie um widget de imagem para exibir a imagem
        imagem_label = tk.Label(self.image_frame, image=tk_image)
        imagem_label.image = tk_image  # Mantém uma referência para evitar que a imagem seja coletada pelo garbage collector
        imagem_label.pack(pady=200)


    
    def salvar(self):
        #salvar imagem em um arquivo .png
        (filename, ext) = filedialog.asksaveasfilename(title="Salvar imagem", filetypes=[("Imagens", "*.png")])

    def sair(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorImagem(root)
    root.mainloop()
