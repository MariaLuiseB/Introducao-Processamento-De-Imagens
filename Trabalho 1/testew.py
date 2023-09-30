import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np

path = filedialog.askopenfilename()

if path:
    img = cv2.imread(path)
    print(img.shape[2])

    r, g, b = cv2.split(img)

    r_out = np.histogram(r, bins=256, range=(0, 256))
    g_out = np.histogram(g, bins=256, range=(0, 256))
    b_out = np.histogram(b, bins=256, range=(0, 256))

    img_out = np.stack( (r_out[0], g_out[0], b_out[0]), axis=1)
    plt.plot(img_out)
    plt.show()