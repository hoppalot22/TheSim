import numpy as np
import matplotlib.pyplot as plt
import pickle
import opensimplex
from PIL import Image # Depends on the Pillow lib
import opensimplex as simplex

WIDTH = 256
HEIGHT = 256
FEATURE_SIZE = 24.0


def Main():
    # im = Image.new('L', (WIDTH, HEIGHT))
    # for y in range(0, HEIGHT):
    #     for x in range(0, WIDTH):
    #         value = simplex.noise4(x / FEATURE_SIZE, y / FEATURE_SIZE, 0.0, 0.0)
    #         color = int((value + 1) * 128)
    #         im.putpixel((x, y), color)
    # #im.show()

    im = Image.new('L', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise4(x / FEATURE_SIZE, y / FEATURE_SIZE, 0.0, 0.0)
            color = int((value + 1) * 127)
            im.putpixel((x, y), color)
    im.save('noise4d.png')


if __name__ == "__main__":
    Main()