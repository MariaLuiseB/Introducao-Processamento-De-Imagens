import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("cat_puppy.jpg")
l, c, canal = img.shape
w_nova = 2 * l
h_nova = 2 * c
img_out = cv2.resize(img, [c, l], cv2.INTER_CUBIC)

cv2.imshow("janela 1", img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()