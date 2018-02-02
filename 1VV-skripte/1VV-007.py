#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resize images to 500 x 500 pixels AND convert to greyscale.
"""

import os
import glob
from os.path import join
import os.path

# same package
from ZZ_HelperModules import basic_image_functions as bif, docfile


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-001")
targetdatafolder = join(workdir, "2VV-daten", "2VV-002")
documentationfile = join(workdir, "2VV-daten", "2VV-002.txt")
docstring = __doc__


# ===============================
# Main
# ===============================

def main(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail):
    if not os.path.exists(targetdatafolder):
        os.makedirs(targetdatafolder)
    for file in glob.glob(sourcedatafolder + "/*"):
        basename, ext = os.path.basename(file).split(".")
        image = bif.load(file)
        image = bif.resize(image, 500, 500)
        image = bif.mode(image, "gray")
        bif.save(image, basename, targetdatafolder)
    docfile.write(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail, __file__)


main(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail)
