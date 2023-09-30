import numpy as np
import matplotlib.pyplot as plt

def gamma_transform(img, gamma):
    c = 255.0 / (255.0**gamma)
    img_gamma = c * (img.astype(np.float64))**gamma
    return img_gamma.astype(np.uint8)

if __name__ == '__main__':
    # Le a imagem
    #img = plt.imread('fractured_spine.tif')
    img = plt.imread('washed_out_aerial_image.tif')
    img_gamma = gamma_transform(img, 5.0)

    # Plota lado a lado
    fig, axs = plt.subplots(1, 2)
    axs[0].axis('off')
    axs[0].set_title('Original')
    axs[0].imshow(img, cmap='gray')
    axs[1].axis('off')
    axs[1].set_title('Gamma')
    axs[1].imshow(img_gamma, cmap='gray')
    plt.show()
