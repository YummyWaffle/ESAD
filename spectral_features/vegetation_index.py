import numpy as np


def simple_ratio(b1_img, b2_img):
    return b1_img / (b2_img + 1e-10)


def norm_diff(b1_img, b2_img):
    return (b1_img - b2_img) / (b1_img + b2_img + 1e-10)


class VI():
    def __init__(self):
        print('developing vegetation index')

    def NDVI(self, red, nir):
        return [norm_diff(nir, red),]

    def VARI(self, green, red):
        # Gitelson et al., Novel algorithms for remote sensing estimation of vegetation fraction, RSE
        # VARI is a vegetation index for visible camera
        return [norm_diff(green, red),]

    def VARI_ARVI(self, blue, green, red):
        # Gitelson et al., Novel algorithms for remote sensing estimation of vegetation fraction, RSE
        # Kaufuman et al., Atmospherically resistant vegetation index (ARVI) for EOS-MODIS
        # Rectify VARI by using ARVI Techniques, which lower the sensitivity of VARI to atmosphere.
        return [(green - red) / (green + green - blue + 1e-10),]