# SimilaritySearch-Summarization
Similarity Search on PDF and Summarization using Huggingface Models

The objective of this experiment is to leverage 2 types of models in conjunction with PostgreSQL, employing the pgvector extension and PL/Python to execute transformation functions directly within the database for efficient searching. 

Use https://huggingface.co/sentence-transformers/all-distilroberta-v1 for generating embeddings on PDF content and for semantic search

Use https://huggingface.co/allenai/led-base-16384 for generating a summary of the content

Insert inside a Postgres Table containing Vectors

Search using a Streamlit Python application on the Postgresql table using Similarity Search

# Requirements

Postgresql 16 installed. 

EDB Language pack installed. 

Run pip install from EDB Python directory as: 
/Library/edb/languagepack/v4/Python-3.11/bin/pip install -r requirements.txt

Install pgvector 0.6 extension from https://github.com/pgvector/pgvector

Install plpython3u extension in the database

create extension plpython3u;

Validate that pl-python3u is working well

postgres=# select public.test_plpython(); 

test_plpython

PL/Python is working! (1 row)

Test that summarization is working using the following OS command. Both programs are in code directory

$python summary.py 

francksidi@MAC-P94C5HH2F1 python % python summary.py                        

Model loading time: 1.31 seconds

Tokenization time: 0.00 seconds

Summary generation time: 21.24 seconds

Generated Summary:
        Jupiter is the fifth planet from the Sun and the largest in the Solar System.                         It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined.             Jupiter is one of the brightest objects visible to the naked eye in the night sky and has been known to ancient civilizations since before recorded history.                   

Total execution time: 22.55 seconds


Test The all-disti model using a python program 
$python alldisti.py

francksidi@MAC-P94C5HH2F1 python % python alldisti.py 

Loading model 'all-distilroberta-v1'...

Generating embeddings...

Embeddings generated:

[[-2.70629954e-02 -3.84049043e-02 -2.54163481e-02 -2.84959245e-02

   7.88855255e-02  1.37084955e-02 -3.98023706e-03  7.30625391e-02
  
  -1.32552511e-03 -3.03104613e-02 -4.47093211e-02 -3.02385204e-02



  ...

     4.33775224e-02 -1.07817305e-02 -3.86205278e-02 -2.25081146e-02]]

The size (dimensionality) of the embeddings vector is: 768




# Create all DDL 

1 - Create The Target Table 

CREATE TABLE IF NOT EXISTS public.demopdf_bert
(
    id serial,
    pdfpath text ,
    embeddings vector(768),
    summary text 
)

TABLESPACE pg_default;

2 - Create the function to load pdf and  generate summary 
Use the script in ddl: insert_embeddings_from_pdf_bert.sql

3 - Create the function get_embedding_bert_f as this function will be called by the application to generate the embedding 
of the input text 

# Generate Data

The best will be to put inside a directory many pdfs, I put some sample in dataset directory and then run from sql command: 

truncate table public.demopdf_bert;
select public.insert_embeddings_from_pdf_bert('/Users/francksidi/Downloads/pdf')

NOTICE:  Sentence Transformer Model Loaded

NOTICE:  BART Model and Tokenizer for Summarization Loaded

NOTICE:  Found 10 PDF files

NOTICE:  Text extraction for /Users/francksidi/Downloads/pdf/SBSA_Oracle Migration.pdf took 0.59 seconds

NOTICE:  Embedding generation for /Users/francksidi/Downloads/pdf/SBSA_Oracle Migration.pdf took 0.73 seconds

NOTICE:  Summary generation for /Users/francksidi/Downloads/pdf/SBSA_Oracle Migration.pdf took 8.58 seconds

NOTICE:  Insert operation for /Users/francksidi/Downloads/pdf/SBSA_Oracle Migration.pdf took 0.01 seconds

NOTICE:  Total processing time for /Users/francksidi/Downloads/pdf/SBSA_Oracle Migration.pdf was 9.90 seconds

NOTICE:  Text extraction for /Users/francksidi/Downloads/pdf/DemoBlog.pdf took 0.73 seconds

NOTICE:  Embedding generation for /Users/francksidi/Downloads/pdf/DemoBlog.pdf took 0.18 seconds

NOTICE:  Summary generation for /Users/francksidi/Downloads/pdf/DemoBlog.pdf took 8.29 seconds

NOTICE:  Insert operation for /Users/francksidi/Downloads/pdf/DemoBlog.pdf took 0.00 seconds

NOTICE:  Total processing time for /Users/francksidi/Downloads/pdf/DemoBlog.pdf was 9.20 seconds

NOTICE:  Text extraction for /Users/francksidi/Downloads/pdf/pa-edb-and-openshift-brief-703263pr-202402-en.pdf took 0.17 seconds

NOTICE:  Embedding generation for /Users/francksidi/Downloads/pdf/pa-edb-and-openshift-brief-703263pr-202402-en.pdf took 0.18 seconds

NOTICE:  Summary generation for /Users/francksidi/Downloads/pdf/pa-edb-and-openshift-brief-703263pr-202402-en.pdf took 8.16 seconds

NOTICE:  Insert operation for /Users/francksidi/Downloads/pdf/pa-edb-and-openshift-brief-703263pr-202402-en.pdf took 0.00 seconds

NOTICE:  Total processing time for /Users/francksidi/Downloads/pdf/pa-edb-and-openshift-brief-703263pr-202402-en.pdf was 8.51 seconds

NOTICE:  Text extraction for /Users/francksidi/Downloads/pdf/Percona_vs_C360_Battlecard_Aug2023.pdf took 0.10 seconds

...

NOTICE:  Summary generation for /Users/francksidi/Downloads/pdf/pem_v9_documentation.pdf took 7.08 seconds

NOTICE:  Insert operation for /Users/francksidi/Downloads/pdf/pem_v9_documentation.pdf took 0.00 seconds

NOTICE:  Total processing time for /Users/francksidi/Downloads/pdf/pem_v9_documentation.pdf was 39.45 seconds


Successfully run. Total query runtime: 2 min 12 secs.

# Run the application 

Run from the command line. Copy the logo.png image in the directory in which the python program is running. 

streamlit run pdf_search_bert.py






