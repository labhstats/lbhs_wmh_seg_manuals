# lbhs_wmh_seg_manuals
Extra details of segmentation algorithms that are attempted to use. Specific detail will be given to problems and special care "required" for them to work satisfactory. This git is in no way trying to critize the algorithms or their creators, but instead to provide a subjective adaption such that it fits the intended project's (at http://www.medical-imaging.no/) needs.

Check the wiki for details: https://github.com/labhstats/lbhs_wmh_seg_manuals/wiki

General scripts will either be referenced or provided.

This repository has no guarantee of efficient code, only code that has been run and works sufficiently.

## "Possible" candidates currently in consideration:
Overlining means that the algorithm(s) in question is no longer considered.
- ~~SLSToolBox:~~ https://github.com/NIC-VICOROB/SLSToolBox (Seem to require a lot of manual pre processing by the user compared to LPA and UBO; whether this is a valid arguement may not be the case.)
- ~~DeepMedic:~~ https://github.com/Kamnitsask/deepmedic (A lot of bugs and issues for unknown reasons.)  Too many "diffuse" errors making implementation impossible to run a test case.
- ~~W2MHS~~ algorithm at: https://www.nitrc.org/projects/w2mhs (SPM12/MatLab and SVM RF based.) May be worth looking further into.
- ~~NiftiNet:~~ https://github.com/NifTK/NiftyNet and https://www.sciencedirect.com/science/article/pii/S0169260717311823 (Provides only abstractions of TensorFlow... and zoo not "wide" enough.)
- ~~DLTK:~~ https://github.com/DLTK/DLTK (Provides only abstractions of TensorFlow... and zoo not "wide" enough.)

## Successful test runs of:
- LPA (in LST 2.0.15);
- UBO Detector;
- Mnist CNN example (TensorFlow/Theano) on CPU.
- wmh_ibbmTum's U-NET that won the MICCAI 2017 WMH segmentation challenge.

## Ready for full scale project runs:
- LPA (in LST 2.0.15);
- UBO Detector (While only using standard options.)
- wmh_ibbmTum's U-NET that won the MICCAI 2017 WMH segmentation challenge.

## File descriptions: (U-Net MICCAI 2017)
1. All original files are present at: https://github.com/hongweilibran/wmh_ibbmTum, although the implementation is too specialized for general use and my own modifications of these files are uploaded for reference. 
2. A functioning modification of the original code is found at "**my_miccai_30_formatting.py**". It is rigourosly commented and maybe even too much, but perhaps also more understandable than the original. Its inputs require a directory where images are stored in some ordering, and a directory where a tranformation matrix correction to native space (.txt) script or file is saved. This (.txt) file  can be run in BaSh given FSL installed (fslmaths); but for some reason not in BaSh via Python, thus this indirect implementation.
3. Another modification named "**my_flair_n4_miccai_30_formatting.py**" is an implementation that is attuned for more pre and post processing of the data. Multiple more files (.txt) allow for instance: Easy WM mask diagnostics [we are not guaranteed that the cropping/padding won't remove any of the WM; rigid body centralization with an atlas could be a possible solution for this issue], show a list of IDs that are finished processing, and further FSL BaSh commands for external calls. A flag that specifies whether you want to continue or redo ("cont" or anything else) the segmentation is also implemented for larger sets of data.
4. Just a more refined segmentation process similar to the previous one, named "**my_miccai_post_wm_30_formatting.py**". Cropping/padding is still poorly handled. (Runs very good with WM masking from FreeSurfer)

![Performance of U-Net](https://github.com/labhstats/lbhs_wmh_seg_manuals/blob/master/dice_ravd_plot_30_cases.png?raw=true)

![Boxplot of DICE U-Net](https://github.com/labhstats/lbhs_wmh_seg_manuals/blob/master/dice_box_unet.png?raw=true)

## File descriptions: (LPA)
1. **LPA_superscript_dirpath.m**: Provided a 'glob/dir' path to T2 FLAIR NIFTI images, Python/MatLab respective functionality, this script will run LPA sequentially for every image.
2. **binary_lesion_maps_post_LPA.m**: Provided a 'glob/dir' path to probability lesion maps (from LPA algorithm), Python/MatLab respective functionality, this script will create binary lesion maps with respect to some threshold specified by the user. (If the fix is not utilized then the threshold is "defaulted" to 0.5.)
3. **extract_vol_noc_nogui_post_LPA.m**: Provided a 'glob/dir' path to probability lesion maps (from LPA algorithm), Python/MatLab respective functionality, this script will calculate total lesion volume (TLV) and number of clusters (NoC/N).
4. Pigz implementation (Parallel Gunzip https://github.com/madler/pigz) through MatLab's cmd call: https://github.com/torgil01/HUNT/blob/master/Matlab/private/myGunzip.m or Gunzip through MatLab's own interface in **myGunzip_pre_LPA.m**.
5. "Correction/fixes" of scripts in algorithm? To allow user specified threshold when using the job interface in MatLab/SPM12 with **binary_lesion_maps_post_LPA.m**. Caution advised.

## File descriptions: (UBO)
1. Script for creating specified UBO directory, BIDS are initially assumed: https://github.com/labhstats/mri_sort_filter_convert/blob/master/other/ubo_cns_copyfier_workspace.py (or https://github.com/labhstats/mri_sort_filter_convert/blob/master/other/ubo_cns_copyfier_workspace_manual_ids.py for manual input of IDs.)
2. "Correction/fixes" of scripts in algorithm? To hinder QC web viewers from popping up for thousands of individuals and thus potentially not exceeding available RAM during the calculation period.
3. **Settings and new Dartel atlas for 40+ population? Or simply use standard/preset ones; implies danger of over- and underfitting algorithm?**
4. **manual_fix_world_matrix.mlab** is a MeVisLab script and a manual way of correcting the world matrices in the flairspace WMH map returned from the UBO Detector.

![LPA and UBO dice values](https://github.com/labhstats/lbhs_wmh_seg_manuals/blob/master/dice_box.png?raw=true)

## General MeVisLab scripts:
1. **automatic_wmh_pipeline_lpa_ubo_w_fix.mlab** is a preliminary script that fixes everything with UBO's world matrix and calculates WMH volume as well. Exact directories and unique file specifiations are necessary to provide for the code to function properly. Is "easily downgraded" or adjusted (e.g. omitt saving certain WMH masks for larger sets of data) to whatever the end user finds to be the most efficient for the corresponding data.

## Primarily specifications of system(s) tested/ran on:
- Debain 9 (Linux), Nvidia K420, Xeon 6 Core 3.60GHz.
- macOS Sierra (Apple), Radeon Pro 555, i7 4 Core 2.8GHz.

## Software tested on:
- Again, check the wiki for test run details https://github.com/labhstats/lbhs_wmh_seg_manuals/wiki.
