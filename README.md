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

Python Environment: The Python environment accessible to PostgreSQL should have the necessary libraries installed: After test that this program is working

Test that summarization is working using the following

$python summary.py 


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

2 - 


