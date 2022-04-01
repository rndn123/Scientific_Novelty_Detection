import pandas as pd
import numpy as np

df = pd.read_csv("JCDL_Results/MT_Novel_Results_0.csv")

for i in range(1,12):
	df_temp = pd.read_csv(f"JCDL_Results/MT_Novel_Results_{i}.csv")
	df = pd.concat([df, df_temp])

df.to_csv("JCDL_Results/MT_Novel_Results.csv")


