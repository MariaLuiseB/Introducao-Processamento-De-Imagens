import numpy as np
import matplotlib.pyplot as plt
import cv2

def gaussian_kernel(size, sigma):
    kernel = np.fromfunction(
        lambda x, y: (1 / (2 * np.pi * sigma**2)) * np.exp(-((x - size // 2)**2 + (y - size // 2)**2) / (2 * sigma**2)),
        (size, size)
    )
    return kernel / np.sum(kernel)

def convolve2d(image, kernel):
    kernel_size = kernel.shape[0]
    offset = kernel_size // 2
    convolved_image = np.zeros_like(image)

    for channel in range(image.shape[2]):  # Percorre cada canal de cor (R, G, B)
        for y in range(offset, image.shape[0] - offset):
            for x in range(offset, image.shape[1] - offset):
                convolved_image[y, x, channel] = np.sum(
                    image[y - offset:y + offset + 1, x - offset:x + offset + 1, channel] * kernel
                )

    return convolved_image

# Carregando uma imagem usando OpenCV
image = cv2.imread('imagem.jpg')  # Substitua pelo caminho da sua imagem
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convertendo de BGR para RGB

# Parâmetros do filtro Gaussiano
kernel_size = 5
sigma = 1.0

# Criando o kernel Gaussiano
kernel = gaussian_kernel(kernel_size, sigma)

# Aplicando a convolução manualmente à imagem
blurred_image = convolve2d(image_rgb, kernel)

# Exibindo as imagens original e suavizada
plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title('Imagem Original')

plt.subplot(1, 2, 2)
plt.imshow(blurred_image)
plt.title('Imagem Suavizada (Filtro Gaussiano)')
plt.show()
