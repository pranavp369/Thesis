# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 22:49:29 2023

@author: prana
"""

import nibabel as nib

sout = "Outputsegmentation"

data = nib.load(r"C:\Users\prana\OneDrive\Desktop\Thesisvenv\fastsurfer_output\Tutorial\mri\aparc.DKTatlas+aseg.deep.mgz")

img_nifti = nib.Nifti1Image(data.get_fdata(), data.affine, header=nib.Nifti1Header())

nib.nifti1.save(img_nifti, r'C:\Users\prana\OneDrive\Desktop\Thesisvenv\fastsurfer_output\Tutorial\mri\ '+ sout+'.nii.gz')