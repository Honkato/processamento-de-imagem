from PIL import Image, ImageDraw
import numpy as np


def converter_cinza(caminho_imagem):
    img_colorida = Image.open(caminho_imagem)

    largura, altura = img_colorida.size

    img_cinza = Image.new("L", (largura, altura))

    pixels_coloridos = img_colorida.load()
    pixels_cinza = img_cinza.load()

    for x in range(largura):
        for y in range(altura):
            r,g,b = pixels_coloridos[x,y]
            cinza = int(r * 0.299 + g * 0.587 + b * 0.114)
            pixels_cinza[x,y] = cinza
    resultado = Image.new("RGB", (largura * 2, altura))
    resultado.paste(img_colorida, [0, 0])
    resultado.paste(img_cinza, [largura, 0])
    resultado.show()

if __name__ == '__main__':
    converter_cinza('james_web_photo.jpg')