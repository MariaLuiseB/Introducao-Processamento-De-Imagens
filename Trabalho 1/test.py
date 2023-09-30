import tkinter as tk
from tkinter import filedialog
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageTk

class EditorImagem(tk.Tk):
    def __init__(self, root):
        # Variaveis pra guardar a imagem original e a imagem atual (com as modificações)
        self.imagem_original = None
        self.imagem_atual = None
        self.imagem_brilho = None
        self.imagem_negativo = None
        self.imagem_log = None
        self.imagem_exp = None
        #=======================================================
        # Variaveis de controle ================================
        self.intensidade_brilho = 1
        self.intensidade_contraste = 1

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

        self.botao_logaritmico = tk.Button(self.menu_frame2, text="Filtro Logaritmico", command=self.aplicar_filtro_logaritmico)
        self.botao_logaritmico.grid(row=1, column=0,pady=10, padx=10, columnspan=2, sticky="ew")

        self.botao_exponencial = tk.Button(self.menu_frame2, text="Filtro Exponencial", command=self.aplicar_filtro_exponencial)
        self.botao_exponencial.grid(row=2, column=0,pady=10, padx=10, columnspan=2, sticky="ew")

        self.frame_transf = tk.Frame(self.menu_frame2, bg="gray")
        self.frame_transf.grid(row=3, column=0, pady=10, padx=10, columnspan=2, sticky="ew")

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
        
        self.botao_aplicar_contraste = tk.Button(self.frame_transf, text="Aplicar Contraste", command=self.aplicar_contraste)
        self.botao_aplicar_contraste.grid(row=3, column=0,pady=10, padx=10, columnspan=2, sticky="ew")
        
        self.botao_histograma = tk.Button(self.frame_transf, text="Histograma", command=self.histograma_imagem)
        self.botao_histograma.grid(row=4, column=0,pady=10, padx=10, columnspan=2, sticky="ew")

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
        image = cv2.imread(filepath)
        if image is not None:
            self.imagem_original = image
            self.redimensionar_imagem(image)

    def redimensionar_imagem(self, image):
        canvas_largura = self.canvas.winfo_width()
        canvas_altura = self.canvas.winfo_height()

        imagem_largura, imagem_altura = image.shape[1], image.shape[0]
        aspect_ratio = imagem_largura / imagem_altura

        if imagem_largura > canvas_largura or imagem_altura > canvas_altura:
            if canvas_largura / aspect_ratio > canvas_altura:
                nova_largura = int(canvas_altura * aspect_ratio)
                nova_altura = canvas_altura
            else:
                nova_largura = canvas_largura
                nova_altura = int(canvas_largura / aspect_ratio)

            image = cv2.resize(image, (nova_largura, nova_altura))

        self.tk_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def aplicar_filtro_negativo(self):
        if self.imagem_original is not None:
            self.imagem_negativo = 255 - self.imagem_original
            self.imagem_atual = self.imagem_negativo
            self.redimensionar_imagem(self.imagem_negativo)

    def aplicar_filtro_logaritmico(self):
        if self.imagem_original is not None:
            self.imagem_log = cv2.log(self.imagem_original.astype(np.float32) + 1.0)
            # Normalizar a imagem resultante para o intervalo de 0 a 255
            self.imagem_log = (self.imagem_log - np.min(self.imagem_log)) / (np.max(self.imagem_log) - np.min(self.imagem_log)) * 255.0
            # Converter de volta para uint8
            self.imagem_log = np.uint8(self.imagem_log)
            self.imagem_atual = self.imagem_log
            self.redimensionar_imagem(self.imagem_log)
    
    def aplicar_filtro_exponencial(self): 
        # Aplicar a transformação exponencial
        self.imagem_exp = cv2.pow(self.imagem_original.astype(np.float32), 2.0)
        # Normalizar a imagem resultante para o intervalo de 0 a 255
        self.imagem_exp = (self.imagem_exp - np.min(self.imagem_exp)) / (np.max(self.imagem_exp) - np.min(self.imagem_exp)) * 255.0
        
        # Converter de volta para uint8
        self.imagem_exp = np.uint8(self.imagem_exp)
        
        self.imagem_atual = self.imagem_exp
        self.redimensionar_imagem(self.imagem_exp)

    def brilho(self, opcao):
        if self.imagem_original is not None:
            if opcao == '+':
                self.intensidade_brilho += 0.5
            elif opcao == '-':
                self.intensidade_brilho -= 0.5
            self.aplicar_brilho()        

    def aumentar_brilho(self):
        self.brilho('+')

    def diminuir_brilho(self):
        self.brilho('-')

    def aplicar_brilho(self):
        if self.imagem_original is not None:
            self.imagem_brilho = cv2.convertScaleAbs(self.imagem_original, alpha=self.intensidade_brilho, beta=0)
            self.imagem_atual = self.imagem_brilho
            self.redimensionar_imagem(self.imagem_brilho)

    def contraste(self, opcao):
        if self.imagem_original is not None:
            if opcao == '+':
                self.intensidade_contraste += 0.2
            elif opcao == '-':
                self.intensidade_contraste -= 0.2
            self.aplicar_contraste()        

    def aumentar_contraste(self):
        self.contraste('+')

    def diminuir_contraste(self):
        self.contraste('-')

    def aplicar_contraste(self):
        if self.imagem_original is not None:
            gray = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY)
            imagem_contraste = cv2.convertScaleAbs(gray, alpha=self.intensidade_contraste, beta=0)
            imagem_contraste = cv2.cvtColor(imagem_contraste, cv2.COLOR_GRAY2BGR)
            self.imagem_atual = imagem_contraste
            self.redimensionar_imagem(imagem_contraste)
    
    def histograma_imagem(self):
        if self.imagem_original is not None and len(self.imagem_original.shape) == 3:
            # Histograma mostrando cada canal de cor
            b, g, r = cv2.split(self.imagem_original)
            rgb = plt.subplot(212)
            rgb = plt.hist(r.ravel(), 256, [0, 256], color="red") + plt.hist(g.ravel(), 256, [
                0, 256], color="green") + plt.hist(b.ravel(), 256, [0, 256], color="blue")
            plt.show()

        elif self.imagem_original is not None and len(self.imagem_original.shape) == 2:
            hist = cv2.calcHist([self.imagem_original], [0], None, [256], [0, 256])
            plt.plot(hist)
            plt.xlabel('Valor de Pixel')
            plt.ylabel('Frequencia')
            plt.title('Histograma')
            plt.show()

       

    def salvar(self):
        if self.imagem_atual is not None:
            filepath = filedialog.asksaveasfilename(defaultextension='')
            if filepath:
                cv2.imwrite(filepath, self.imagem_atual)

    def sair(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorImagem(root)
    root.mainloop()
