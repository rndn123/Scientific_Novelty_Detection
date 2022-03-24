# Scientific_Novelty_Detection
Phrase Extraction
We use BERT-CRF model to extract the phrases from the contribution sentences. 
The BERT-based model is efficient for contextual representations of the sentences. 
We train model two additional datasets SciERC and SciClaim. The SciERC  dataset includes annotations for scientific entities, 
their relations, and coreference clusters. 
This dataset is annotated for 500 scientific abstracts and the Sciclaim 12,738 annotations on 901 sentences from expert-identified claims in SBS
papers, recognized causal language in PubMed papers, and claims and causal language heuristically discovered from CORD-19 abstracts. 

Triplet Extraction
From the phrase extraction model, we receive discrete phrases.
Next, we have to organize these phrases into triplets (subject, predicate), and (object). 
To learn in deep of the triplet's characteristics, we categorized triplets into five categories A, B, C, D, E. For the type  A, B, C, D, 
we use four Bidirectional Encoder Representations from Transformer (BERT)-based classifiers to validate triplets and extract type E triplets 
using a rule-based approach. We use the \textit{Neo4j} platform for the visualization of the knowledge graph. Neo4j is a graph database optimized 
for storing graph nodes, attributes, and edges.
