import stanza
import grobid_tei_xml
import os
import re
import glob

path_xml = "XML_files/MT/*.tei.xml"
directory = glob.glob(path_xml)
print(len(directory))

for i, file_path in enumerate(directory):
	
	grobid_dir = "grobid_files/" + path_xml[10:-10]
	stanza_dir = "stanza_files/" + path_xml[10:-10]
	
	if(not os.path.isdir(grobid_dir)):
		os.mkdir(grobid_dir)
	if(not os.path.isdir(stanza_dir)):
		os.mkdir(stanza_dir)
	
	grobid_file = "grobid_files/" + file_path[10:-8] + "-Grobid-out.txt"
	stanza_file = "stanza_files/" + file_path[10:-8] + "-Stanza-out.txt"
	
	if(os.path.isfile(grobid_file) and os.path.isfile(stanza_file)):
		print(i)	
		continue
	    
	print(grobid_file, stanza_file)
	
	print(i, file_path)
	
	with open(file_path, 'r') as f:
	  data = f.read()

	doc = grobid_tei_xml.parse_document_xml(data)
	title = doc.header.title
	abstract = doc.abstract
	body = doc.body
	if(body == None):
		continue
	body = re.sub(r'[^\x00-\x7F]+','?', body)

	body = body.split('\n')

	with open(grobid_file, "w") as f:
	  f.write("title\n")
	  if (title != None):
	    f.write(title)
	    f.write("\n\n")
	  f.write("abstract\n")
	  if(abstract != None):
	    abstract = re.sub(r'[^\x00-\x7F]+','?', abstract)
	    f.write(abstract)
	  f.write("\n")
	  for text in body:
	    f.write("\n")
	    tokens = text.split()
	    if(len(tokens) == 0):
	       continue
	    heading = tokens[0]
	    f.write(text)
	    f.write("\n")
	    if(heading == 'Conclusion' or heading == 'References'):
	      break


	with open(grobid_file, "r") as f:
	  grobid_lines = f.readlines()

	nlp = stanza.Pipeline(lang='en', processors='tokenize')

	stanza_lines = []
	for line in grobid_lines:
	  doc = nlp(line)
	  for i, sentence in enumerate(doc.sentences):
	    tokens = [token.text for token in sentence.tokens]
	    sent = " ".join(tokens)
	    sent = sent+"\n"
	    stanza_lines.append(sent)

	with open(stanza_file, "w") as f:
	  f.writelines(stanza_lines)
