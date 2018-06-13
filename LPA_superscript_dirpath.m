
function y_status = LPA_superscript_dirpath(glob_path_input)
    %The unsupervised LPA streamlined batch system: 
    %Purposefully created to avoid using the GUI for large sets of data.
    %REQUIRE:
    % - SPM12
    % - LST 2.0.15
    
    %glob_path = '/home/lars/Desktop/testing_dicomsort/new_lpa_nifti_test/*/T2_FLAIR_3D/t2_flair_3d.nii';
    glob_path = glob_path_input;
    
    files = dir(glob_path); %Requires char...
    
    n_files = length(files); %We expect over 1800 subjects.
    
    files_fixed_paths = string(zeros(n_files,1)); %Enforcing string for functionality...
    for i = 1:n_files
        disp(i);
        files_fixed_paths(i) = string(fullfile(files(i).folder,files(i).name)); %Further enforcing string for functionality...
    end
    
    disp(files_fixed_paths)
    
    %Remember to change each "files_fixed_paths(i)" back to char with "char()",
    % as LPA requires it for inputs.
    
    spm('defaults','fmri');
    for j = 1:n_files
       disp(j); 
       
       image_path_j_char = join([char(files_fixed_paths(j)),',1'],''); %This is the fix that LPA requires.
       
       matlabbatch{1}.spm.tools.LST.lpa.data_F2 = {image_path_j_char};
       matlabbatch{1}.spm.tools.LST.lpa.data_coreg = {''};
       matlabbatch{1}.spm.tools.LST.lpa.html_report = 0;
       
       spm_jobman('run', matlabbatch);
    end
    
    %Run reached end without too many problems.
    y_status = 1;
end


