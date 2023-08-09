import os
import skimage.transform as st
import matplotlib.pyplot as plt
from osgeo import gdal
import shutil
from tqdm import tqdm
import spatial_features.texture as TexFeat
import spectral_features.vegetation_index as VIFeat
import feature_fusion.DimReduce as DimReduce
import numpy as np
import object_features.statistic as OBST
import correlation_funcs.spatial_correlation as SPC

bands = []

save_dir = 'xBD_Gabor'
if os.path.exists(save_dir):
    shutil.rmtree(save_dir)
os.mkdir(save_dir)

dataset = {}
dataset_dir = 'D:/A_BNU/xBD/xview2_geotiff.tar/geotiffs/tier1/images'
files = os.listdir(dataset_dir)
files = list(filter(lambda x: 'post' in x, files))

event_files = []

events = ['volcano', 'fire', 'flood', 'earthquake']

for event in events:
    for file in files:
        if event in file:
            event_files.append(file)

files = event_files

for file in files:
    id = file.split('_')[0] + '_' + file.split('_')[1]
    imgp_pre = dataset_dir + '/' + file.replace('post', 'pre')
    imgp_post = dataset_dir + '/' + file
    dataset[id] = [imgp_pre, imgp_post]

w_size = 30
for key in tqdm(dataset.keys()):
    # Image Is Organized As CWH Format
    img_pre = gdal.Open(dataset[key][0]).ReadAsArray().transpose((1, 2, 0))
    img_pre = (img_pre - np.min(img_pre)) / (np.max(img_pre) - np.min(img_pre))
    img_post = gdal.Open(dataset[key][1]).ReadAsArray().transpose((1, 2, 0))
    img_post = (img_post - np.min(img_post)) / (np.max(img_post) - np.min(img_post))

    # Pixel-Based Feature Extraction
    pre_pixel_feats = []
    aft_pixel_feats = []

    # Color / Spectral Feature Extraction: (Spectral_Dim, H, W)
    spectral_extractor = VIFeat.VI()
    spectral_pre = spectral_extractor.VARI(img_pre[:, :, 1], img_pre[:, :, 0])
    spectral_aft = spectral_extractor.VARI(img_post[:, :, 1], img_post[:, :, 0])
    pre_pixel_feats.extend(spectral_pre)
    pre_pixel_feats.extend([img_pre[:, :, 0], img_pre[:, :, 1], img_pre[:, :, 2]])
    aft_pixel_feats.extend(spectral_aft)
    aft_pixel_feats.extend([img_post[:, :, 0], img_post[:, :, 1], img_post[:, :, 2]])

    # Texture Feature Extraction: (Texture_Dim, H, W)
    texture_extractor = TexFeat.Gabor_Texture()
    texture_pre = texture_extractor.gabor_texture(img_pre)
    texture_aft = texture_extractor.gabor_texture(img_post)
    pre_pixel_feats.extend(texture_pre)
    aft_pixel_feats.extend(texture_aft)

    # Pixel-Based Feature Fusion
    pre_pixel_feats = np.array(pre_pixel_feats).transpose((1, 2, 0))
    aft_pixel_feats = np.array(aft_pixel_feats).transpose((1, 2, 0))
    h, w, feat_dim = aft_pixel_feats.shape
    pre_pixel_feats = pre_pixel_feats.reshape((h * w, feat_dim))
    aft_pixel_feats = aft_pixel_feats.reshape((h * w, feat_dim))

    pre_pixel_feat = DimReduce.apply_pca(pre_pixel_feats).reshape((h, w))
    aft_pixel_feat = DimReduce.apply_pca(aft_pixel_feats).reshape((h, w))

    # Object-Based Feature Extraction
    windows_size = 30
    pre_obj_var = OBST.var_image(pre_pixel_feat, windows_size)
    aft_obj_var = OBST.var_image(aft_pixel_feat, windows_size)

    # Spatial-Temporal Correlation-Based Anomaly Detection
    pre_moran = SPC.local_moran(pre_obj_var)
    post_moran = SPC.local_moran(aft_obj_var)

    plt.figure(figsize=(13, 10))

    plt.subplot(231)
    plt.imshow(img_pre)
    plt.axis('off')

    plt.subplot(232)
    plt.imshow(img_post)
    plt.axis('off')

    plt.subplot(233)
    plt.imshow(pre_moran)
    plt.axis('off')

    plt.subplot(234)
    plt.imshow(post_moran)
    plt.axis('off')

    plt.subplot(235)
    change_mask = (pre_moran != post_moran)
    change_mask = st.resize(change_mask, (img_post.shape[0], img_post.shape[1]), order=0, preserve_range=True,
                            anti_aliasing=False)
    change_mask = np.expand_dims(change_mask, axis=-1)
    plt.imshow(change_mask * img_pre)
    plt.axis('off')

    plt.subplot(236)
    plt.imshow(change_mask * img_post)
    plt.axis('off')

    plt.suptitle(key, fontsize=18)

    plt.savefig(save_dir + '/' + key + '.png')
    plt.close()