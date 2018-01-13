#!/usr/bin/env python3

"""
This module offers some basic functions for image processing with Pillow.
"""

from os.path import join
from PIL import Image


def load(file):
    """
    Load an Image file
    :param file: Source file
    :return: Image object
    """
    image = Image.open(file)
    return image


def save(image, basename, targetdatafolder):
    """
    Save Image as JPEG
    :param image: Sourcefile
    :param basename: Basename
    :param targetdatafolder: Target data folder
    :return: Nothing
    """
    filename = join(targetdatafolder, basename + ".jpg")
    try:
        image.save(filename, "JPEG")
    except IOError:
        print("error for", basename, filename)


def resize(image, a, b):
    """
    Resize an Image
    :param image: Sourcefile
    :param a: # TODO Is this width or height?!
    :param b: # TODO Is this width or height?!
    :return: Resized Image
    """
    image = image.resize((a, b))
    return image


def mode(image, mode):
    """
    Convert Image to another mode
    (see also: https://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes)
    :param image: Sourcefile
    :return: Image object
    """
    if mode == "gray":
        image = image.convert("L")
    elif mode == "bw":
        image = image.convert("1")
    elif mode == "RGB":
        image = image.convert("RGB")
    elif mode == "CMYK":
        image = image.convert("CMYK")

    return image
