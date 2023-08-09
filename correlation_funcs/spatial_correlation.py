import numpy as np
from libpysal.weights import lat2W
from pysal.explore.esda.moran import Moran_Local
import matplotlib.pyplot as plt

def local_moran(feat_map):
    w = lat2W(feat_map.shape[0], feat_map.shape[1])
    moran_local = Moran_Local(feat_map.flatten(), w)
    response =  np.reshape(moran_local.q, feat_map.shape)
    return response