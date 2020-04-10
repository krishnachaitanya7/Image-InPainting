import imageio
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt


# https://note.nkmk.me/en/python-opencv-pillow-image-size/
# TODO: Find the image specifications standards in Python. 3x1024x1024 or 1024x1024x3?
if __name__ == "__main__":
    im = imageio.imread('32435.png')
    im_resized = resize(im, (1024, 1024), anti_aliasing=True)
    mask_img = []
    for _ in range(3):
        mask_img.append(im_resized)
    mask_img = np.array(mask_img)
    plt.imshow(mask_img)
    plt.show()
    im = np.asarray(imageio.imread('27.jpg'))
    idx = (im_resized == 0)
    im[idx] = mask_img[idx]
    plt.show(im)
