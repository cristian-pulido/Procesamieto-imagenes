import os
import sys
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]


import nibabel as nib
import numpy as np
from dipy.core.gradients import gradient_table
from dipy.io.trackvis import save_trk
from tareas.dependencias import definitions as d
import collections
###################
folder=os.path.dirname(path_input)
file_inMask=""
for i in os.listdir(folder):
    if "masked_mask" in i:
        file_inMask=os.path.join(folder,i)

folder_sujeto=path_output
for l in os.listdir(folder_sujeto):
    if "TENSOR" in l and "bval" in l:
        fbval=os.path.join(folder_sujeto, l)
    if "TENSOR" in l and "bvec" in l:
        fbvec=os.path.join(folder_sujeto, l)


#################
if not os.path.exists(os.path.join(path_output,'feature.out')):
    list_path_atlas_1=[]
    with open(os.path.join(folder,"list_path_atlas_1.txt")) as f:
        for line in f:
            list_path_atlas_1.append(line.strip())


    list_path_atlas_2=[]
    with open(os.path.join(folder,"list_path_atlas_2.txt")) as f:
        for line in f:
            list_path_atlas_2.append(line.strip())


    list_path_atlas_3=[]
    with open(os.path.join(folder,"list_path_atlas_3.txt")) as f:
        for line in f:
            list_path_atlas_3.append(line.strip())


    list_path_atlas_4=[]
    with open(os.path.join(folder,"list_path_atlas_4.txt")) as f:
        for line in f:
            list_path_atlas_4.append(line.strip())



    # def to_generate_bunddle(path_dwi_input, path_output, path_binary_mask, path_bval, path_bvec, bunddle_rules, atlas_dict):
    from dipy.reconst.shm import CsaOdfModel
    from dipy.data import default_sphere
    from dipy.direction import peaks_from_model
    from dipy.tracking.local import LocalTracking
    from dipy.tracking import utils
    from dipy.tracking.local import ThresholdTissueClassifier
    from dipy.tracking._utils import (_mapping_to_voxel, _to_voxel_coordinates)

    print(d.separador + 'starting of model')

    dwi_img = nib.load(path_input)
    dwi_data = dwi_img.get_data()
    dwi_affine = dwi_img.affine

    dwi_mask_data = nib.load(file_inMask).get_data().astype(bool)

    g_tab = gradient_table(fbval, fbvec)

    csa_model = CsaOdfModel(g_tab, sh_order=6)

    csa_peaks = peaks_from_model(csa_model, dwi_data, default_sphere, sh_order=6,
                                 relative_peak_threshold=.8,
                                 min_separation_angle=35, mask=dwi_mask_data)

    print(d.separador + 'ending of model')

    print(d.separador + 'starting of classifier')

    classifier = ThresholdTissueClassifier(csa_peaks.gfa, .2)

    print(d.separador + 'ending of classifier')

    list_bunddle = []

    ruleNumber = 1

    indexHarvardOxfortCortical = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                  24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                                  46, 47]

    atlas_dict = {'Morel': list_path_atlas_2, 'AAN': list_path_atlas_1, 'HarvardOxfordCort': list_path_atlas_4,
    'HypothalamusAtlas': list_path_atlas_3}

    bunddle_rules = [
            (('AAN', [1, 3]), ('Morel', [4, 5, 6, 18, 42, 43, 44, 56]), ('HarvardOxfordCort', indexHarvardOxfortCortical)),
            (('Morel', [4, 5, 6, 18, 42, 43, 44, 56]), ('HarvardOxfordCort', indexHarvardOxfortCortical)),
    (('HypothalamusAtlas', [1, 2, 3]), None)]


    for rule in bunddle_rules:
        print('Starting ROI reconstruction')

        for elementROI in rule[0][1]:
            if not ('roi' in locals()):
                roi = nib.load(atlas_dict[rule[0][0]][elementROI]).get_data().astype(bool)
            else:
                roi = roi | nib.load(atlas_dict[rule[0][0]][elementROI]).get_data().astype(bool)

        nib.save(nib.Nifti1Image(roi.astype(np.float32), dwi_affine),os.path.join( path_output , 'roi_rule_' + str(ruleNumber) + '.nii.gz'))

        seeds = utils.seeds_from_mask(roi, density=[2, 2, 2], affine=dwi_affine)

        streamlines = LocalTracking(csa_peaks, classifier, seeds, dwi_affine, step_size=1)

        streamlines = [s for s in streamlines if s.shape[0] > 30]

        streamlines = list(streamlines)

        #save_trk(path_output + 'bundleROI_rule_' + str(ruleNumber) + '.trk', streamlines, dwi_affine, roi.shape)

        print('Finished ROI reconstruction')

        print('Starting TARGET filtering')

        bunddle = []

        lin_T, offset = _mapping_to_voxel(dwi_affine, None)

        if rule[1] is not None:
            for elementROI in rule[1][1]:
                if not ('target' in locals()):
                    target = nib.load(atlas_dict[rule[1][0]][elementROI]).get_data().astype(bool)
                else:
                    target = target | nib.load(atlas_dict[rule[1][0]][elementROI]).get_data().astype(bool)

            #nib.save(nib.Nifti1Image(target.astype(np.float32), dwi_affine), path_output + 'target_rule_' + str(ruleNumber) + '.nii.gz')

            for sl in streamlines:
                # sl += offset
                # sl_Aux = np.copy(sl)
                sl_Aux = sl
                sl = _to_voxel_coordinates(sl, lin_T, offset)
                i, j, k = sl.T
                labelsROI = target[i, j, k]

                if sum(labelsROI) > 0:
                    bunddle.append(sl_Aux)
        else:
            bunddle = streamlines

        #save_trk(path_output + 'bundle_rule_' + str(ruleNumber) + '.trk', bunddle, dwi_affine, roi.shape)

        print('Finished TARGET filtering')

        if len(rule) == 3:  # If is necessary other filtering (exclusition)

            for elementROI in rule[2][1]:
                if not ('roiFiltered' in locals()):
                    roiFiltered = nib.load(atlas_dict[rule[2][0]][elementROI]).get_data().astype(bool)
                else:
                    roiFiltered = roiFiltered | nib.load(atlas_dict[rule[2][0]][elementROI]).get_data().astype(bool)

            bunddleFiltered = []

            for b in bunddle:
                b_Aux = b
                b = _to_voxel_coordinates(b, lin_T, offset)
                i, j, k = b.T
                labelsROI = roiFiltered[i, j, k]

                if sum(labelsROI) == 0:
                    bunddleFiltered.append(b_Aux)


            print('Finished exclusive filtering:')
            if 'roiFiltered' in locals():
                del roiFiltered
        else:
            if 'bunddleFiltered' in locals():
                del bunddleFiltered

            bunddleFiltered = bunddle

        save_trk(os.path.join(path_output, 'bundle_rule_' + str(ruleNumber) + '.trk'), bunddleFiltered, dwi_affine, roi.shape)

        if 'roi' in locals():
            del roi
        if 'target' in locals():
            del target

        ruleNumber = ruleNumber + 1

        list_bunddle.append(bunddleFiltered)
    print(list_bunddle)

    roi_rules = collections.OrderedDict()
    roi_rules['AAN'] = [1, 3]
    roi_rules['Morel'] = [4, 5, 6, 18, 42, 43, 44, 56]
    roi_rules['HypothalamusAtlas'] = [1, 2, 3]


    list_maps=[]
    with open(os.path.join(folder,"list_maps.txt")) as f:
        for line in f:
            list_maps.append(line.strip())


    features=[]

    # Measuring over streamlines
    for bunddle in list_bunddle:
        features.append(len(bunddle)) # Fibers number

    # Measuring over roi list
    for key in roi_rules.keys():
        print(key)
        for elementROI in roi_rules[key]:
            print(atlas_dict[key][elementROI])
            roi = nib.load(atlas_dict[key][elementROI]).get_data().astype(bool)

            for map in list_maps:
                data_map = nib.load(map).get_data()[roi]
                features.append(np.mean(data_map))
                features.append(np.min(data_map))
                features.append(np.max(data_map))
                features.append(np.std(data_map))

    np.savetxt(os.path.join(path_output, 'feature.out'), np.array(features), delimiter=' ', fmt='%s')

print(os.path.join(path_output,'feature.out'))
print(path_input)