import pandas as pd
import numpy as np
import random
import re
import torch
from tqdm import tqdm
import transformers

from transformers import AutoTokenizer, AutoModel

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased').to(device)

def remove(x):
    return x.replace('"', ' ').lower()

def weights(df):
	
	df['triplets'] = df['sub'] + " " + df['pred'] + " " + df['obj']
	triplets = (df['triplets']).tolist()

	sub_obj = (df['sub'] + " " + df['obj']).tolist()
	predicate = df['pred'].tolist()

	weights = []
	for pred, sub in tqdm(zip(predicate, sub_obj), total = len(predicate)):
	    input_ids = torch.tensor(tokenizer.encode(pred)).unsqueeze(0).to(device)
	    output1 = model(input_ids)[0][0][0]
	    input_ids = torch.tensor(tokenizer.encode(sub)).unsqueeze(0).to(device)
	    output2 = model(input_ids)[0][0][0]
	    norm1 = torch.linalg.norm(output1)
	    norm2 = torch.linalg.norm(output2)
	    dot = torch.dot(output1, output2)
	    outputs = dot/(norm1 * norm2)
	    weights.append(outputs.item())

	df['pred_weights'] = weights
	
	return df

df1 = pd.read_csv("JCDL_Triplets/KG/MT_triplets_results.csv")
df2 = pd.read_csv("JCDL_Triplets/Non_Novel/MT_PDF_triplets_results.csv")
df = pd.concat([df1, df2])
df.dropna(inplace = True)
df['sub'] = df['sub'].apply(remove)
df['obj'] = df['obj'].apply(remove)
df = weights(df)
df.to_csv("JCDL_Triplets/KG/MT_triplets_weights.csv", index = None)

df_blogs = pd.read_csv("JCDL_Triplets/Blogs/MT_Blogs_triplets_results.csv")
df_blogs['sub'] = df_blogs['sub'].apply(remove)
df_blogs['obj'] = df_blogs['obj'].apply(remove)
df_blogs = weights(df_blogs)
df_blogs.to_csv("JCDL_Triplets/Blogs/MT_Blogs_triplets_weights.csv", index = None)

df_blogs = pd.read_csv("JCDL_Triplets/Novel/MT2021_triplets_results.csv")
df_blogs['sub'] = df_blogs['sub'].apply(remove)
df_blogs['obj'] = df_blogs['obj'].apply(remove)
df_blogs = weights(df_blogs)
df_blogs.to_csv("JCDL_Triplets/Novel/MT2021_triplets_weights.csv", index = None)



