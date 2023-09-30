import numpy as np
import matplotlib.pyplot as plt
import cv2

# funcao para redimensionar uma imagem
def resizeImg(img, sch, scw):
    '''
      img: imagem de entrada
      sch: fator de escala na altura
      scw: fator de escala na largura
    '''
    h, w, c = img.shape # dimensoes de img

    # aloca a nova imagem
    nh = int(round(h * sch))
    nw = int(round(w * scw))
    newImg = np.zeros((nh, nw, c), dtype=np.uint8)

    # calcula os fatores de escala
    sr = float(h / nh)
    sc = float(w / nw)

    #percorre a nova imagem usando loops
    for r in range(nh):    # nas linhas
        for c in range(nw):  # nas colunas
            rm = r * sr
            if rm >= h-1:
                rm = h - 1.5
            r0 = int(np.floor(rm))

            cm = c * sc
            if cm >= w-1:
                cm = h - 1.5
            c0 = int(np.floor(cm))

            deltar = rm-r0
            deltac = cm-c0

            Ia = img[r0, c0]
            Ib = img[r0+1, c0]
            Ic = img[r0, c0+1]
            Id = img[r0+1, c0+1]

            dr = rm - r0
            dc = cm - c0
            wa = (1.0 - dr) * (1.0 - dc)
            wb = dr * (1.0 - dc)
            wc = (1.0 - dr) * dc
            wd = dr * dc 

            newImg[r,c] = wa*Ia + wb*Ib + wc*Ic + wd*Id
    
    return newImg


if __name__ == '__main__':
    img = plt.imread("cat_puppy.jpg")
    
    factor = 2.0
    newImg = resizeImg(img, factor, factor)
   
    #ajusta o padrao de cores para apresentacao usando opencv
    
    #Concatena as imagens
    img_aux = None
    horizontal = None
    if factor > 1.0:
        img_aux = np.ones(newImg.shape, dtype=np.uint8)
        img_aux[0:(img.shape[0]), 0:(img.shape[1])] = img
        horizontal = np.hstack((img_aux, newImg))
    else:
        img_aux = np.ones(img.shape, dtype=np.uint8)
        img_aux[0:(newImg.shape[0]), 0:(newImg.shape[1])] = newImg
        horizontal = np.hstack((img, img_aux))
    
    
    # mostra as imagens usando matplotlib
    #plt.imshow(horizontal)
    #plt.show()
    
   
    # mostra as imagens com opencv
    horizontal = cv2.cvtColor(horizontal, cv2.COLOR_RGB2BGR)
    cv2.namedWindow("Original vs Resized", cv2.WINDOW_AUTOSIZE) 
    cv2.imshow("Original vs Resized", horizontal)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
