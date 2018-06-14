
function extract_vol_noc_nogui_post_LPA(glob_path_input,prob_threshold)
    %Find by dynamic path:
    %glob_path = '/home/lars/Desktop/testing_dicomsort/new_lpa_nifti_test/*/T2_FLAIR_3D/ples_lpa_mt2_flair_3d.nii';
    glob_path = glob_path_input;
    
    files = dir(glob_path);
    
    n_files = length(files);
    
    %Initialise and iterate while correcting and merging:
    files_fixed_paths = string(zeros(n_files,1));
    cell_char_paths = cell(n_files,1);
    for i = 1:n_files
        disp(i);
        files_fixed_paths(i) = join([string(fullfile(files(i).folder,files(i).name)),',1'],'');
        %To merge all paths into one cell array for optimal handling.
        %Cannot get all TLV and NoC in one CSV elseway.
        cell_char_paths{i} = char(files_fixed_paths(i)); 
    end
    
    %Display:
    disp(files_fixed_paths)
    disp(cell_char_paths)
    
    %Initiate and run job:
    spm('defaults','fmri');
    
    matlabbatch{1}.spm.tools.LST.tlv.data_lm = cell_char_paths;
    matlabbatch{1}.spm.tools.LST.tlv.bin_thresh = prob_threshold;
    
    spm_jobman('run', matlabbatch);
end
