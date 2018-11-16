#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 16:25:39 2018

@author: lars
"""

##Tensorflow issue with upgrades.
#https://github.com/tensorflow/tensorflow/issues/20778

import os
import time
import numpy as np
import warnings
import scipy
import SimpleITK as sitk

import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Cropping2D, ZeroPadding2D, Activation
from keras.layers.merge import concatenate
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras import backend as K
#from keras.preprocessing.image import apply_transform, transform_matrix_offset_center
#from evaluation import getDSC, getHausdorff, getLesionDetection, getAVD, getImages
K.set_image_data_format('channels_last')

import subprocess

#Global parameters of what, how should they be changed? #These should correspond to image sizes
rows_standard = 200 
cols_standard = 200
thresh_FLAIR = 70      #to mask the brain
thresh_T1 = 30
smooth=1.

flair=True #Retrieved from function.
t1=True #Retrieved from function.

def dice_coef_for_training(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_coef_loss(y_true, y_pred):
    return 1.-dice_coef_for_training(y_true, y_pred)

def conv_bn_relu(nd, k=3, inputs=None):
    conv = Conv2D(nd, k, padding='same')(inputs) #, kernel_initializer='he_normal'
    #bn = BatchNormalization()(conv)
    relu = Activation('relu')(conv)
    return relu

def get_crop_shape(target, refer):
        # width, the 3rd dimension
        cw = (target.get_shape()[2] - refer.get_shape()[2]).value
        assert (cw >= 0)
        if cw % 2 != 0:
            cw1, cw2 = int(cw/2), int(cw/2) + 1
        else:
            cw1, cw2 = int(cw/2), int(cw/2)
        # height, the 2nd dimension
        ch = (target.get_shape()[1] - refer.get_shape()[1]).value
        assert (ch >= 0)
        if ch % 2 != 0:
            ch1, ch2 = int(ch/2), int(ch/2) + 1
        else:
            ch1, ch2 = int(ch/2), int(ch/2)

        return (ch1, ch2), (cw1, cw2)

def get_unet(img_shape = None, first5=True):
        inputs = Input(shape = img_shape)
        concat_axis = -1

        if first5: filters = 5
        else: filters = 3
        conv1 = conv_bn_relu(64, filters, inputs)
        conv1 = conv_bn_relu(64, filters, conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        conv2 = conv_bn_relu(96, 3, pool1)
        conv2 = conv_bn_relu(96, 3, conv2)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

        conv3 = conv_bn_relu(128, 3, pool2)
        conv3 = conv_bn_relu(128, 3, conv3)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

        conv4 = conv_bn_relu(256, 3, pool3)
        conv4 = conv_bn_relu(256, 4, conv4)
        pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

        conv5 = conv_bn_relu(512, 3, pool4)
        conv5 = conv_bn_relu(512, 3, conv5)

        up_conv5 = UpSampling2D(size=(2, 2))(conv5)
        ch, cw = get_crop_shape(conv4, up_conv5)
        crop_conv4 = Cropping2D(cropping=(ch,cw))(conv4)
        up6 = concatenate([up_conv5, crop_conv4], axis=concat_axis)
        conv6 = conv_bn_relu(256, 3, up6)
        conv6 = conv_bn_relu(256, 3, conv6)

        up_conv6 = UpSampling2D(size=(2, 2))(conv6)
        ch, cw = get_crop_shape(conv3, up_conv6)
        crop_conv3 = Cropping2D(cropping=(ch,cw))(conv3)
        up7 = concatenate([up_conv6, crop_conv3], axis=concat_axis)
        conv7 = conv_bn_relu(128, 3, up7)
        conv7 = conv_bn_relu(128, 3, conv7)

        up_conv7 = UpSampling2D(size=(2, 2))(conv7)
        ch, cw = get_crop_shape(conv2, up_conv7)
        crop_conv2 = Cropping2D(cropping=(ch,cw))(conv2)
        up8 = concatenate([up_conv7, crop_conv2], axis=concat_axis)
        conv8 = conv_bn_relu(96, 3, up8)
        conv8 = conv_bn_relu(96, 3, conv8)

        up_conv8 = UpSampling2D(size=(2, 2))(conv8)
        ch, cw = get_crop_shape(conv1, up_conv8)
        crop_conv1 = Cropping2D(cropping=(ch,cw))(conv1)
        up9 = concatenate([up_conv8, crop_conv1], axis=concat_axis)
        conv9 = conv_bn_relu(64, 3, up9)
        conv9 = conv_bn_relu(64, 3, conv9)

        ch, cw = get_crop_shape(inputs, conv9)
        conv9 = ZeroPadding2D(padding=(ch, cw))(conv9)
        conv10 = Conv2D(1, 1, activation='sigmoid', padding='same')(conv9) #, kernel_initializer='he_normal'
        model = Model(inputs=inputs, outputs=conv10)
        model.compile(optimizer=Adam(lr=(2e-4)), loss=dice_coef_loss)

        return model

def Utrecht_preprocessing(FLAIR_image, T1_image):

    channel_num = 2
    
    print("Initial pre-pro:")
    print(np.shape(FLAIR_image))
    print(np.shape(T1_image))
    
    num_selected_slice = np.shape(FLAIR_image)[0]
    image_rows_Dataset = np.shape(FLAIR_image)[1]
    image_cols_Dataset = np.shape(FLAIR_image)[2]
    T1_image = np.float32(T1_image)
    FLAIR_image = np.float32(FLAIR_image)

    brain_mask_FLAIR = np.ndarray((num_selected_slice,image_rows_Dataset, image_cols_Dataset), dtype=np.float32)
    brain_mask_T1 = np.ndarray((num_selected_slice,image_rows_Dataset, image_cols_Dataset), dtype=np.float32)
    imgs_two_channels = np.ndarray((num_selected_slice, rows_standard, cols_standard, channel_num), dtype=np.float32)
    #imgs_mask_two_channels = np.ndarray((num_selected_slice, rows_standard, cols_standard,1), dtype=np.float32)

    # FLAIR --------------------------------------------
    brain_mask_FLAIR[FLAIR_image >=thresh_FLAIR] = 1
    brain_mask_FLAIR[FLAIR_image < thresh_FLAIR] = 0
    for iii in range(np.shape(FLAIR_image)[0]):
        brain_mask_FLAIR[iii,:,:] = scipy.ndimage.morphology.binary_fill_holes(brain_mask_FLAIR[iii,:,:])  #fill the holes inside brain
    
    ###SOMETHING HAPPENS HERE:
    print("Pre something T2:")
    print(np.shape(FLAIR_image))
    FLAIR_image = FLAIR_image[:,
                              (image_rows_Dataset/2-rows_standard/2):(image_rows_Dataset/2+rows_standard/2),
                              (image_cols_Dataset/2-cols_standard/2):(image_cols_Dataset/2+cols_standard/2)]
    print("Post something T2:")
    print(np.shape(FLAIR_image))
    
    brain_mask_FLAIR = brain_mask_FLAIR[:, 
                                        (image_rows_Dataset/2-rows_standard/2):(image_rows_Dataset/2+rows_standard/2), 
                                        (image_cols_Dataset/2-cols_standard/2):(image_cols_Dataset/2+cols_standard/2)]
    ###------Gaussion Normalization here
    FLAIR_image -=np.mean(FLAIR_image[brain_mask_FLAIR == 1])      #Gaussion Normalization
    FLAIR_image /=np.std(FLAIR_image[brain_mask_FLAIR == 1])
    # T1 -----------------------------------------------
    brain_mask_T1[T1_image >=thresh_T1] = 1
    brain_mask_T1[T1_image < thresh_T1] = 0
    for iii in range(np.shape(T1_image)[0]):
        brain_mask_T1[iii,:,:] = scipy.ndimage.morphology.binary_fill_holes(brain_mask_T1[iii,:,:])  #fill the holes inside brain
    
    ###SOMETHING HAPPENS HERE:
    print("Pre something T1:")
    print(np.shape(T1_image))
    T1_image = T1_image[:, 
                        (image_rows_Dataset/2-rows_standard/2):(image_rows_Dataset/2+rows_standard/2), 
                        (image_cols_Dataset/2-cols_standard/2):(image_cols_Dataset/2+cols_standard/2)]
    print("Post something T1:")
    print(np.shape(T1_image))
    
    brain_mask_T1 = brain_mask_T1[:, 
                                  (image_rows_Dataset/2-rows_standard/2):(image_rows_Dataset/2+rows_standard/2), 
                                  (image_cols_Dataset/2-cols_standard/2):(image_cols_Dataset/2+cols_standard/2)]
    #------Gaussion Normalization
    T1_image -=np.mean(T1_image[brain_mask_T1 == 1])      
    T1_image /=np.std(T1_image[brain_mask_T1 == 1])
    #---------------------------------------------------
    print("Pre np.newaxis:")
    print(np.shape(FLAIR_image))
    print(np.shape(T1_image))
    
    FLAIR_image  = FLAIR_image[..., np.newaxis]
    T1_image  = T1_image[..., np.newaxis]
    
    print("Post np.newaxis:")
    print(np.shape(FLAIR_image))
    print(np.shape(T1_image))
    
    imgs_two_channels = np.concatenate((FLAIR_image, T1_image), axis = 3)
    print("Post np.concatenate:")
    print(np.shape(imgs_two_channels))
    return imgs_two_channels

def Utrecht_postprocessing(FLAIR_array, pred):
    start_slice = 6
    num_selected_slice = np.shape(FLAIR_array)[0]
    image_rows_Dataset = np.shape(FLAIR_array)[1]
    image_cols_Dataset = np.shape(FLAIR_array)[2]
    original_pred = np.ndarray(np.shape(FLAIR_array), dtype=np.float32)
    original_pred[...] = 0
    original_pred[:,(image_rows_Dataset-rows_standard)/2:(image_rows_Dataset+rows_standard)/2,(image_cols_Dataset-cols_standard)/2:(image_cols_Dataset+cols_standard)/2] = pred[:,:,:,0]
    
    original_pred[0:start_slice, :, :] = 0
    original_pred[(num_selected_slice-start_slice-1):(num_selected_slice-1), :, :] = 0
    return original_pred

def do_unet_2017(input_dir,call_file_name):
    id_list_dir = os.listdir(input_dir)
    
    n = len(id_list_dir)
    n_i = 1
    
    for i in id_list_dir:
        #Printing context
        print "="*10
        print "At: " + str(n_i) + " of " + str(n) + " observations."
        print "ID: " + str(i)
        
        #Importing image of i'th individual:
        FLAIR_filename = input_dir + str(i) + '/' + 'T2_FLAIR_3D/t2_flair_3d.nii'
        FLAIR_image = sitk.ReadImage(FLAIR_filename)
        FLAIR_array = sitk.GetArrayFromImage(FLAIR_image)
        
        T1_image = sitk.ReadImage(input_dir + str(i) + '/' + 'T1_3D_SAG/t1_3d_sag.nii')
        T1_array = sitk.GetArrayFromImage(T1_image)
        
        print("T2 shape:")
        print(np.shape(FLAIR_array))
        print("T1 shape:")
        print(np.shape(T1_array))
        
        FLAIR_array_pad = np.pad(FLAIR_array, ((0,0),(0,0),(12,12)),'constant') #Padding axial up to 200. (Case specific)
        T1_array_pad = np.pad(T1_array, ((0,0),(0,0),(12,12)),'constant') #Padding axial up to 200. (Case specific)
        
        #Using Utrecht preprocessing since it seems the most "universal":
        imgs_test = Utrecht_preprocessing(FLAIR_array_pad, T1_array_pad)
        
        #Readying model:
        img_shape = (rows_standard, cols_standard, flair+t1)
        
        model = get_unet(img_shape, True)
        model_path = '/home/lars/Desktop/micca2017/weights_h5/0_final.h5'
        model.load_weights(model_path)
        print("Weights are loaded.")
        
        #Running prediction for i'th individual:
        pred = model.predict(imgs_test, batch_size=1, verbose=True)
        
        #Binarizing predictions:
        pred[pred > 0.5] = 1.
        pred[pred <= 0.5] = 0.
        
        #Postprocessing, mirroring pre_processing:
        print("Post-processing...")
        original_pred = Utrecht_postprocessing(FLAIR_array_pad, pred)
        
        #Depadding pred for comparison with original FLAIR_array. i.e. depadding axial down to 176. (Case specific)
        print("Pre depadding:")
        print(np.shape(original_pred))
        original_pred = original_pred[:,
                                      :,
                                      12:188] 
        print("Post depadding:")
        print(np.shape(original_pred))
        
        #Saving image(s):
        print("Saving...")
        filename_result_orig_pred = input_dir + str(i) + '/' + 'T2_FLAIR_3D/' + str(i) + '_WMH_NN_post.nii.gz'
        sitk.WriteImage(sitk.GetImageFromArray(original_pred), filename_result_orig_pred) #Output with wrong TranformationMatrix
        
        ##Force transformation matrix that is lost in original_pred
        filename_output = input_dir + str(i) + '/' + 'T2_FLAIR_3D/' + str(i) + '_WMH_NN_ok.nii.gz'
        fix_trans_matrix_command = 'fslmaths' + """ '""" + FLAIR_filename + """' """ + '-mul 0 -add' + """ '""" + filename_result_orig_pred + """' """ + """ '""" + filename_output + """'\n"""
        
        print("Shell call saved:")
        print(fix_trans_matrix_command)
        
        my_call_file = open(call_file_name, 'a')
        my_call_file.write(fix_trans_matrix_command)
        my_call_file.close()
        
        #Updating count.
        n_i = n_i + 1
        
        #End of loop
    
    print("End of function...")


##Running:
test_directory = "/home/lars/Desktop/wmh_thirty_cases_article/unet_run/test_data/"
out_calls = '/home/lars/Desktop/micca2017/output_runs/shell_call_transformation_fslmaths_30.txt' #Remember to delete this function for every run...

do_unet_2017(test_directory,out_calls)














