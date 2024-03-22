CREATE OR REPLACE FUNCTION insert_embeddings_from_pdf_bert(pdf_dir text)
RETURNS void AS $$
    import os
    import glob
    import pdfplumber
    import torch
    from sentence_transformers import SentenceTransformer
    from transformers import BartTokenizer, BartForConditionalGeneration
    import time

    # Ensure PyTorch uses only CPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    torch.set_num_threads(1)
    device = "cpu"

    # Initialize the Sentence Transformer model for embeddings
    if 'model' not in SD:
        SD['model'] = SentenceTransformer('all-distilroberta-v1').to(device)
        plpy.notice("Sentence Transformer Model Loaded")
    embedding_model = SD['model']

    # Initialize the BART model for summarization
    if 'summary_model' not in SD or 'summary_tokenizer' not in SD:
        SD['summary_tokenizer'] = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        SD['summary_model'] = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(device)
        plpy.notice("BART Model and Tokenizer for Summarization Loaded")
    summary_tokenizer = SD['summary_tokenizer']
    summary_model = SD['summary_model']

    # Find all PDF files in the specified directory
    pdf_paths = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    plpy.notice(f"Found {len(pdf_paths)} PDF files")

    # Process each PDF
    for pdf_path in pdf_paths:
        file_start_time = time.time()

        # Extract text from PDF
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            text_extraction_time = time.time() - file_start_time
            plpy.notice(f"Text extraction for {pdf_path} took {text_extraction_time:.2f} seconds")
        except Exception as e:
            plpy.warning(f"Error processing {pdf_path}: {str(e)}")
            continue

        # Generate embedding for the text
        start_embedding_time = time.time()
        embedding = embedding_model.encode([full_text])[0]  # Process a single document
        embedding_generation_time = time.time() - start_embedding_time
        plpy.notice(f"Embedding generation for {pdf_path} took {embedding_generation_time:.2f} seconds")

        # Generate summary for the text
        start_summary_time = time.time()
        inputs = summary_tokenizer.encode("summarize: " + full_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summary_model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = summary_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary_generation_time = time.time() - start_summary_time
        plpy.notice(f"Summary generation for {pdf_path} took {summary_generation_time:.2f} seconds")

        # Insert PDF path, embedding, and summary into the database
        start_insert_time = time.time()
        plan = plpy.prepare("INSERT INTO public.demopdf_bert(pdfpath, embeddings, summary) VALUES ($1, $2::vector, $3)", ["text", "vector", "text"])
        plpy.execute(plan, [pdf_path, list(embedding), summary])
        insert_time = time.time() - start_insert_time
        plpy.notice(f"Insert operation for {pdf_path} took {insert_time:.2f} seconds")

        # Calculate and log the total time for processing the current PDF
        total_file_time = time.time() - file_start_time
        plpy.notice(f"Total processing time for {pdf_path} was {total_file_time:.2f} seconds")
$$ LANGUAGE plpython3u;
