import pandas as pd
import numpy as np
import random
import re
import torch
from tqdm import tqdm
import transformers

from transformers import AutoTokenizer, AutoModel

#device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

#tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
#model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased').to(device)


# In[1]:


import pandas as pd
import numpy as np
import random
import re
import torch
import copy
from tqdm import tqdm


# In[2]:


information_units = ['Results', 'Model', 'Experimental setup', 'Contribution', 'Hyperparameters', 
                    'Ablation analysis', 'Baselines', 'Experiments', 'Approach']


# In[3]:


df = pd.read_csv("Triplets/SKG/MT_triplets.csv")
df.dropna(inplace = True)


# In[4]:


df_temp = df.rename(columns = {"sub" : "obj", "obj" : "sub"})
df = pd.concat([df, df_temp]).reset_index(drop = True)


# In[6]:

d = 0.85**6
print(d)


# In[ ]:


nodes = df['sub'].unique()
tr_nodes = dict()
for key in nodes:
    tr_nodes[key] = 1


# In[ ]:


df_blogs = pd.read_csv("JCDL_Triplets/Blogs/MT_Blogs_triplets_weights.csv")
df_blogs = pd.concat([df_blogs, df_blogs.rename(columns = {"sub" : "obj", "obj" : "sub"})]).reset_index(drop = True)



# In[ ]:


total_papers = df_blogs['paper_ID'].max()+1


# In[ ]:


delta_dict = dict()


# In[ ]:


for i in range(total_papers):
    tr_updated_nodes = copy.deepcopy(tr_nodes)
    df_blog = df_blogs[df_blogs['paper_ID'] == i]
    df_doc = pd.concat([df, df_blog])
    pred_dict = dict(zip(df_doc.triplets, df_doc.pred_weights))
    doc_nodes = df_blog['sub'].unique()
    nodes = df_doc['sub'].unique()
    for sub in nodes:
        df_temp = df_doc[df_doc['sub'] == sub]
        x = df_temp['pred'].to_list()
        y = df_temp['obj'].to_list()
        t = df_temp['triplets'].to_list()
        summation = 0
        for pred, obj, triplet in zip(x,y,t):
            z = df_doc[(df_doc['sub'] == obj)]['triplets'].to_list()
            sum_den = sum([pred_dict[key] for key in z])
            if(sum_den == 0):
                continue
            #triplet = sub + " " + pred + " " + obj
            if obj in tr_nodes.keys():
                add = pred_dict[triplet] * tr_nodes[obj] / sum_den
            else:
                add = pred_dict[triplet] / sum_den
            summation += add
        print(summation)
        tr_updated_nodes[sub] = 1-d + d*summation
    tr_updated = np.array(list(tr_updated_nodes.values()))
    variance = np.var(tr_updated)
    probd = df_blog['sub'].value_counts()/len(df_blog.index)
    probr = df_doc['sub'].value_counts()/len(df_blog.index)
    prob = pd.merge(probd, probr, left_index = True, right_index = True)
    prob['log'] = np.log(prob['sub_x']) - np.log(prob['sub_y'])
    prob['sum'] = prob['log']*prob['sub_x']
    KL_score = prob['sum'].sum()
    delta_dict[i] = (KL_score, variance)


# In[ ]:


key_value, KL_score, variance = [], [], []
for key, value in delta_dict.items():
    key_value.append(key)
    KL_score.append(value[0])
    variance.append(value[1])


# In[ ]:


df_non_novel = pd.DataFrame({'paper_ID' : key_value, "KL_score" : KL_score, 'variance' : variance})
df_non_novel.to_csv("JCDL_Results/MT_Non_Novel_Results.csv", index = None)

