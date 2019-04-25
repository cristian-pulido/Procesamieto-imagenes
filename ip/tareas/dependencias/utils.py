__author__ = 'Jrudascas'

import os
from os import listdir
from os.path import isfile, join
import nibabel as nib
import numpy as np
import scipy.ndimage as ndim
import tareas.dependencias.definitions as d


def to_extract_filename_extention(path_input):
    return path_input.split('/')[path_input.split('/').__len__() - 1]


def to_extract_foldername(path_input):
    return path_input.split('/')[path_input.split('/').__len__() - 2]


def to_extract_filename(path_input):
    refName = to_extract_filename_extention(path_input)
    return refName.split('.')[0]


def to_extract_extension(path_input):
    refName = to_extract_filename_extention(path_input)
    return refName.split('.')[1]


def to_delete_files(folder):
    files_dump = [join(folder, c) for c in listdir(folder)]
    files_dump = filter(lambda c: isfile(c), files_dump)
    [os.remove(c) for c in files_dump]


def to_validate_extention(path, extList):
    if to_extract_extension(path) in extList:
        return True
    else:
        return False


def what_kind_neuroimage_is(path):
    import nibabel as nib

    def is_t1(path):
        try:
            image = nib.load(path)
        except:
            return False

        if len(image.shape) == 3:
            return True
        else:
            return False

    def is_dwi(path):
        try:
            image = nib.load(path)
        except:
            return False

        if len(image.shape) == 4 and image.shape[-1] > 1 and image.shape[-1] < 50:
            return True
        else:
            return False

    if to_extract_extension(path) == 'bvec':
        return 'bvec'
    elif to_extract_extension(path) == 'bval':
        return 'bval'
    elif to_validate_extention(path, ['nii', 'gz']):
        if is_t1(path):
            return 't1'
        elif is_dwi(path):
            return 'dwi'
        else:
            return 'unknown'

def registration_atlas_to(path_atlas, path_output, affine, mapping):
    img_atlas = nib.load(path_atlas)
    atlas_data = img_atlas.get_data()

    indexs = np.unique(atlas_data)

    ref_name = to_extract_filename(path_atlas)
    list_path_roi = []

    for index in indexs:
        roi = (atlas_data == index)
        # warped_roi = mapping.transform_inverse(roi.astype(int)*255, interpolation='nearest')
        warped_roi = mapping.transform_inverse(ndim.binary_dilation(roi).astype(int), interpolation='nearest')

        warped_roi = ndim.binary_dilation(warped_roi)
        warped_roi = ndim.binary_erosion(warped_roi)

        bin_warped_roi = np.ceil(warped_roi)

        filled_warped_roi = ndim.binary_fill_holes(bin_warped_roi.astype(int)).astype(int)

        nib.save(nib.Nifti1Image(filled_warped_roi.astype(np.float32), affine),
                 os.path.join(path_output, ref_name + '_ROI_' + str(index) + d.extension))

        list_path_roi.append(os.path.join(path_output, ref_name + '_ROI_' + str(index) + d.extension))
        # print("ROI # " + str(index) + " for " + ref_name + " Atlas, has been saved")

        if not ('registered_atlas' in locals()):
            registered_atlas = np.zeros(filled_warped_roi.shape)

        registered_atlas[filled_warped_roi != 0] = index

    nib.save(nib.Nifti1Image(registered_atlas.astype(np.float32), affine), os.path.join(path_output, ref_name + '_registered_' + d.extension))

    return list_path_roi