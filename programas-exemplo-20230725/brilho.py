import numpy as np
import matplotlib.pyplot as plt
import cv2

# Ajusta o brilho de uma imagem monocromatica
def ajustaBrilho(img, fator):
    if img.ndim == 3 or fator < 0: 
        return None
    else:
        newImg = np.zeros(img.shape, dtype = np.float64)
        newImg = fator * img
        newImg[newImg > 255] = 255
        newImg[newImg < 0] = 0
        return newImg.astype(np.uint8)

if __name__ == '__main__':
    
    # Le a imagem
    img = plt.imread('cat_puppy.jpg')

    # converte para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # aumenta o brilho em 40%
    img_brighter = ajustaBrilho(img_gray, 1.4)

    # diminui em 40%
    img_darker = ajustaBrilho(img_gray, 0.6)

    # para comparar colocamos as imagens lado a lado
    fig, axs = plt.subplots(1, 3)
    axs[0].axis('off')
    axs[0].set_title('Original')
    axs[0].imshow(img_gray, cmap='gray', vmin=0, vmax=255)
    axs[1].axis('off')
    axs[1].set_title('Mais Brilho')
    axs[1].imshow(img_brighter, cmap='gray', vmin=0, vmax=255)
    axs[2].axis('off')
    axs[2].set_title('Menos Brilho')
    axs[2].imshow(img_darker, cmap='gray', vmin=0, vmax=255)
    plt.show()
