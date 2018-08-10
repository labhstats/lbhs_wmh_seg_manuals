function volume_y = getAVD(image_1_vol,image_2_vol)
    %Is this correct?
    %Per: https://github.com/hjkuijf/wmhchallenge/blob/master/evaluation.py
    %%
    %Rename.
    vol_1 = image_1_vol;
    vol_2 = image_2_vol;
    
    %%
    %Calculate.
    nominator = abs(vol_1 - vol_2);
    
    denominator = vol_1;
    
    %%
    %Return.
    volume_y = nominator/denominator;
end