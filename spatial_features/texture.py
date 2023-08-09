from skimage import color
from skimage.filters import gabor, gaussian
from skimage.feature import graycomatrix, graycoprops
from pywt import dwt2
import numpy as np
import scipy as sp

class Gabor_Texture():
    def __init__(self, orient=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], frequency=[0.1, 0.2, 0.3, 0.4],
                 auto_band=False):
        self.orient = orient
        self.frequency = frequency
        self.auto_band = auto_band

    def get_image_energy(sefl, pixels):
        _, (cH, cV, cD) = dwt2(pixels.T, 'db1')
        energy = (cH ** 2 + cV ** 2 + cD ** 2).sum() / pixels.size
        return energy

    def get_energy_density(self, pixels):
        energy = self.get_image_energy(pixels)
        energy_density = energy / (pixels.shape[0] * pixels.shape[1])
        return round(energy_density * 100, 5)  # multiplying by 100 because the values are very small

    def get_magnitude(self, response):
        magnitude = np.array([np.sqrt(response[0][i][j] ** 2 + response[1][i][j] ** 2)
                              for i in range(len(response[0])) for j in range(len(response[0][i]))])
        return magnitude

    def gabor_texture(self, image):
        # Convert the image to grayscale
        image_gray = color.rgb2gray(image)

        # bandwidth computation
        if self.auto_band:
            # image energy density based bandwidth
            energy_density = self.get_energy_density(image_gray)
            band_width = abs(0.4 * energy_density - 0.5)
        else:
            # scikit learn default bandwidth
            band_width = 1

        # Define the range of orientations and frequencies
        orientations = self.orient
        frequencies = self.frequency

        # Initialize an array to store the filtered images
        filtered_images = []

        # Apply Gabor filter for each combination of orientation and frequency
        for orientation in orientations:
            for frequency in frequencies:
                # Construct the Gabor filter
                real, comp = gabor(image_gray, frequency=frequency, theta=orientation, bandwidth=band_width)
                # feature normalization
                #real = (real - np.min(real)) / (np.max(real) - np.min(real))
                #comp = (comp - np.min(comp)) / (np.max(comp) - np.min(comp))
                # get magnitude
                magnitude = self.get_magnitude([real, comp]).reshape(real.shape)
                # feature smoothing
                sigma = 0.5 * frequency
                smoothed = gaussian(magnitude, sigma)
                filtered_images.append(smoothed)

        return filtered_images

class PanTex_Texture():
    def __init__(self):
        print('developing pantex')


