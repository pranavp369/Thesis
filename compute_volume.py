# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 02:19:16 2023

@author: prana
"""

import SimpleITK as sitk
import nibabel as nib
import numpy as np


stats = sitk.StatisticsImageFilter()

#image = sitk.ReadImage(r"C:\Users\prana\OneDrive\Desktop\Thesisvenv\Output_sub-OAS30001_sess-d0129_run-01_T1w\single\complete_segmentation.nii.gz")

img = nib.load(r"C:\Users\prana\OneDrive\Desktop\Thesisvenv\Output_sub-OAS30001_sess-d0129_run-01_T1w\single\complete_segmentation.nii.gz")

label_lookup = {
                        'Left-Lateral-Ventricle': 4,
                        'Left-Inf-Lat-Vent': 5,
                        'Left-Cerebellum-White-Matter': 7,
                        'Left-Cerebellum-Cortex': 8,
                        'Left-Thalamus-Proper': 10,
                        'Left-Caudate': 11,
                        'Left-Putamen': 12,
                        'Left-Pallidum': 13,
                        'Left-3rd-Ventricle': 14,
                        'Left-4th-Ventricle': 15,
                        'Left-Brain-Stem': 16,
                        'Left-Hippocampus': 17,
                        'Left-Amygdala': 18,
                        'Left-CSF': 24,
                        'Left-Accumbens-area': 26,
                        'Left-VentralDC': 28,
                        'Left-choroid-plexus': 31,
                        'Right-Lateral-Ventricle': 43,
                        'Right-Inf-Lat-Vent': 44,
                        'Right-Cerebellum-White-Matter': 46,
                        'Right-Cerebellum-Cortex': 47,
                        'Right-Thalamus-Proper': 49,
                        'Right-Caudate': 50,
                        'Right-Putamen': 51,
                        'Right-Pallidum': 52,
                        'Right-Hippocampus': 53,
                        'Right-Amygdala': 54,
                        'Right-Accumbens-area': 58,
                        'Right-VentralDC': 60,
                        'Right-choroid-plexus': 63,
                        'Right-3rd-Ventricle': 14,
                        'Right-4th-Ventricle': 15,
                        'Right-Brain-Stem': 16,
                        'Right-CSF': 24,
                        'ctx-lh-caudalanteriorcingulate': 1002,
                        'ctx-lh-caudalmiddlefrontal': 1003,
                        'ctx-lh-cuneus': 1005,
                        'ctx-lh-entorhinal': 1006,
                        'ctx-lh-fusiform': 1007,
                        'ctx-lh-inferiorparietal': 1008,
                        'ctx-lh-inferiortemporal': 1009,
                        'ctx-lh-isthmuscingulate': 1010,
                        'ctx-lh-lateraloccipital': 1011,
                        'ctx-lh-lateralorbitofrontal': 1012,
                        'ctx-lh-lingual': 1013,
                        'ctx-lh-medialorbitofrontal': 1014,
                        'ctx-lh-middletemporal': 1015,
                        'ctx-lh-parahippocampal': 1016,
                        'ctx-lh-paracentral': 1017,
                        'ctx-lh-parsopercularis': 1018,
                        'ctx-lh-parsorbitalis': 1019,
                        'ctx-lh-parstriangularis': 1020,
                        'ctx-lh-pericalcarine': 1021,
                        'ctx-lh-postcentral': 1022,
                        'ctx-lh-posteriorcingulate': 1023,
                        'ctx-lh-precentral': 1024,
                        'ctx-lh-precuneus': 1025,
                        'ctx-lh-rostralanteriorcingulate': 1026,
                        'ctx-lh-rostralmiddlefrontal': 1027,
                        'ctx-lh-superiorfrontal': 1028,
                        'ctx-lh-superiorparietal': 1029,
                        'ctx-lh-superiortemporal': 1030,
                        'ctx-lh-supramarginal': 1031,
                        'ctx-lh-transversetemporal': 1034,
                        'ctx-lh-insula': 1035,
                        'ctx-rh-caudalanteriorcingulate': 2002,
                        'ctx-rh-caudalmiddlefrontal': 2003,
                        'ctx-rh-cuneus': 2005,
                        'ctx-rh-entorhinal': 2006,
                        'ctx-rh-fusiform': 2007,
                        'ctx-rh-inferiorparietal': 2008,
                        'ctx-rh-inferiortemporal': 2009,
                        'ctx-rh-isthmuscingulate': 2010,
                        'ctx-rh-lateraloccipital': 2011,
                        'ctx-rh-lateralorbitofrontal': 2012,
                        'ctx-rh-lingual': 2013,
                        'ctx-rh-medialorbitofrontal': 2014,
                        'ctx-rh-middletemporal': 2015,
                        'ctx-rh-parahippocampal': 2016,
                        'ctx-rh-paracentral': 2017,
                        'ctx-rh-parsopercularis': 2018,
                        'ctx-rh-parsorbitalis': 2019,
                        'ctx-rh-parstriangularis': 2020,
                        'ctx-rh-pericalcarine': 2021,
                        'ctx-rh-postcentral': 2022,
                        'ctx-rh-posteriorcingulate': 2023,
                        'ctx-rh-precentral': 2024,
                        'ctx-rh-precuneus': 2025,
                        'ctx-rh-rostralanteriorcingulate': 2026,
                        'ctx-rh-rostralmiddlefrontal': 2027,
                        'ctx-rh-superiorfrontal': 2028,
                        'ctx-rh-superiorparietal': 2029,
                        'ctx-rh-superiortemporal': 2030,
                        'ctx-rh-supramarginal': 2031,
                        'ctx-rh-transversetemporal': 2034,
                        'ctx-rh-insula': 2035}

label = label_lookup.values()
label_name = label_lookup.keys()
print(label)
# check orientation of the 3D CT
x, y, z = nib.aff2axcodes(img.affine)
print('\nImage orientation:', x, y, z)

voxel_spacing = img.affine[:3, :3]
image_origin = img.affine[:3, 3]

"""
su = np.sum(img.get_fdata() == 0)

su1 = np.sum(img.get_fdata() == 4)

su2 = np.sum(img.get_fdata() == 43)

print("0 --> "+str(su))

print("4 --> "+str(su1))

print("43 --> "+str(su2))
"""
"""
summ = 0

for i in label:
    s = np.sum(img.get_fdata() == i)
    summ = summ+s
    
    print("Label-"+str(i)+"count is "+str(s))

print("Total volume is",summ/(256*256*256))
"""


voxvol = voxel_spacing[0]+voxel_spacing[1]+voxel_spacing[2]

voxvol1 = voxvol[0]*voxvol[1]*voxvol[2]

print(voxvol1)



print('\nVoxel spacing:\n', voxel_spacing)

print('\nImage origin:\n', image_origin)

starting_physical_point = voxel_spacing.dot([0, 0, 0]) + image_origin
print('\nstarting_physical_point:', starting_physical_point)

ending_physical_point = voxel_spacing.dot([511, 511, 104]) + image_origin
print('\nending_physical_point:', ending_physical_point)


"""
#image = sitk.ReadImage(nif)
# img is a SimpleITK image
stats.Execute(image)

# get the number of voxels with label 1
nvoxels = stats.GetSum()


spacing = image.GetSpacing()
print(spacing)

#print(spacing)
voxvol = spacing[0]*spacing[1]*spacing[2]

print(voxvol)

volume = nvoxels * voxvol/1000

totvol = (256*256*256) *voxvol
#print(img.GetSize())
#print(nif.shape)
#print(totvol)
print("Volume of the Segmentation is "+str(volume))

#print((volume/totvol)*100)

ind = sitk.GetArrayFromImage(image)
#print(ind.size)#- np.count_nonzero(ind)
"""