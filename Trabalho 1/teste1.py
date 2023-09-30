import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class EditorImagem: # Classe principal
    def __init__(self, principal): # Método construtor self é o objeto que está sendo criado e principal é o primeiro parâmetro 
        self.principal = principal
        self.principal.title("Editor de Imagens")
        self.principal.columnconfigure(0, weight=1)
        self.principal.columnconfigure(1, weight=0)
        self.principal.rowconfigure(0, weight=0)
        self.principal.rowconfigure(1, weight=1)
        self.principal.minsize(800, 600)

        self.tk_image = None

        # Crie um frame para o menu lateral
        self.menu_frame1 = tk.Frame(principal, bg="gray")
        self.menu_frame1.grid(row=0, column=0, padx=(0,0), pady=(0,5), sticky="nsew", columnspan=2)  # Coloque-o à direita com sticky="ns"

        self.menu_frame2 = tk.Frame(principal, bg="gray")
        self.menu_frame2.grid(row=1, column=1, padx=3, pady=(0,0.5), sticky="nsew")

        self.image_frame = tk.Frame(principal, bg="white")
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
            canvas_largura = self.canvas.winfo_width() # Retorna a largura do canvas em pixels como um inteiro
            canvas_altura = self.canvas.winfo_height() # Retorna a altura do canvas em pixels como um inteiro

            imagem_largura, imagem_altura = pil_image.size # Retorna uma tupla contendo a largura e a altura da imagem
            razao_tamanho = imagem_largura / imagem_altura # Calcula a razão de aspecto da imagem (largura / altura)

            if imagem_largura > canvas_largura or imagem_altura > canvas_altura: # Se a imagem for maior que o canvas
                if canvas_largura / razao_tamanho > canvas_altura: # Se a largura do canvas for maior que a altura
                    nova_largura = int(canvas_altura * razao_tamanho) # Redimensiona a largura para a altura do canvas
                    nova_altura = canvas_altura # A altura é igual à altura do canvas
                else:
                    nova_largura = canvas_largura # A largura é igual à largura do canvas
                    nova_altura = int(canvas_largura / razao_tamanho) # Redimensiona a altura para a largura do canvas

                pil_image = pil_image.resize((nova_largura, nova_altura)) # Redimensiona a imagem

            self.tk_image = ImageTk.PhotoImage(pil_image) # Converte a imagem Pillow em um formato Tkinter PhotoImage

            self.canvas.delete("all")  # Limpa o conteúdo do canvas
            self.canvas.create_image(30, 30, anchor="nw", image=self.tk_image) # Cria uma imagem no canvas com a imagem redimensionada

                    

    def mostrar_imagem(self, pil_image): # Método para mostrar a imagem
        # Converte a imagem Pillow em um formato Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image) # Converte a imagem Pillow em um formato Tkinter PhotoImage

        # Crie um widget de imagem para exibir a imagem
        imagem_label = tk.Label(self.image_frame, image=tk_image)
        imagem_label.image = tk_image  # Mantém uma referência para evitar que a imagem seja coletada pelo garbage collector
        imagem_label.pack(pady=200)

    
    def salvar(self):
        print("Botão 2 pressionado")

    def sair(self):
        print("Botão 3 pressionado")

if __name__ == "__main__":
    principal = tk.Tk()
    app = EditorImagem(principal)
    principal.mainloop()
