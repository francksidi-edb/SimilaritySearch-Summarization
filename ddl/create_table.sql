CREATE TABLE IF NOT EXISTS public.demopdf_bert
(
    id serial,
    pdfpath text ,
    embeddings vector(768),
    summary text 
)

TABLESPACE pg_default;
