#downloads GPT-2, trains model, creates & saves checkpoint

import pandas as pd 
import numpy as np
import gpt_2_simple as gpt2
import tensorflow as tf
import datetime 
import glob 
import os 

gpt2.download_gpt2(model_name="345M")

files_1 = os.listdir('../csvs/')
files_2 = os.listdir('../crunchbase_csv/')

df = pd.concat([pd.read_csv(f, error_bad_lines=False) for f in glob.glob('../csvs/*.csv')], ignore_index = True)
df_2 = pd.concat([pd.read_csv(f, error_bad_lines=False) for f in glob.glob('../crunchbase_csv/*.csv')], ignore_index = True)
df_big = pd.concat([df, df_2], ignore_index = True)

df_final = df_big.drop(['Organization Name URL', 'Organization Name', 'Description'], axis = 1)
df_final.to_csv('big_boy_df.csv')
df_final['Categories'] = df_final['Categories'].str.lower()

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

#steps is set to 3 in in order to test script; increase as needed.
sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              dataset=file_name,
              model_name='345M',
              accumulate_gradients = 13,
              steps=3,
              restore_from='fresh',
              run_name='run1',
              print_every=10,
              sample_every=100,
              save_every=250, 
              only_train_transformer_layers=False
              )


checkpoint_folder = os.path.join('checkpoint', run_name)
if copy_folder:
        shutil.copytree(checkpoint_folder, "./script" + checkpoint_folder)
else:
    file_path = get_tarfile_name(checkpoint_folder)
    # Reference: https://stackoverflow.com/a/17081026
    with tarfile.open(file_path, 'w') as tar:
        tar.add(checkpoint_folder)
    shutil.copyfile(file_path, "./script" + file_path)


def get_tarfile_name(checkpoint_folder):
    tarfile_name = checkpoint_folder.replace(os.path.sep, '_') + '.tar'

    return tarfile_name        


gpt2.copy_checkpoint_to_gdrive(run_name='run1')