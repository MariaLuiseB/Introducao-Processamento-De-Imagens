import numpy as np
import matplotlib.pyplot as plt
import cv2

# implementa o calculo de um histograma
#def hist(img): #supondo img monocromatica
#    h = np.zeros(256)
#    for i in range(256):
#        h[i] = np.sum(img==i)
#    linhas = img.shape[0]
#    colunas = img.shape[1]
#    h = h / (linhas * colunas)
#    return h

#def calcula_cdf(h): # h é o histograma normalizado
#    cdf = np.zeros(256)
#    cdf[0] = h[0]
#    for i in range(1, 256):
#        cdf[i] = cdf[i-1] + h[i]
#     return cdf

if __name__ == '__main__':
    img = cv2.imread('low_contrast_pollen.tif') 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    R = img.shape[0]
    C = img.shape[1]

    #calculo do histograma normalizado (pr)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256]) 
    pr = hist/(R*C)

    # cummulative distribution function (CDF)
    cdf = pr.cumsum()
    sk = 255 * cdf
    sk = np.round(sk)

    # criando a imagem de saída
    img_out = np.zeros(img.shape, dtype=np.uint8)
    for i in range(256):
        img_out[img == i] = sk[i]

    #plota lado a lado
    fig, axs = plt.subplots(1,2)
    axs[0].axis('off')
    axs[0].set_title('Original')
    axs[0].imshow(img, cmap = 'gray', vmin=0, vmax=255)
    axs[1].axis('off')
    axs[1].set_title('Equalizada')
    axs[1].imshow(img_out, cmap='gray', vmin=0, vmax=255)
    plt.show()
