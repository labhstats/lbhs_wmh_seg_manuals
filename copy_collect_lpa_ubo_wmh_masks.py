#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 16:41:38 2018

@author: lars
"""

def copy_collect_lpa_ubo_wmh_masks(lpa_dir,ubo_dir,collective_dir):
    #It should get IDs from "lpa_dir" which contains BIDS structure..!
    
    print "LPA directory: ",lpa_dir, " UBO directory: " ,ubo_dir, " Output/collective directory: " ,collective_dir
    
    import shutil
    import os
    
    id_list_dir = os.listdir(lpa_dir)
    
    n = len(id_list_dir)
    n_i = 1
    
    for i in id_list_dir:
        print "="*12
        print "Copying masks of ID: ", i, " Number: ", n_i, " of ", n
        
        
        
        ##Force typeset
        
        #LPA
        print "--- LPA ---"
        #lpa_last_part_path = "/ples_lpa_mt2_flair_3d.nii" #For testing...
        lpa_last_part_path = "/T2_FLAIR_3D/ples_lpa_mt2_flair_3d.nii"
        
        full_lpa_path = lpa_dir + i + lpa_last_part_path
        
        new_lpa_target_name = i + "_ples_lpa_mt2_flair_3d.nii"
        
        full_collective_lpa_path = collective_dir + i + "/" + new_lpa_target_name
        
        ensure_dir_path = collective_dir + i + "/"
        if not os.path.exists(ensure_dir_path):
            print "Making directory: ", ensure_dir_path
            os.makedirs(ensure_dir_path)
            
        
        print "From: ", full_lpa_path
        print "To: ", full_collective_lpa_path
        shutil.copyfile(full_lpa_path,full_collective_lpa_path)
        print("Copied LPA mask...")
        
        #T2 FLAIR image also...
        print "--- T2FLAIR ---"
        
        #t2_name = "/t2_flair_3d.nii" #For testing.
        t2_name = "/T2_FLAIR_3D/t2_flair_3d.nii.gz"
        t2_name_target = "/t2_flair_3d.nii.gz"
        
        full_t2_path = lpa_dir + i + t2_name
        
        full_collective_t2_path = collective_dir + i + t2_name_target
        
        print "From: ", full_t2_path
        print "To: ", full_collective_t2_path
        shutil.copyfile(full_t2_path,full_collective_t2_path)
        print("Copied T2 FLAIR image...")
        
        #UBO
        print "--- UBO ---"
        ubo_intermediate_part_path = "/mri/extractedWMH/"
        dynamic_flairspace_map_name = i + "_WMH_FLAIRspace.nii.gz"
        
        full_ubo_path = ubo_dir + i + ubo_intermediate_part_path + dynamic_flairspace_map_name
        
        new_ubo_target_name = dynamic_flairspace_map_name
        
        full_collective_ubo_path = collective_dir + i + "/" + new_ubo_target_name
        
        print "From: ", full_ubo_path
        print "To: " , full_collective_ubo_path
        shutil.copyfile(full_ubo_path,full_collective_ubo_path)
        print("Copied UBO mask...")
        
        #Increment
        n_i = n_i + 1
        print("ID copied...")
        print "="*12
        #End ID loop

    
    print("Finished...")
    #End function...


##Actual call...
base_LPA_30_directory = "/home/lars/Desktop/wmh_thirty_cases_article/LPA/" #The IDs here should be readily found by listdir.
base_UBO_directory = "/home/lars/Desktop/wmh_thirty_cases_article/UBO_CNS/subjects/"

base_dir_collected_cases = "/home/lars/Desktop/wmh_thirty_cases_article/collected_cases/"

copy_collect_lpa_ubo_wmh_masks(base_LPA_30_directory,
                               base_UBO_directory,
                               base_dir_collected_cases)

##Test call... Worked...
#lpa_test_dir = "/home/lars/Desktop/testing_dicomsort/lpa_4_real_cases/"
#ubo_test_dir = "/home/lars/Desktop/testing_dicomsort/ubo_4_real_cases_standard/subjects/"
#collective_test_dir = "/home/lars/Desktop/testing_dicomsort/test_collective_directory/"

#copy_collect_lpa_ubo_wmh_masks(lpa_test_dir,
#                               ubo_test_dir,
#                               collective_test_dir)

