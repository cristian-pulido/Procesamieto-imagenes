__author__ = 'Jrudascas'

import numpy as np
from dipy.align.metrics import CCMetric, EMMetric, SSDMetric
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration

from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)

from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)
import warnings

warnings.filterwarnings("always")

syn_metric_dict = {'CC': CCMetric,
                   'EM': EMMetric,
                   'SSD': SSDMetric}


def syn_registration(moving, static,
                     moving_grid2world=None,
                     static_grid2world=None,
                     step_length=0.25,
                     metric='CC',
                     dim=3,
                     level_iters=[10, 10, 5],
                     sigma_diff=2.0,
                     prealign=None):
    """
    Register a source image (moving) to a target image (static)
    Parameters
    ----------
    moving : ndarray
        The source image data to be registered
    moving_grid2world : array, shape (4,4)
        The affine matrix associated with the moving (source) data.
    static : ndarray
        The target image data for registration
    static_grid2world : array, shape (4,4)
        The affine matrix associated with the static (target) data
    metric : string, optional
        The metric to be optimized. One of `CC`, `EM`, `SSD`, Default: CCMetric.
    dim: int (either 2 or 3), optional
       The dimensions of the image domain. Default: 3
    level_iters : list of int, optional
        the number of iterations at each level of the Gaussian Pyramid (the
        length of the list defines the number of pyramid levels to be
        used).
    Returns
    -------
    warped_moving : ndarray
        The data in `moving`, warped towards the `static` data.
    forward : ndarray (..., 3)
        The vector field describing the forward warping from the source to the target.
    backward : ndarray (..., 3)
        The vector field describing the backward warping from the target to the source
    """
    use_metric = syn_metric_dict[metric](dim, sigma_diff=sigma_diff)

    sdr = SymmetricDiffeomorphicRegistration(use_metric, level_iters,
                                             step_length=step_length)
    mapping = sdr.optimize(static, moving,
                           static_grid2world=static_grid2world,
                           moving_grid2world=moving_grid2world,
                           prealign=prealign)

    warped_moving = mapping.transform(moving)
    return warped_moving, mapping


def resample(moving, static, moving_grid2world, static_grid2world):
    """
    """
    identity = np.eye(4)
    affine_map = AffineMap(identity,
                           static.shape, static_grid2world,
                           moving.shape, moving_grid2world)
    resampled = affine_map.transform(moving)


# Affine registration pipeline:
affine_metric_dict = {'MI': MutualInformationMetric}


def c_of_mass(moving, static, static_grid2world, moving_grid2world,
              reg, starting_affine, params0=None):
    transform = transform_centers_of_mass(static, static_grid2world,
                                          moving, moving_grid2world)
    transformed = transform.transform(moving)
    return transformed, transform.affine, transform


def translation(moving, static, static_grid2world, moving_grid2world,
                reg, starting_affine, params0=None):
    transform = TranslationTransform3D()
    translation = reg.optimize(static, moving, transform, params0,
                               static_grid2world, moving_grid2world,
                               starting_affine=starting_affine)

    return translation.transform(moving), translation.affine, translation


def rigid(moving, static, static_grid2world, moving_grid2world,
          reg, starting_affine, params0=None):
    transform = RigidTransform3D()
    rigid = reg.optimize(static, moving, transform, params0,
                         static_grid2world, moving_grid2world,
                         starting_affine=starting_affine)
    return rigid.transform(moving), rigid.affine, rigid


def affine(moving, static, static_grid2world, moving_grid2world,
           reg, starting_affine, params0=None):
    transform = AffineTransform3D()
    affine = reg.optimize(static, moving, transform, params0,
                          static_grid2world, moving_grid2world,
                          starting_affine=starting_affine)

    return affine.transform(moving), affine.affine,affine


def affine_registration(moving, static,
                        moving_grid2world=None,
                        static_grid2world=None,
                        nbins=32,
                        sampling_prop=None,
                        metric='MI',
                        pipeline=[c_of_mass, translation, rigid, affine],
                        level_iters=[10000, 1000, 100],
                        sigmas=[3.0, 1.0, 0.0],
                        factors=[4, 2, 1],
                        params0=None):
    """
    Find the affine transformation between two 3D images
    """

    if len(moving.shape) == 4:
        data=moving
        moving = moving[:,:,:,0]

    # Define the Affine registration object we'll use with the chosen metric:
    use_metric = affine_metric_dict[metric](nbins, sampling_prop)
    affreg = AffineRegistration(metric=use_metric,
                                level_iters=level_iters,
                                sigmas=sigmas,
                                factors=factors)
    
    # Bootstrap this thing with the identity:
    starting_affine = np.eye(4)
    # Go through the selected transformation:

    for func in pipeline:
        transformed, starting_affine, transform = func(moving, static,
                                    static_grid2world,
                                    moving_grid2world,
                                    affreg, starting_affine,
                                    params0)
    try:
        transformed = np.zeros((static.shape[0], static.shape[1], static.shape[2], data.shape[-1]))
        for volume in range(data.shape[-1]):
            transformed[:,:,:,volume]=transform.transform(data[:,:,:,volume])
    except:
        print("NO Data time")


    return transformed, starting_affine
