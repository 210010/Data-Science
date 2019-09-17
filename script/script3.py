#post-processing of generated company descriptions to improve output quality

import pandas as pd
import spacy 
from spacy import displacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

# Function to make the output more readable
def print_line(line):
  while len(str(line)) > 90:
    print(line[:90])
    line = line[90:]
  print(line,'\n\n')

def cleanup(desc):
  '''Cleans output from gpt-2, start/end of description markers left in'''
  desc = desc.replace('<|startoftext|>','').replace('<|endoftext|>\n','')
  return desc.strip()

def word_freq(desc):
  '''Return frequency of unique words not in stopwords'''
  desc = str(desc).lower()
  full_len = len(desc.split())
  stopwords = ['founded by', 'is based in', 'was founded in', 
                'is headquartered in', 'headquarters in', 'developed by',
                'developed in', 'additional offices', 'germany',
                'france', 'china', 'california', 'india', 'wholly-owned'
                'silicon valley', 'san francisco', 'established in',
                'mountain view', 'family owned', 'family-owned', 
                'clients include', 'argentina', 'brazil', 'chile', 'colombia', 
                'japan', 'korea', 'malaysia', 'mexico', 'subsidiary',
                'formerly known as', 'venture capital', 'for more information']
  
  # Drop words that encode garbage info, thus penalizing on the frequency score
  for phrase in stopwords:
    desc = desc.replace(phrase,'')
  
  split_desc = str(desc).split()
  
  # Calculate unique word frequency, return 0 if description is too small
  if ((len(split_desc) < 10) | (long_word(split_desc))):
    return 0
  return len(set(split_desc)) / full_len

def entity_freq(text, nlp):
  '''Return frequency of low value entities'''
  doc = nlp(text)
  count = 0
  
  # Use Spacy to pull find entities and count them
  for X in doc.ents:
    if (X.label_ in ['ORG', 'DATE', 'PERSON', 'TIME', 'PERCENT', 'MONEY']):
      count += 1
      
  return count/len(text.split())

def long_word(desc, length=20):
  '''Return True if description contains words too long'''
  for word in desc:
    if len(word) >= length:
      return True
  
  return False

## Culling

# Read in the generated descriptions
df = pd.read_csv('log.csv')
df = df.drop('Unnamed: 0', axis=1)
df['descriptions'] = df['descriptions'].apply(cleanup)
df = df[df['descriptions'] != '']

# Begin culling and formatting the dataframe
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

df.describe()

# Look at all descriptions
for i in range(0,len(df)):
  print('Word Frequency:', df['word_freq'][i])
  print('Entity Frequency:', df['ent_freq'][i])
  print_line(df['descriptions'][i])