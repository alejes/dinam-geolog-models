import cv2
import numpy as np


def create(height: int, width: int, white: bool=False) -> np.ndarray:
    image = np.zeros((height, width), np.uint8)
    if white:
        image.fill(255)
    return image


def load(image_name: str) -> np.ndarray:
    return cv2.imread(image_name, 1)


def show(*images: np.ndarray):
    for i, image in enumerate(images):
        cv2.imshow('image-' + str(i), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    _height = 10
    _width = 10

    _image = create(_height, _width)

    _image[:, 0: int(0.5 * _width)] = (255, 0, 0)      # (B, G, R)
    _image[:, int(0.5 * _width): _width] = (0, 255, 0)

    show(_image)

