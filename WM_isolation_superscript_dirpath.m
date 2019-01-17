function y_status = WM_isolation_superscript_dirpath(glob_path_input) 
    %Purposefully created to avoid using the GUI for large sets of data.
    %REQUIRE:
    % - SPM12
    
    %Global paths:
    spm_tpm_dir = '/home/lars/Apps/spm12/tpm/TPM.nii'; %User advised to double check.
    
  %%
    glob_path = glob_path_input; %'/home/lars/Desktop/wmh_thirty_cases_article/wm_isolation_test_run/*'
    
    basic_glob_path = glob_path(1:end-1); %Removes wildcard "*" for inputations later.
    
    stat_t1_path = '/T1_3D_SAG/t1_3d_sag.nii'; %User advised to double check.
    stat_t2_path = '/T2_FLAIR_3D/t2_flair_3d.nii'; %User advised to double check.
    mod_stat_t1_path = '/T1_3D_SAG/rt1_3d_sag.nii'; %User advised to double check.
    
    IDs = dir(glob_path); %Requires char...
    
    IDs = IDs(~ismember({IDs.name},{'.','..'})); %Should remove dot directories...
    
    n_files = length(IDs); %We expect over 1800 subjects.
    
    disp(n_files);
    
    %%
    for j = 1:n_files
       disp(j);
       
       current_id_j = IDs(j).name;
       T1_image_path_j_char = [basic_glob_path current_id_j stat_t1_path];
       T2_image_path_j_char = [basic_glob_path current_id_j stat_t2_path];  
       
       disp(T1_image_path_j_char)
       disp(T2_image_path_j_char)
       
       %Feed to sub-functions coregister and then segment (remember that
       %['r' t1path] must be used).
       
       %%
       my_coregister_estimate_reslice(T1_image_path_j_char,T2_image_path_j_char) %Call to coregistration.
       
       mod_T1_image_path_j_char = [basic_glob_path current_id_j mod_stat_t1_path];
       
       %%
       disp(mod_T1_image_path_j_char)
       
       standard_mm_spm_segment(mod_T1_image_path_j_char,T2_image_path_j_char,spm_tpm_dir) %Call to segmentation post coregistration.
       
       %%
       fixed_wm_mask_input_name = [basic_glob_path current_id_j '/T1_3D_SAG/c2rt1_3d_sag.nii']; %Depends on input name of t1 file.
       fixed_wm_mask_output_name = [basic_glob_path current_id_j '/T1_3D_SAG/filled_c2rt1_3d_sag.nii']; %Depends on input name of t1 file.
       
       fsl_maths_bin_fillh_call = ['fslmaths ' fixed_wm_mask_input_name ' -bin -fillh ' fixed_wm_mask_output_name];
       disp(fsl_maths_bin_fillh_call);
       system(fsl_maths_bin_fillh_call);
       
       wm_rt1_output_name = [basic_glob_path current_id_j '/T1_3D_SAG/wm_rt1_3d_sag.nii'];
       fsl_maths_rt1_isolation_call = ['fslmaths ' mod_T1_image_path_j_char ' -mul ' fixed_wm_mask_output_name ' ' wm_rt1_output_name];
       disp(fsl_maths_rt1_isolation_call);
       system(fsl_maths_rt1_isolation_call);
       
       wm_t2_flair_output_name = [basic_glob_path current_id_j '/T2_FLAIR_3D/wm_t2_flair_3d.nii'];
       fsl_maths_t2_isolation_call = ['fslmaths ' T2_image_path_j_char ' -mul ' fixed_wm_mask_output_name ' ' wm_t2_flair_output_name];
       disp(fsl_maths_t2_isolation_call);
       system(fsl_maths_t2_isolation_call);
       
    end
    
    %Run reached end without too many problems.
    y_status = 1;
end