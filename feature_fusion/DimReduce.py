from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

def apply_pca(array):
    """
    :param array: array of shape pXd
    :return: reduced and transformed array of shape dX1
    """
    # apply dimensionality reduction to the input array
    standardized_data = StandardScaler().fit_transform(array)
    pca = PCA(n_components=1)
    pca.fit(standardized_data)
    transformed_data = pca.transform(standardized_data)
    return transformed_data

def apply_tsne(array):
    standardized_data = StandardScaler().fit_transform(array)
    tsne = TSNE(n_components=1)
    tsne.fit(standardized_data)
    transformed_data = tsne.transform(standardized_data)
    return transformed_data