
function y_status = dice_jaccard_coef(manual_dir,automatic_dir)
    %%
    %Initialize inputs.
    y_status = 0; %#ok<NASGU>
    
    manual_path_base = manual_dir; %For actual run.
    %manual_path_base = '/home/lars/Desktop/wmh_thirty_cases_article/Manual_ver_corrected/roi_native/'; %For testing only.
    roi_fixed_suffix = '_roi.nii.gz';
    
    automatic_path_base = automatic_dir; %For actual run.
    %automatic_path_base = '/home/lars/Desktop/wmh_thirty_cases_article/MeVisLab_corrected/collected_cases/*/t2_flair_3d.nii.gz'; %For testing only.
    
    all_files = dir(automatic_path_base);
    
    n_files = length(all_files);
    
    disp(n_files);
    %%
    %Fixed path names - easily changed, extended or removed.
    image_LPA_path      = 'LPA_wmh_map.nii.gz';
    image_UBO_path      = 'UBO_wmh_map_fix.nii.gz';  
    image_UBOorLPA_path = 'OR_UBO_LPA_wmh_map.nii.gz';
    
    %%
    %Arrays for storing results... (Remember to check for equal length.)
    %Only initialized for ";"/vertical appending with header information.
    LPA_matrix      = [1 2 3 4 5 6 7]; %'ID' 'Dice' 'Jaccard' 'AVD' 'Volume diff' 'Volume rel' 'Manual volume'
    UBO_matrix      = [1 2 3 4 5 6 7]; %'ID' 'Dice' 'Jaccard' 'AVD' 'Volume diff' 'Volume rel' 'Manual volume'
    UBOorLPA_matrix = [1 2 3 4 5 6 7]; %'ID' 'Dice' 'Jaccard' 'AVD' 'Volume diff' 'Volume rel' 'Manual volume'
    
    %%
    %For loop start.
    
    for i = 1:n_files
        disp('------------');
        %%
        %Extract current ID.
        split_id_string = split(all_files(i).folder,"/");
        cell_id_string = split_id_string(end,1);
        current_ID_string = cell_id_string{1}; %To be paired or "fullfiled" with manual_dir.
        disp(['The current ID is: ' current_ID_string]);
        disp(['Number: ' string(i) ' of ' string(n_files)]);
        
        %%
        %Load and ready "image_i".
        current_image_i_path = fullfile(manual_path_base,[current_ID_string roi_fixed_suffix]);
        image_i = niftiread(current_image_i_path);
        whos image_i
        
        disp(['Manual trace is read from: ' current_image_i_path]);
        
        image_i = imbinarize(image_i);
        whos image_i
        %%
        %Readying reference maps that have been handled in MeVisLab.
        LPA_path_i          = string(fullfile(all_files(i).folder,image_LPA_path));
        UBO_path_i          = string(fullfile(all_files(i).folder,image_UBO_path)); 
        UBOorLPA_path_i     = string(fullfile(all_files(i).folder,image_UBOorLPA_path)); 
        
        disp(['LPA wmh mask is read from: ' LPA_path_i]);
        disp(['UBO wmh mask is read from: ' UBO_path_i]);
        disp(['Union of LPA/UBO wmh mask is read from: ' UBOorLPA_path_i]);
        
        image_LPA_i         = niftiread(LPA_path_i);
        whos image_LPA_i
        image_UBO_i         = niftiread(UBO_path_i);
        whos image_UBO_i
        image_UBOorLPA_i    = niftiread(UBOorLPA_path_i);
        whos image_UBOorLPA_i
        
        image_LPA_i         = imbinarize(image_LPA_i);
        whos image_LPA_i
        image_UBO_i         = imbinarize(image_UBO_i);
        whos image_UBO_i
        image_UBOorLPA_i    = imbinarize(image_UBOorLPA_i);
        whos image_UBOorLPA_i
        %%
        %Calculate statistics - Dice and Jaccard first and foremost.
        d_LPA_i             = dice(image_i,image_LPA_i);
        j_LPA_i             = jaccard(image_i,image_LPA_i);
        
        d_UBO_i             = dice(image_i,image_UBO_i);
        j_UBO_i             = jaccard(image_i,image_UBO_i);
        
        d_UBOorLPA_i        = dice(image_i,image_UBOorLPA_i);
        j_UBOorLPA_i        = jaccard(image_i,image_UBOorLPA_i);
        
        %%
        %Other statistics
        
        %AVD --- volume estimates and relative differences to manual traced images.
        volume_LPA_i        = sum(sum(sum(image_LPA_i)));
        volume_UBO_i        = sum(sum(sum(image_UBO_i)));
        volume_UBOorLPA_i   = sum(sum(sum(image_UBOorLPA_i)));
        
        volume_image_i      = sum(sum(sum(image_i)));
        
        AVD_LPA_i           = getAVD(volume_image_i,volume_LPA_i);
        AVD_UBO_i           = getAVD(volume_image_i,volume_UBO_i);
        AVD_UBOorLPA_i      = getAVD(volume_image_i,volume_UBOorLPA_i);
        
        %Volume difference (not absolute).
        volume_diff_LPA_i = volume_LPA_i - volume_image_i;
        volume_diff_UBO_i = volume_UBO_i - volume_image_i;
        volume_diff_UBOorLPA_i = volume_UBOorLPA_i - volume_image_i;
        
        %Volume relative difference.
        volume_relative_LPA_i = volume_LPA_i/volume_image_i;
        volume_relative_UBO_i = volume_UBO_i/volume_image_i;
        volume_relative_UBOorLPA_i = volume_UBOorLPA_i/volume_image_i;
        
        %%
        %Collecting and appending to matrice (for later csv.)
        LPA_array_i         = [str2double(current_ID_string) d_LPA_i j_LPA_i AVD_LPA_i volume_diff_LPA_i volume_relative_LPA_i volume_image_i];
        UBO_array_i         = [str2double(current_ID_string) d_UBO_i j_UBO_i AVD_UBO_i volume_diff_UBO_i volume_relative_LPA_i volume_image_i];
        UBOorLPA_array_i    = [str2double(current_ID_string) d_UBOorLPA_i j_UBOorLPA_i AVD_UBOorLPA_i volume_diff_UBOorLPA_i volume_relative_LPA_i volume_image_i];
        
        LPA_matrix = [LPA_matrix; LPA_array_i]; %#ok<AGROW>
        UBO_matrix = [UBO_matrix; UBO_array_i]; %#ok<AGROW>
        UBOorLPA_matrix = [UBOorLPA_matrix; UBOorLPA_array_i]; %#ok<AGROW>
        
        disp('Finished with this individual...');
        disp('------------');
    end  
    disp('Finished with all individuals');
    
    %%
    %Saving and returning csv?
    
    filename_LPA_csv        = 'LPA_30_comparisons.csv';
    filename_UBO_csv        = 'UBO_30_comparisons.csv';
    filename_UBOorLPA_csv   = 'UBOorLPA_30_comparisons.csv';
    
    disp(['Look for filename: ' filename_LPA_csv ' in "Current folder".']);
    disp(['Look for filename: ' filename_UBO_csv ' in "Current folder".']);
    disp(['Look for filename: ' filename_UBOorLPA_csv ' in "Current folder".']);
    
    dlmwrite(filename_LPA_csv,LPA_matrix,'delimiter',',','precision',8);
    dlmwrite(filename_UBO_csv,UBO_matrix,'delimiter',',','precision',8);
    dlmwrite(filename_UBOorLPA_csv,UBOorLPA_matrix,'delimiter',',','precision',8);
    
    disp('All csvs are written!');
    %Finished ok is True.
    y_status = 1;
end


