#In this repository we have shared the code

**JCDL_Dataset_Statistics.ipynb** - Statistics of Triplets in a csv file, Input - triplets csv file path

**JCDL_Classification_Algorithm.ipynb** - Classification of Papers into Novel and Non-Novel, Input - Novel papers results csv file path, Non-Novel papers (Blogs) results csv file path

**Knowledge_Graph.ipynb** - Knowledge Graph Neo4j Visulation, Input - triplets csv file path

**Algorithm_weights.ipynb** - Calculate the edge weights between the nodes for the triplets, Input - triplets csv file path

**Algorithm.ipynb** - Calculate TR Score of Only Background Knowledge Graph

**JCDL_Graph.ipynb** - Graph Analysis, Input - KL Divergence Results, Variance Results csv file

**grobid_and_stanza.py** - Convert XML files to grobid and stanza txt files, threre should be 3 folders, XML_files - stored XML_files, grobid_files - output grobid files will be stored here
stanza_files - output stanza files will be stored here

**general_preprocessing.py** - Input - Stanza files, Output - CSV files to be input to the pipeline

**Preprocessing.py** - Calculate the edge weights between the nodes for the triplets

**Non_Novel_Papers.py** - Processing Non Novel Papers Triplets

**Novel_Papers.py** - Processing Novel Papers Triplets

**merge.py** - Merge All results for Novel Papers i.e. Merge Multiple Slots Novel Papers Results to one csv file


# In directory Triplets there are preprocessed csv files

In the current directory
Create a JCDL_Results  directory to store the results

Run the following .py files

**python Non_Novel_Papers.py** - Generates the results of all Blogs \
**python Novel_Papers.py** - Generates the results of Novel Papers numbered from start_paper to end_paper (excluded) \
**python merge.py** - Merge all Novel Papers Results 

Then run
**JCDL_Classification_Algorithm.ipynb**
