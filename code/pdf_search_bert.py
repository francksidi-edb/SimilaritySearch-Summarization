import streamlit as st
import psycopg2
from PIL import Image
import cv2
import numpy as np
import io
import time


# Custom Header Section
logo_path = "logo.svg"
primary_color = "#FF4B33"
background_color = "#FFFFFF"

header_css = f"""
<style>
.header {{
    background-color: {background_color};
    padding: 10px;
    color: white;
}}
a {{
    color: {primary_color};
    padding: 0 16px;
    text-decoration: none;
    font-size: 16px;
}}
</style>
"""

st.markdown(header_css, unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])

with col1:
    st.image(logo_path, width=150)

with col2:
    st.markdown(f"""
    <div class="header">
        <a href="#" target="_blank">Products</a>
        <a href="#" target="_blank">Solutions</a>
        <a href="#" target="_blank">Resources</a>
        <a href="#" target="_blank">Company</a>
    </div>
    """, unsafe_allow_html=True)

# Streamlit UI for Image Similarity Search
st.title('PDF Search')
st.markdown("## Powered by EDB Postgresql and Pgvector")
st.markdown("## Using all-distilroberta-v1 model")



# Initialize session_state.search_text if not already set
if 'search_text' not in st.session_state:
    st.session_state['search_text'] = ""

# Define the create_db_connection function
def create_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost"
    )

# Define the run_queries function
def run_queries(search_text):
    conn = st.session_state.db_conn
    cur = conn.cursor()
    pdf_links = []

    try:
        # Assuming 'public.get_embedding_bert_f' returns a vector used for further queries
        start_time = time.time()

        cur.execute("SELECT public.get_embedding_bert_f(%s);", (search_text,))
        vector_result = cur.fetchone()[0]

        vector_time = time.time() - start_time
        st.write(f"Fetching vector took {vector_time:.4f} seconds.")

        start_time = time.time()


        # Execute the main query to find PDFs based on the vector
        query = """
        SELECT id, pdfpath, summary, 1 - (embeddings <=> %s::vector) as similarity
        FROM public.demopdf_bert
        ORDER BY similarity DESC
        LIMIT 5;
        """
        cur.execute(query, (vector_result,))
        results = cur.fetchall()

        # Assuming pdf_links should contain tuples of (id, pdfpath, similarity)
        pdf_links = [(result[1], result[2], result[3]) for result in results]

        query_time = time.time() - start_time
        st.write(f"Searching pdf took {query_time:.4f} seconds.")

    except Exception as e:
        st.error("An error occurred: " + str(e))
    finally:
        cur.close()
    return pdf_links

# Ensure DB connection is set in session_state
if 'db_conn' not in st.session_state or st.session_state.db_conn.closed:
    st.session_state.db_conn = create_db_connection()

# Streamlit UI setup for PDF search
search_text = st.text_input("Enter text to search for PDF:", key='search_text')

# Search button functionality

if st.button('Search'):
    if st.session_state.search_text:
        pdf_links = run_queries(st.session_state.search_text)
        num_pdfs = len(pdf_links)
        if num_pdfs > 0:
            st.success(f"Found {num_pdfs} PDF{'s' if num_pdfs > 1 else ''}:")
            for id, (pdfpath, summary, similarity) in enumerate(pdf_links):
                # Present the file path as text and instruct users on how to use it
                #st.markdown(f"**ID:** {id+1}, **PdfPath:** `{pdfpath}`, **Similarity:** {similarity}")
                #st.text(f"ID: {id+1}, PdfPath: {pdfpath}, Similarity: {similarity}")
                #st.text("Copy the path above and open it with your PDF reader.")
                st.markdown(f"**ID:** {id+1}")
                st.markdown(f"**Summary:** {summary}")
                st.markdown(f"**PdfPath:** [Example PDF]({pdfpath})")
                st.markdown(f"**Similarity:** {similarity}")
                st.markdown("Copy the path above and open it with your PDF reader.")
        else:
            st.error("No matching PDFs found.")
    else:
        st.error("Please enter some text to search for.")


