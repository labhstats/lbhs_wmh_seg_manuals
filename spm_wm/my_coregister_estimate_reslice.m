%%My coregister function, used for making sure T1 is matched to
%%intra-subject T2 FLAIR image for WM extraction.

function my_coregister_estimate_reslice(t1path,t2path)

    %REQUIRE:
    % - SPM12

loc_arg1_check = exist(t1path,'file');
loc_arg2_check = exist(t2path,'file');

if(loc_arg1_check && loc_arg2_check)
    disp('Inputs OK')
else
    disp('Inputs do not exist... at COREGISTER')
    exit
end

spm('Defaults','fMRI');
spm_jobman('initcfg');

matlabbatch{1}.spm.spatial.coreg.estwrite.ref = {t2path}; %Stationary image.
matlabbatch{1}.spm.spatial.coreg.estwrite.source = {t1path}; %To be similarized to ref.
matlabbatch{1}.spm.spatial.coreg.estwrite.other = {''}; %Sets of other images which should keep up with source image.
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.interp = 4;
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.mask = 0;
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.prefix = 'r'; %This sets a new prefix for the file which segmentation is to be done at.

spm_jobman('run', matlabbatch);

end
