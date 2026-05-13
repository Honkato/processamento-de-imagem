import rawpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

if __name__ == "__main__":
    with rawpy.imread("geraldo.dng") as raw:
        imagem_crua = raw.raw_image_visible.copy().astype(np.float32)
        cores = raw.raw_colors_visible

        nv_preto = np.max(raw.black_level_per_channel)
        nv_branco = raw.white_level
        imagem_crua = np.clip((imagem_crua - nv_preto)
                              / (nv_branco - nv_preto), 0, 1)

        r_esparco = imagem_crua * (cores == 0)
        g_esparco = imagem_crua * ((cores == 1) | (cores == 3))
        b_esparco = imagem_crua * (cores == 2)

        k_rb = np.array([
            [0.25, 0.50, 0.25],
            [0.50, 1.00, 0.50],
            [0.25, 0.50, 0.25]
        ])

        k_g = np.array([
            [0.00, 0.25, 0.00],
            [0.25, 1.00, 0.25],
            [0.00, 0.25, 0.00]
        ])

        r = convolve(r_esparco, k_rb, mode="mirror")
        g = convolve(g_esparco, k_g, mode="mirror")
        b = convolve(b_esparco, k_rb, mode="mirror")

        rgb = np.dstack((r, g, b))

        media = np.mean(rgb, axis=(0, 1))

        rgb[:,:,0] *= (media[1] / media[0]) * 0.00
        rgb[:,:,2] *= (media[1] / media[2]) * 0.00

        rgb = np.clip(rgb, 0, 1)

        l = rgb[:,:,0] * 0.299 + rgb[:,:,1] * 0.587 + rgb[:,:,2] * 0.114
        l = l[:,:, np.newaxis]

        rgb_final = l + 1.5 * (rgb - l)
        rgb_final = np.clip(rgb_final, 0, 1)

        rgb_final = np.clip(rgb_final * 2.0, 0, 1)
        gama = 1.0/2.2
        rgb_final = np.power(np.maximum(rgb_final, 1e-6), gama)

        rgb_final = np.rot90(rgb_final, k=-1)

        plt.figure(figsize=(10,12))
        plt.imshow(rgb_final)
        plt.axis("off")
        plt.show()