import sys
import os

sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]


path_input = sys.argv[1]
path_output = sys.argv[2]


from tareas.dependencias import utils
from tareas.dependencias import definitions as d
import nibabel as nib
import numpy as np
from dipy.denoise.noise_estimate import estimate_sigma
from dipy.denoise.nlmeans import nlmeans
print('    - running NonLocal Mean algoritm...')

finalFileName = os.path.join(path_output, utils.to_extract_filename(path_input) + d.id_non_local_mean + d.extension)

if not (os.path.exists(finalFileName)):
    img = nib.load(path_input)
    data = img.get_data()

    newData = np.zeros(data.shape)
    gradientDirections = data.shape[-1]

    for index in range(gradientDirections):
        print(index)
        sigma = estimate_sigma(data[:, :, :, index], N=8)
        newData[:, :, :, index] = nlmeans(data[:, :, :, index], sigma=sigma)

    nib.save(nib.Nifti1Image(newData.astype(np.float32), img.affine), finalFileName)
print(finalFileName)
