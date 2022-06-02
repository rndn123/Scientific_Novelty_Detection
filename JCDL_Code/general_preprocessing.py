#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import os
import re
import random
import pandas as pd
import re
import nltk
import string


# In[2]:


default = ['title', 'abstract', 'introduction', 'related work', 'experiments', 'experiment', 'result', 
           'results', 'experimental-setup', 'experimental setup', 'hyperparameter', 'hyperparameters',
           'ablation analysis', 'conclusion', 'background', 'future work', 'discussion', 'method']


# In[3]:


def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]


# In[4]:


def compare(s1, s2):
    s1 = re.sub('[^A-Za-z0-9]+', ' ', s1).lower()
    s2 = re.sub('[^A-Za-z0-9]+', ' ', s2).lower()
    l1 = s1.split()
    l2 = s2.split()
    l2 = [token for token in l2 if not token.isnumeric()]
    return l1 == l2, l1


# In[5]:


def full_sentence(lines):
    sentences = []
    sentence = ""
    for i in range(len(lines)):
        sentence += lines[i]
        if(lines[i].endswith('et al') or lines[i].endswith('et al.') or lines[i].endswith('et al .')):
            sentence += " "
        elif(lines[i].endswith('?') or lines[i].endswith('?:') or lines[i].endswith(';') 
             or lines[i].endswith(',')):
            sentence += " "
        else:
            sentences.append(sentence)
            sentence = ""
    return sentences


# In[6]:

path = "../stanza_files/Blogs/SA/*-Stanza-out.txt"
directory = glob.glob(path, recursive = True)
print(directory, path)
df = pd.DataFrame(columns = ['topic', 'paper_ID', 'text', 'main_heading', 'sub_heading', 
                             'label', 'pos1', 'pos2', 'pos3', 'citation'])
ID_list, text, length = [], [], []
main_heading, sub_heading = [], []
pos1, pos2, pos3, masks = [], [], [], []
for i, dir_path in enumerate(directory):
    
    print(i, dir_path)
    stanza_file = dir_path
    main_file = "".join((dir_path,"/main_heading.txt"))
    sub_file = "".join((dir_path,"/sub_heading.txt"))
    
    # Reading sentences from stanza file
    with open(stanza_file, encoding='ISO-8859-1') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = full_sentence(lines)
    
    # Initialize Heading and Sub_Heading as default list
    headings = default
    sub_headings = default
    
    # Check if main heading file exists
    if (os.path.isfile(main_file)):
        # Reading Main Heading from main_heading.txt
        with open(main_file, encoding='ISO-8859-1') as f:
            headings = f.readlines()
        # Reading Sub Heading from sub_heading.txt
        with open(sub_file, encoding='ISO-8859-1') as f:
            sub_headings = f.readlines()

            
    #Remove end of line from each line
    headings = [head.strip() for head in headings]
    sub_headings = [head.strip() for head in sub_headings]
    
    #Add paper_id and topic to list
    ID_list.extend([i]*len(lines))
    
    main_head, sub_head, mask = "", "", 0
    # Enumerating lines in stanza file
    for i, line in enumerate(lines):
        
        head_flag, sub_flag = False, False
        
        # Check whether this sentence is a heading
        for head in headings:
            flag, temp_list = compare(head, line)
            if(flag and len(temp_list)):
                main_head = " ".join(temp_list)
                head_flag = True
                break
        
        # Check whether this sentence is a sub heading
        for head in sub_headings:
            flag, temp_list = compare(head, line)
            if(flag and len(temp_list)):
                sub_head = " ".join(temp_list)
                sub_flag = True
                break
        
        #print(i, head_flag, sub_flag)
        #print(line)
        
        if(line.lower() == 'Referemces'):
            mask = 1
        
        # Adding current sentence data to a list
        text.append(line)
        pos1.append(i+1)
        main_heading.append(main_head)
        sub_heading.append(sub_head)
        length.append(len(line.split()))
        masks.append(mask)
        
        # If sentence is a main_heading
        if (head_flag == True):
            pos2.append(1)
            pos3.append(1)
        else:
            pos2.append(pos2[-1]+1)
            # If sentence is a sub_heading
            if (sub_flag == True):
                pos3.append(1)
            else:
                pos3.append(pos3[-1]+1)
                


# In[7]:


df = pd.DataFrame({"topic" : "summarization", "paper_ID" : ID_list, "main_heading" : main_heading, "sub_heading" : sub_heading, 
                   "text" : text, "pos1" : pos1, "pos2" : pos2, "pos3" : pos3, "length" : length, "masks" : masks})


# In[8]:


df = df[~(df['main_heading'].isin(['conclusion', 'background', 'future work', 'related work'])) & 
        (df['masks'] == 0) & (df['length'] > 4)].reset_index(drop = True)
df.drop(columns = ['masks'], inplace = True)


# In[9]:


df


# In[10]:


def surrounding(df):
    text = df['text'].tolist()
    pos3 = df['pos3'].tolist()
    prev_text = []
    next_text = []
    for i, x in enumerate(pos3):
        if x > 2:
            prev_text.append(text[i-1])
        else:
            prev_text.append(" ")
        if x < 3:
            next_text.append(" ")
        else:
            next_text.append(text[i])
    if (len(next_text) > 0):
    	next_text.pop(0)
    next_text.append(" ")
    df['prev_text'] = prev_text
    df['next_text'] = next_text
    return df


# In[11]:


df = surrounding(df)


# In[12]:


df.sort_values(['paper_ID', 'pos1', 'pos2', 'pos3'], ascending=[True, False, False, False], inplace=True)

p1, p2, p3 = 1,1,1
l1, l2, l3 = 1,1,1
ofs1 = []
ofs2 = []
ofs3 = []
for index, row in df.iterrows():
    if(row['pos1']>=p1):
        l1 = row['pos1']
    p1 = row['pos1']
    ofs1.append(p1/l1)
    if(row['pos2']>=p2):
        l2 = row['pos2']
    p2 = row['pos2']
    ofs2.append(p2/l2)
    if(row['pos3']>=p3):
        l3 = row['pos3']
    p3 = row['pos3']
    ofs3.append(p3/l3)

df['ofs1'] = ofs1
df['ofs2'] = ofs2
df['ofs3'] = ofs3

df.sort_values(['paper_ID', 'pos1', 'pos2', 'pos3'], ascending=[True, True, True, True], inplace=True)


# In[13]:


df


# In[14]:


df.to_csv("SA_dataset.csv", index = None)

