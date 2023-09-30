import cv2
import numpy as np

# Carregue a imagem
imagem = cv2.imread('test_images\lena_gray_256.tif')

# Verifique se a imagem foi carregada corretamente
if imagem is not None:
    # Aplicar a transformação logarítmica
    imagem_log = cv2.log(imagem.astype(np.float32) + 1.0)
    
    # Normalizar a imagem resultante para o intervalo de 0 a 255
    imagem_log = (imagem_log - np.min(imagem_log)) / (np.max(imagem_log) - np.min(imagem_log)) * 255.0
    
    # Converter de volta para uint8
    imagem_log = np.uint8(imagem_log)
    
    # Exibir a imagem original e a imagem transformada
    cv2.imshow('Imagem Original', imagem)
    cv2.imshow('Imagem com Transformação Logarítmica', imagem_log)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('Não foi possível carregar a imagem.')
