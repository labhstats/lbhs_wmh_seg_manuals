
function y_status = myGunzip_pre_LPA(glob_path_input)
    %Gunzip using MatLab's interface for decompressing ".gz" files.
    %Intention is to have a zip function that do not mess around at system
    %level. https://se.mathworks.com/help/matlab/ref/gunzip.html It does
    %not apparently remove the uncompressed file.
    
    %glob_path =
    %'/home/lars/Desktop/testing_dicomsort/gunzip_test/*/T2_FLAIR_3D/*.gz';
    %<<Static>> test path.
    
    %Re-use:
    glob_path = glob_path_input; %Dynamic path.
    
    files = dir(glob_path);

    n_files = length(files); 

    files_fixed_paths = string(zeros(n_files,1)); %Creating string array.
    for i = 1:n_files
        disp(i);
        files_fixed_paths(i) = string(fullfile(files(i).folder,files(i).name)); %Ensuring string array.
    end
    
    disp(files_fixed_paths);
    %Re-use end:
    
    %Unzipping:
    gunzip(files_fixed_paths);
    
    %Run reached end without too many problems.
    y_status = 1;
end