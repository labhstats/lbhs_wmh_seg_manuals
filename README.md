# lbhs_wmh_seg_manuals
Extra details of segmentation algorithms that are attempted to use. Specific detail will be given to problems and special care "required" for them to work satisfactory.

Check the wiki for details: https://github.com/labhracorgi/lbhs_wmh_seg_manuals/wiki

General scripts will either be referenced or provided.

This repository has no guarantee of efficient code, only code that has been run and works sufficiently.

## Successful runs of:
- LPA (in LST 2.0.15)
- UBO Detector

## File descriptions: (LPA)
1. **LPA_superscript_dirpath.m**: Provided a 'glob/dir' path to T2 FLAIR NIFTI images, Python/MatLab respective functionality, this script will run LPA sequentially for every image.
2. **Script for creating binary lesion map**
3. **Script for calculating wmh volume from lesion map**
4. Pigz implementation (Parallel Gunzip https://github.com/madler/pigz) through MatLab's cmd call: https://github.com/torgil01/HUNT/blob/master/Matlab/private/myGunzip.m or Gunzip through MatLab's own interface in "myGunzip_pre_LPA.m".

## File descriptions: (UBO)
1. **Script that suppresses QC?**
2. 

## Primarily systems tested on:
- Debain 9 (Linux), Nvidia K420, Xeon 6 Core 3.60Ghz.


## Software tested on:
- Again, check the wiki for test run details https://github.com/labhracorgi/lbhs_wmh_seg_manuals/wiki
