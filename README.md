# lbhs_wmh_seg_manuals
Extra details of segmentation algorithms that are attempted to use. Specific detail will be given to problems and special care "required" for them to work satisfactory. This git is in no way trying to critize the algorithms or their creators, but instead to provide a subjective adaption such that it fits the intended project's (at http://www.medical-imaging.no/) needs.

Check the wiki for details: https://github.com/labhracorgi/lbhs_wmh_seg_manuals/wiki

General scripts will either be referenced or provided.

This repository has no guarantee of efficient code, only code that has been run and works sufficiently.

## "Possible" candidates currently in consideration:
- ~~https://github.com/NIC-VICOROB/SLSToolBox~~ (Seem to require a lot of manual pre processing by the user compared to LPA and UBO; whether this is a valid arguement may not be the case)
- ~~https://github.com/Kamnitsask/deepmedic~~ (A lot of bugs and issues for unknown reasons.)
- ~~W2MH algorithm at https://www.nitrc.org/projects/w2mhs~~ (SPM12/MatLab and SVM RF based.) May be worth looking further into.
- ~~Winner of MICCAI 2017 WMH segmentation https://github.com/hongweilibran/wmh_ibbmTum (Competition description http://wmh.isi.uu.nl/wp-content/uploads/2017/09/sysu_media.pdf and arxiv article https://arxiv.org/pdf/1802.05203.pdf)~~ Do not seem to have nearly enough documentation for a beginner to apply.

## Successful test runs of:
- LPA (in LST 2.0.15)
- UBO Detector

## Ready for full scale project runs:
- LPA (in LST 2.0.15)

## File descriptions: (LPA)
1. **LPA_superscript_dirpath.m**: Provided a 'glob/dir' path to T2 FLAIR NIFTI images, Python/MatLab respective functionality, this script will run LPA sequentially for every image.
2. **binary_lesion_maps_post_LPA.m**: Provided a 'glob/dir' path to probability lesion maps (from LPA algorithm), Python/MatLab respective functionality, this script will create binary lesion maps with respect to some threshold specified by the user. (If the fix is not utilized then the threshold is "defaulted" to 0.5.)
3. **extract_vol_noc_nogui_post_LPA.m**: Provided a 'glob/dir' path to probability lesion maps (from LPA algorithm), Python/MatLab respective functionality, this script will calculate total lesion volume (TLV) and number of clusters (NoC/N).
4. Pigz implementation (Parallel Gunzip https://github.com/madler/pigz) through MatLab's cmd call: https://github.com/torgil01/HUNT/blob/master/Matlab/private/myGunzip.m or Gunzip through MatLab's own interface in **myGunzip_pre_LPA.m**.
5. "Correction/fixes" of scripts in algorithm? To allow user specified threshold when using the job interface in MatLab/SPM12 with **binary_lesion_maps_post_LPA.m**. Caution advised.

## File descriptions: (UBO)
1. Script for creating specified UBO directory, BIDS are initially assumed: https://github.com/labhracorgi/mri_sort_filter_convert/blob/master/other/ubo_cns_copyfier_workspace.py
2. "Correction/fixes" of scripts in algorithm? To hinder QC web viewers from popping up for thousands of individuals and thus potentially not exceeding available RAM during the calculation period.
3. **Settings and new Dartel atlas for 40+ population? Or simply use standard/preset ones?**

## Primarily systems tested on:
- Debain 9 (Linux), Nvidia K420, Xeon 6 Core 3.60Ghz.


## Software tested on:
- Again, check the wiki for test run details https://github.com/labhracorgi/lbhs_wmh_seg_manuals/wiki
