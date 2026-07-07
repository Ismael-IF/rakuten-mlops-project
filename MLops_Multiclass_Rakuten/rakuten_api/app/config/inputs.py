# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pickle
import tensorflow as tf


# Define directories    

# Local new
# model_dir  =                 './app/models/trained_models/'
# tokenizer_dir  =             './app/models/tokenizer/'

#Docker
model_dir  =                 '/app/models/trained_models/'
tokenizer_dir  =             '/app/models/tokenizer/'


conv1D_fname  =              'conv1d_text_model.h5'
simpleDNN_fname  =           'Model_Texte_SimpleDNN.hdf5'
xception_fname =             'Model_Images_Xception.hdf5'
inception_fname =            'Model_Images_InceptionV3.hdf5'

df_train_sple =              'Xtrain_samples.pkl'
fitted_tokenizer_name =      'fitted_tokenizer.pickle'

xception_im_shape =          (299, 299)
inception_im_shape =         (299, 299)

xception_SC =                0.66
inception_SC =               0.64
conv1D_SC   =                0.80
simplDNN_SC =                0.81


conv1D_w   =                0.35
simplDNN_w =                0.36
xception_w =                0.29
inception_w =               0.29







