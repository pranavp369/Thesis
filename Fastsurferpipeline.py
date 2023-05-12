# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 22:56:55 2023

@author: prana
"""

#Import Section
import sys
import argparse
from pathlib import Path
import os
import subprocess
import nibabel as nib
import re
import numpy as np
import SimpleITK as sitk
import pandas as pd





#Command Line Input
"""
This section takes in the input from the command line (Either Single file or a 
directory) and sends it to the next module as input. 
"""

class FastSurferPipeline:
    
    #__init__ function : Initializing variables
    def __init__(self):
        self.t1_path = ""
        self.dir_path = ""
        self.label_list = [0]
        self.labels_lookup = {
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
        
        self.df = pd.DataFrame(columns = self.labels_lookup.keys())
        
        
    
    #Parse Function: a method to get the command line arguments and call the pipeline function
    def parse_arguments(self):
        
        #Get the current working directory
        self.directory_int = os.getcwd()
        self.directory = os.path.join(self.directory_int,'FastSurfer')
        #print(self.directory)
        
        
        sys.path.append(self.directory)


        
        parser = argparse.ArgumentParser(description = "FastSurfer Pipeline")
        
        #Parse Argument for single T1 Image
        parser.add_argument("--t1",metavar="T1_IMAGE",help="The T1 weighted volume for the FastSurfer Pipeline ")
        
        #Parse Argument for for a directory of T1 Images
        parser.add_argument("--d",metavar="DIR_PATH",help="The T1 weighted volume directory for the FastSurfer Pipeline ")
        
        #Parser Argument for the list of labels to be segmented
        parser.add_argument("--l",metavar="LABEL_LIST",help="A List of Labels to be segmented")
        
        parser.add_argument("--all",help = "All possible labels are segmented",action = 'store_true')
        
        args = parser.parse_args()
        
        
        #Conditional Statement to call the pipeline for a sigular image 
        if args.t1 is not None and args.d is None:
            self.t1_path = args.t1
            
            if args.l is not None and args.all is None:
                self.label_red = re.findall(r'\d+',args.l)
                self.label_list_temp = []
                
                for i in self.label_red:
                    self.label_list_temp.append(int(i))
                
                self.label_list = self.label_list_temp
            
            if args.all is not None and args.l is None:
                
                self.label_list = self.labels_lookup.values()
                #print(self.label_list)
            
            
            
            
                
            self.start_pipeline_single(self.t1_path,self.label_list)
            
            
        #Conditional Statement to call the pipeline for a directory of images
        if args.t1 is None and args.d is not None:
            self.dir_path = args.d
            if args.l is not None and args.all is None:
                self.label_red = re.findall(r'\d+',args.l)
                self.label_list_temp = []
                
                for i in self.label_red:
                    self.label_list_temp.append(int(i))
                
                self.label_list = self.label_list_temp
            
            if args.all is not None and args.l is None:
                self.label_list = self.labels_lookup.values()
                
            
            self.start_pipeline_directory(self.dir_path,self.label_list)
            
            
                
            
            
        #No input argument error    
        if args.t1 is None and args.d is None:
            print("ERROR: No Input Arguments Given")
            print("A T1 weighted image or a directory of t1 weighted images must be provided as input")
            
        
        #Two different input commands given
        if args.t1 is not None and args.d is not None:
            print("ERROR: Two Different Types of Input Given")
            print("A T1 weighted image and a directory is given. Only one option should be given as input")
        
    
    #Run_Pipeline_Single Function: A method that calls the fastsurfer module for a single image 
    def start_pipeline_single(self,t1_path,label_list):
        
        self.t1_path = t1_path
        self.labels = label_list
        
        #Splitting the input path into head and tail
        self.path_split = os.path.split(self.t1_path)
        self.t1_head = self.path_split[0]
        self.t1_name = self.path_split[1]
        
        #Setting up a path for the output volume
        self.output_tail = "Output_"+ self.t1_name[:-4]
        self.output_path = os.path.join(self.t1_head,self.output_tail)
        
        #Set up sid for the subprocess
        self.sid = "single"
        
        #Setting up the output directory
        os.mkdir(self.output_path)
        
        #print("Check 1")
        
        #The subprocess to call the Fastsurfer Prediction module
        subprocess.call(['python', r'FastSurfer/FastSurferCNN/run_prediction.py','--t1',self.t1_path,'--sid',self.sid,'--sd',self.output_path])
        
        #Call the Next Module to Convert output file to Nifti
        self.combined_path = os.path.join(self.output_path,self.sid)
        self.convert_MGZ_to_NIFTI(self.combined_path,self.labels)
        #print("12345")
        #print(self.nifti_path)
        #print("98765s")
        self.vol_dict = self.compute_volume(self.t1_name,self.nifti_path,self.labels)
        
        #Dictionary to DataFrame
        #self.df = self.df.append(self.vol_dict,ignore_index=True)
        
        #print(self.vol_dict)
        return self.vol_dict
        
        #print(self.df)
        
        #print("The volume has been generated")
        #print(self.output_path)
        #print(self.t1_name)
        
    
    #Run_Pipeline_Directory Function: A method that calls the fastsurfer module for an image directory
    def start_pipeline_directory(self,dir_path,label_list):
        
        self.directory_int = os.getcwd()
        self.dir = dir_path
        self.directory = os.path.join(self.directory_int,self.dir)
        #print("Please Help")
        
        #print(dir_path)
        self.labels = label_list
        
        for i in os.listdir(self.directory):
            self.t1 = os.path.join(self.directory,i)
            self.v = self.start_pipeline_single(self.t1,self.labels)
            
            self.df = self.df.append(self.v,ignore_index=True)
        
        
        print("[CONVERT TO CSV]: Convert the data to CSV")
        
        self.df.to_csv("500_600.csv",index=False)
        #print(self.df)
        
        #print(self.df)
            
        """
            #Splitting the input path into head and tail
            self.path_split = os.path.split(self.t1_path)
            self.t1_head = self.path_split[0]
            self.t1_name = self.path_split[1]
        
            #Setting up a path for the output volume
            self.output_tail = "Output_"+ self.t1_name[:-4]
            self.output_path = os.path.join(self.t1_head,self.output_tail)
            #print(i)
            
            #self.vol_dict = self.compute_volume(self.output_path,self.labels)
            """
            
            
            
            
    
    
    #convert_MGZ_to_NIFTI Function: A method that convert the output MGZ volume to a NIFTI volume
    def convert_MGZ_to_NIFTI(self,combined_path,label_list):
        
        print("[CONVERSION MODULE] : Converting mgz volume to a nifti segmentation volume")
        
        self.combined_path = combined_path
        self.labels = label_list
        
        self.mgz_int_path = os.path.join(self.combined_path,"mri")
        self.mgz_path = os.path.join(self.mgz_int_path,"aparc.DKTatlas+aseg.deep.mgz")
        
        self.mgz_data = nib.load(self.mgz_path)
        
        self.nifti_segmentation = nib.Nifti1Image(self.mgz_data.get_fdata(), self.mgz_data.affine, header=nib.Nifti1Header())
        
        self.nifti_path = os.path.join(self.combined_path,'complete_segmentation.nii.gz')
        nib.nifti1.save(self.nifti_segmentation, self.nifti_path)
        
        
        """
        if self.labels == [0]:
            print("The NIFTI segmentation has been saved")
        
        else:
            self.label_segmentation(self.nifti_path,self.label_list)
        """
            
    def label_segmentation(self, nifti_path, label_list):
        
        print("[LABEL SEGMENTATION MODULE] : Segmentation of T1 Image into selected Labels")
        self.nifti_path = nifti_path
        self.labels = label_list
        
        self.path_split = os.path.split(self.nifti_path)
        self.nifti_head = self.path_split[0]
        print(self.nifti_head)
        
        self.label_output = os.path.join(self.nifti_head,'LabelSegmentation')
        os.mkdir(self.label_output)
        
        
        
        for i in self.labels:
            self.seg_label = [i]
            
            self.nifti_load = nib.load(self.nifti_path).get_fdata()
            self.label_find = np.in1d(self.nifti_load, self.seg_label).reshape(self.nifti_load.shape)
            self.roi = np.where(self.label_find, 1, 0)
            
            
            self.new_image = nib.Nifti1Image(self.roi, affine=np.eye(4))
            
            for n in self.labels_lookup:
                if self.labels_lookup[n] == self.seg_label[0]:
                    self.label_name = n
            
            
            self.compute_volume(self.nifti_path,self.label_name)
            
            self.label_seg_path = os.path.join(self.label_output, self.label_name)
            
            #nib.save(self.new_image, self.label_seg_path)
            
            
    
    def compute_volume(self,name,nif_path,label_list):
        
        self.nif_img = nib.load(nif_path)
        self.name = name

        print("[VOLUME MODULE]: Computing Volume of the segmentation")
        #print(nif_path)
        self.split_path = os.path.split(nif_path)
        self.inter = self.split_path[0]
        
        self.total_vol_path_int = os.path.join(self.inter,"mri")
        self.total_vol_path = os.path.join(self.total_vol_path_int,"mask.mgz")
        
        self.mask_img = nib.load(self.total_vol_path)
        self.mask_sum = np.sum(self.mask_img.get_fdata())
        
        self.label = label_list
        
        self.label_dict = {}
        
        self.label_val = list(self.labels_lookup.values())
        self.label_key = list(self.labels_lookup.keys())
        
        self.total_vol = 0
        #print(self.label)
        
        self.label_dict.update({"CaseName":self.name})
        
        for i in self.label:
            self.num_vox = np.sum(self.nif_img.get_fdata() == i)
            
            self.pos = self.label_val.index(i)
            self.lbl = self.label_key[self.pos]
            
            self.voxel_spacing = self.nif_img.affine[:3, :3]
            
            self.voxvol_int = self.voxel_spacing[0]+self.voxel_spacing[1]+self.voxel_spacing[2]

            self.voxvol = self.voxvol_int[0]*self.voxvol_int[1]*self.voxvol_int[2]
            
            self.volume = self.num_vox *self.voxvol/1000
            
            self.label_dict.update({self.lbl:self.volume})
            
        
        #Total Intercranial Volume
        self.mask_voxel_spacing = self.mask_img.affine[:3, :3]
            
        self.mask_voxvol_int = self.mask_voxel_spacing[0]+self.mask_voxel_spacing[1]+self.mask_voxel_spacing[2]

        self.maskvoxvol = self.mask_voxvol_int[0]*self.mask_voxvol_int[1]*self.mask_voxvol_int[2]
        
        self.total_vol = self.mask_sum*self.maskvoxvol/1000
            
            
            
        self.label_dict.update({"InterCranial Volume":self.total_vol})
            
        return self.label_dict
        
        #print( self.label_dict)
        
        #print(self.label_val)
        
        
        
        
        
        
        
        
            
            


if __name__ == '__main__':
    
    sys.path.insert(1, r'C:\Users\prana\OneDrive\Desktop\Thesisvenv\FastSurfer')
    FastSurferPipeline().parse_arguments()