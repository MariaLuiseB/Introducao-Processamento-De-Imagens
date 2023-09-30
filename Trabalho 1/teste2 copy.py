import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np

class EditorImagem(tk.Tk):
    def __init__(self, root):
        # Variaveis pra guardar a imagem original e a imagem atual (com as modificações)
        self.imagem_original = None
        self.imagem_atual = None
        self.imagem_brilho = None
 
        #=======================================================
        # Variaveis de controle ================================
        self.intensidade_brilho = 1
        self.intensidade_contraste = 0

        #=======================================================

        self.root = root
        self.root.title("Editor de Imagens")

        # Configuração da janela principal ======================
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.minsize(800, 600)
        # =======================================================

        # Menu de cima ==========================================
        self.menu_frame1 = tk.Frame(root, bg="gray")
        self.menu_frame1.grid(row=0, column=0, padx=(0,0), pady=(0,5), sticky="ew", columnspan=2)  # Coloque-o à direita com sticky="ns"

        self.botao_abrir = tk.Button(self.menu_frame1, text="Abrir", command=self.abrir_imagem)
        self.botao_abrir.grid(row=0, column=0,pady=10, padx=10)
       
        self.botao_salvar = tk.Button(self.menu_frame1, text="Salvar", command=self.salvar)
        self.botao_salvar.grid(row=0, column=1,pady=10, padx=10)
       
        self.botao_sair = tk.Button(self.menu_frame1, text="Sair", command=self.sair)
        self.botao_sair.grid(row=0, column=2,pady=10, padx=10)
        # =======================================================

        # Menu do lado ==========================================
        self.menu_frame2 = tk.Frame(root, bg="gray")
        self.menu_frame2.grid(row=1, column=1, padx=3, pady=(0,0.5), sticky="nsew")

        self.botao_negativo = tk.Button(self.menu_frame2, text="Filtro Negativo", command=self.aplicar_filtro_negativo)
        self.botao_negativo.grid(row=0, column=0,pady=10, padx=10, columnspan=2, sticky="ew")

        self.botao_gamma = tk.Button(self.menu_frame2, text="Filtro Logaritmico", command=self.aplicar_filtro_logaritmico)
        self.botao_gamma.grid(row=1, column=0,pady=10, padx=10, columnspan=2, sticky="ew")

        self.frame_transf = tk.Frame(self.menu_frame2, bg="gray")
        self.frame_transf.grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuir_brilho = tk.Button(self.frame_transf, text="Diminuir Brilho", command=self.diminuir_brilho)
        self.botao_diminuir_brilho.grid(row=0, column=0,pady=10, padx=10, sticky="ew")

        self.botao_aumentar_brilho = tk.Button(self.frame_transf, text="Aumentar Brilho", command=self.aumentar_brilho)
        self.botao_aumentar_brilho.grid(row=0, column=1,pady=10, padx=10, sticky="ew")

        self.botao_aplicar_brilho = tk.Button(self.frame_transf, text="Aplicar Brilho", command=self.aplicar_brilho)
        self.botao_aplicar_brilho.grid(row=1, column=0,pady=10, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuir_contraste = tk.Button(self.frame_transf, text="Diminuir Contraste", command=self.diminuir_contraste)
        self.botao_diminuir_contraste.grid(row=2, column=0,pady=10, padx=10)

        self.botao_aumentar_contraste = tk.Button(self.frame_transf, text="Aumentar Contraste", command=self.aumentar_contraste)
        self.botao_aumentar_contraste.grid(row=2, column=1,pady=10, padx=10)
        
        self.botao_aplicar_contraste = tk.Button(self.frame_transf, text="Aplicar Contraste")
        self.botao_aplicar_contraste.grid(row=3, column=0,pady=10, padx=10, columnspan=2, sticky="ew")
        # =======================================================

        # Frame para exibir a imagem ============================
        self.image_frame = tk.Frame(root, bg="white")
        self.image_frame.grid(row=1, column=0, padx=0.8, pady=(0,10), sticky="nsew")
        self.image_frame.columnconfigure(0, weight=1)
        self.image_frame.rowconfigure(0, weight=1)

        # Canvas para exibir a imagem ===========================
        self.canvas = tk.Canvas(self.image_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def abrir_imagem(self):
        filepath = filedialog.askopenfilename()
        image = Image.open(filepath)
        if image:
            self.imagem_original = image
            # Redimensiona a imagem para caber no tamanho do canvas
            self.redimensionar_imagem(image)

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

    def aplicar_filtro_logaritmico(self):
        if self.imagem_original:
            image_array = np.array(self.imagem_original)
            log_image = np.log(image_array + 1)
            pil_image = Image.fromarray(log_image)
            self.imagem_atual = pil_image
            self.redimensionar_imagem(pil_image)

    def aplicar_filtro_negativo(self):
        if self.imagem_original:
            image_array = np.array(self.imagem_original)
            negative_image = 255 - image_array
            pil_image = Image.fromarray(negative_image)
            self.imagem_atual = pil_image
            self.redimensionar_imagem(pil_image)

    
    def brilho(self, opcao):
        if self.imagem_atual:
            if opcao == '+':
                self.intensidade_brilho += 0.2
            elif opcao == '-':
                self.intensidade_brilho -= 0.2
            imagem = ImageEnhance.Brightness(self.imagem_atual).enhance(self.intensidade_brilho)
            self.imagem_brilho = imagem
            self.redimensionar_imagem(imagem)
        
    
    def aumentar_brilho(self):
        self.brilho('+')

    def diminuir_brilho(self):
        self.brilho('-')
    
    def aplicar_brilho(self):
        self.salvar_estado_atual('brilho')
    
    def contraste(self, opcao):
        if self.imagem_atual:
            if opcao == '+':
                self.intensidade_contraste += 0.2
            elif opcao == '-':
                self.intensidade_contraste -= 0.2
            imagem = ImageEnhance.Contrast(self.imagem_atual).enhance(self.intensidade_contraste)
            self.imagem_contraste = imagem
            self.redimensionar_imagem(imagem)
        

    def aumentar_contraste(self):
        self.contraste('+')
    
    def diminuir_contraste(self):
        self.contraste('-')
    
    def aplicar_contraste(self):
        self.salvar_estado_atual('contraste')

    def salvar_estado_atual(self, tipo):
        if tipo == 'brilho':
            self.imagem_atual = self.imagem_brilho
            self.redimensionar_imagem(self.imagem_atual)
    
    def salvar(self):
        if self.imagem_atual:
            filepath = filedialog.asksaveasfilename(defaultextension=self.imagem_atual.format)
            if filepath:
                self.imagem_atual.save(filepath, format=self.imagem_atual.format)

    def sair(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorImagem(root)
    root.mainloop()
