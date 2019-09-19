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

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')

#concatenation of inital descriptions.
gen_file = 'gpt2_gentext.txt'
print('gen_file created!')

print('Beginning Generation....')
gpt2.generate_to_file(sess,
                      destination_path=gen_file,
                      length=400,
                      temperature=0.85,
                      nsamples=1000,
                      batch_size=20
                      )
print('Generation complete!')

with open('gpt2_gentext.txt', 'r') as in_file:
  desc = [line.strip('=*') for line in in_file]
df = pd.DataFrame({'descriptions':desc})
df.to_csv('log.csv')
print('log saved!')

def print_line(line):
  while len(str(line)) > 90:
    print(line[:90])
    line = line[90:]
  print(line,'\n\n')

def cleanup(desc):
  # Cleans output from gpt-2, start/end of description markers left in
  df = df[df['descriptions'].str.startswith('<|startoftext|>') & 
          df['descriptions'].str.endswith('<|endoftext|>\n')]
  df['descriptions'] = df['descriptions'].apply(cleanup)
  df = df.drop('Unnamed: 0', axis=1).reset_index(drop=True)
  df = df[df['descriptions'] != '']
  desc = desc.replace('<|startoftext|>','').replace('<|endoftext|>\n','')
  print('cleanup complete!')
  return desc.strip()

def long_word(desc, length=20):
  '''Return True if description contains words too long'''
  for word in desc:
    if len(word) >= length:
      return True
  
  return False


def remove_stop_words(desc, nlp):
  '''Remove default spacy stopwords and punctuation from a description'''
  spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
  
  doc = nlp(desc)
  tokens = [token.text 
            for token in doc 
            if not token.is_stop and not token.is_punct]

  return tokens


def remove_stop_phrases(desc):
  '''Remove phrases that encode little to no value in generated descriptions'''
  stop_phrases = ['founded by', 'is based in', 'was founded in', 
                'is headquartered in', 'headquarters in', 'developed by',
                'developed in', 'additional offices', 'germany',
                'france', 'china', 'california', 'india', 'wholly-owned'
                'silicon valley', 'san francisco', 'established in',
                'mountain view', 'family owned', 'family-owned', 
                'clients include', 'argentina', 'brazil', 'chile', 'colombia', 
                'japan', 'korea', 'malaysia', 'mexico', 'subsidiary',
                'formerly known as', 'venture capital', 'for more information',
                'new york', 'united states', 'u.s.', 'u.s.a']
  
  for phrase in stop_phrases:
    desc = desc.replace(phrase,'')
    
  return desc


def word_freq(desc, nlp):
  '''Return frequency of unique words not in stopwords/phrases'''
  full_desc_len = len(str(desc).split())

  desc = remove_stop_phrases(str(desc).lower())
  desc = remove_stop_words(desc, nlp)

  # Calculate unique word frequency, return 0 if description is too small
  if ((len(desc) < 10) | (long_word(desc))):
    return 0
  return len(set(desc)) / full_desc_len


def reduce_by_word_freq(df):
  '''Reduce df size by narrowing word frequency range'''
  lower = df['word_freq'].median()
  upper = df['word_freq'].median() + df['word_freq'].std()

  return df[(df['word_freq'] > lower) & (df['word_freq'] < upper)]


def entity_freq(text, nlp):
  '''Return frequency of low value entities'''
  doc = nlp(text)
  count = 0
  
  # Use SpaCy to find entities and count low value ones
  for X in doc.ents:
    if (X.label_ in ['ORG', 'DATE', 'PERSON', 'TIME', 'PERCENT', 'MONEY']):
      count += 1
      
  return count/len(text.split())

# dropping emptys and applying cleanup
df = pd.read_csv('https://raw.githubusercontent.com/labs15-pain-point/Data-Science/master/script/log.csv')
df = df.drop('Unnamed: 0', axis=1)
df['descriptions'] = df['descriptions'].apply(cleanup)
print('cleanup complete!')
df = df[df['descriptions'] != '']

start_sum = df['descriptions'].count()
print('Descriptions before any drops:', start_sum)

df['word_freq'] = df['descriptions'].apply(word_freq)
df = df[df['word_freq'] >.6]
df['ent_freq'] = [entity_freq(desc, nlp) for desc in df['descriptions']]

word_freq_cond = ((df['word_freq'] > .75) & (df['word_freq'] < .925))
ent_freq_cond = (df['ent_freq'] < .04)
df = df[word_freq_cond & ent_freq_cond].reset_index().drop('index', axis=1)

print('Descriptions after frequency windows:', df['descriptions'].count())
print('% Kept from Batch:', df['descriptions'].count()/start_sum)

#generating to JSON
df.to_json('generated_descriptions.json')
