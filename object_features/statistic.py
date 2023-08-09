import numpy as np
import math

def mean_image(feature_image, window_size=10):
    row, col = feature_image.shape
    nrow = math.ceil(row / window_size)
    ncol = math.ceil(col / window_size)
    var_mat = np.zeros([nrow, ncol])
    for i in range(nrow):
        for j in range(ncol):
            row_min = i * window_size
            col_min = j * window_size
            row_max = min(window_size * (i + 1), row)
            col_max = min(window_size * (j + 1), col)
            patch = feature_image[row_min: row_max, col_min: col_max]
            var_mat[i,j] = np.mean(patch)
    return var_mat

def var_image(feature_image, window_size=10):
    row, col = feature_image.shape
    nrow = math.ceil(row / window_size)
    ncol = math.ceil(col / window_size)
    var_mat = np.zeros([nrow, ncol])
    for i in range(nrow):
        for j in range(ncol):
            row_min = i * window_size
            col_min = j * window_size
            row_max = min(window_size * (i + 1), row)
            col_max = min(window_size * (j + 1), col)
            patch = feature_image[row_min: row_max, col_min: col_max]
            var_mat[i,j] = np.var(patch)
    return var_mat