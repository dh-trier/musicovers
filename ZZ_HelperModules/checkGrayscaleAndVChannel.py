#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get grayscale value of all pixels and compare with V-channel from the HSV image.
"""


# general
import glob
from os.path import join
import os.path
import cv2

# same package
from ZZ_HelperModules import basic_image_functions as bif


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-005")


# ===============================
# Functions
# ===============================


def load_image_in_hsv(file):
    """
    Load image in BGR color space (OpenCV default) and convert to HSV space.
    :param file: Input image
    :return: Image in HSV color space
    """
    img = cv2.imread(file)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return image


# ========================
# Main
# ========================

def main(sourcedatafolder):
    abweichung_total = 0
    # Internetbeiträge zum Thema "HSV und Graustufen":
    # https://stackoverflow.com/questions/23811638/convert-hsv-to-grayscale-in-opencv
    # https://de.mathworks.com/matlabcentral/answers/312101-how-to-convert-gray-image-to-hsv-plane-v-value-image
    # https://stackoverflow.com/questions/38136291/why-the-gray-scale-image-is-different-from-value-channel-of-hsv-image?rq=1
    for file in glob.glob(join(sourcedatafolder, "*")):
        # load images
        image_1 = load_image_in_hsv(file)  # load with OpenCV
        image_2 = bif.mode(bif.load(file), 'gray')  # load with Pillow

        abweichung_img = 0
        count = 0
        for x in range(len(image_1)):  # compare V channel with gray pixel
            for y in range(len(image_1)):
                v_channel = image_1[x][y][2]  # x == row ; y == column
                gray_pixel = image_2.getpixel((y, x))  # y == row ; x == column
                abw_current = v_channel - gray_pixel  # berechne Abweichung
                abweichung_img += abw_current  # summiere Abweichungen für ein Bild
                count += 1

        # print(str(v_channel) + "  --  " + str(gray_pixel))
        print("Abweichung: " + str(abweichung_img/count))  # Durchschnittliche Abweichung je Bild
        print("----------")

        abweichung_total += abweichung_img/count  # füge Abweichung des einzelnen Bildes zu Gesamtabweichung hinzu

    print("Durchschnittliche Abweichung: " + str(abweichung_total/500))  # Durchschnittliche Abweichung in allen Bildern ; 500 ist die Anzahl der Testbilder


if __name__ == '__main__':
    main(sourcedatafolder)
