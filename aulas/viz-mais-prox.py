import numpy as np
import matplotlib.pyplot as plt
import cv2

# funcao para redimensionar uma imagem
def resizeImg(img, sch, scw): # fatores de escala : se quiser dobrar é só colocar sch = 2 e scw = 2
    '''
      img: imagem de entrada
      sch: fator de escala na altura
      scw: fator de escala na largura
    '''
    h, w, c = img.shape # dimensoes de img (linhas, colunas, planos de cor)

    # aloca a nova imagem
    nh = int(round(h * sch))
    nw = int(round(w * scw))
    newImg = np.zeros((nh, nw, c), dtype=np.uint8)

    # indices dos pixels da nova imagem
    Ro = np.arange(nh)
    Co = np.arange(nw)

    # calcula os fatores de escala
    Sr = float(h) / float(nh) # h = numero de linhas da imagem original; nh= nova
    Sc = float(w) / float(nw) # w = numero de colunas da imagem original; nw = nova

    #calcula o mapeamento dos indices
    Rm = np.floor(Ro * Sr).astype(int)
    Cm = np.floor(Co * Sc).astype(int)

    coord_new = [(x,y) for x in Ro for y in Co] # todas as coodenadas de pixel da imagem nova
    coord_ori = [(x,y) for x in Rm for y in Cm] # todos as coordendas novas mapeadas para a original
    for cn, co in zip(coord_new, coord_ori):
        newImg[cn] = img[co]

    return newImg



if __name__ == '__main__':
    img = plt.imread("cat_puppy.jpg")
    
    factor = 1.5
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
