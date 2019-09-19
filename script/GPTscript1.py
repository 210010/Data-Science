#downloads GPT-2, trains model, generates and discriminates output

#in your environment:
'''
tensorflow
spacy
pandas
numpy
sklearn
gpt_2_simple

python -m spacy download en_core_web_sm
'''

import pandas as pd 
import numpy as np
import gpt_2_simple as gpt2
import tensorflow as tf
import datetime 
import glob 
import os 
import tarfile
import json
import requests
import sys
import shutil
import re
from tqdm import tqdm, trange
from tensorflow.core.protobuf import rewriter_config_pb2
import time
from datetime import datetime
import csv
import argparse
import spacy
from spacy import displacy
from collections import Counter
import wget

import en_core_web_sm

nlp = spacy.load('en_core_web_sm')

#can be subbed for 124M model for testing/iter
gpt2.download_gpt2(model_name="345M")

#concatenation of inital descriptions.
files_1 = os.listdir('../csvs/')
files_2 = os.listdir('../crunchbase_csv/')

df = pd.concat([pd.read_csv(f, error_bad_lines=False) for f in glob.glob('../csvs/*.csv')], ignore_index = True)
df_2 = pd.concat([pd.read_csv(f, error_bad_lines=False) for f in glob.glob('../crunchbase_csv/*.csv')], ignore_index = True)
df_big = pd.concat([df, df_2], ignore_index = True)

#dropping (maybe) extraneous columns
df_final = df_big.drop(['Organization Name URL', 'Organization Name', 'Description'], axis = 1)
df_final.to_csv('big_boy_df.csv')
df_final['Categories'] = df_final['Categories'].str.lower()

# filtering out unfeasible ideas
df_final = df_final[df_final['Categories'].str.contains('medical|constructi'\
'on|biotechnology|bitcoin|biomedical|health|care|physical security|delivery'\
'marketing|tobacco|cryptocurrency|pharmaceutical|therapeutics|manufacturin'\
'g|hardware|virtual currency|3d|infrastructure|blockchain|oil and gas|food '\
'processing|chemical|hospitality|mining|mobile|telecommunications|Wireless'\
'|photography|robotics|security|jewelry|semiconductor|energy|building|mate'\
'rial|industrial|nanotechnology|real estate|drones|packaging|recruiting|sta'\
'ffing|broadcasting|virtual reality|consumer, women\'s|wearables|insur|paas|'\
'compliance|nurs|funeral|energy|medic|pharma|wastewater|water treat|billing|'\
'debt|lending|cloud archi|voip|care|gene|sex|adult|medical|dental|neuro|pharma'\
'ceutic|vaccine|anti|finance|counseling|advertising|banking|forestry|fintech|p'\
'ayments|outsourcing|cloud|publishing|aerospace|classifieds|shipping|electroni'\
'cs|sales|b2b|tv production|risk|healthcare')==False]


train = df_final['Full Description']
train.to_csv('train.csv', sep = ' ', index = False, header = False)

file_name = "train.csv"

#steps is set to 3 in in order to test script; increase as needed, 2000 base.
sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              dataset=file_name,
              model_name='345M',
              accumulate_gradients = 13,
              steps=2000,
              restore_from='fresh',
              run_name='run1',
              print_every=10,
              sample_every=250,
              save_every=250, 
              only_train_transformer_layers=False
              )
print('Training complete!')