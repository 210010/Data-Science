#loads saved checkpoint & generates output

import pandas as pd 
import numpy as np
import gpt_2_simple as gpt2
import tensorflow as tf
import datetime 
import glob 
import os

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')

gen_file = 'gpt2_gentext.txt'


gpt2.generate_to_file(sess,
                      destination_path=gen_file,
                      length=300,
                      temperature=0.75,
                      nsamples=1,
                      batch_size=1
                      )

with open('gpt2_gentext.txt', 'r') as in_file:
  desc = [line.strip('=*') for line in in_file]
df = pd.DataFrame({'descriptions':desc})
df.to_csv('log.csv')
df.head()