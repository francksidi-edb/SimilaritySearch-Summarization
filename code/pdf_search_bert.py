import streamlit as st
import os
import psycopg2
from PIL import Image
import time

# Streamlit page configuration
st.set_page_config(
    page_title="PDF Search with EDB Postgres",
    page_icon="🔍",
    layout="wide"
)

# Custom Styling
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section with Custom Styling
def display_header(logo_path):
    with st.container():
        col1, col2 = st.columns([1, 4], gap="small")
        with col1:
            st.image(logo_path, width=150)
        with col2:
            st.markdown("""
                <div style="text-align: right;">
                    <a href="#" target="_blank">Products</a> |
                    <a href="#" target="_blank">Solutions</a> |
                    <a href="#" target="_blank">Resources</a> |
                    <a href="#" target="_blank">Company</a>
                </div>
                """, unsafe_allow_html=True)

# Display the header
logo_path = "logo.svg"
display_header(logo_path)

# Main App Title
st.title('PDF Search')
st.markdown("### Powered by EDB Postgresql and Pgvector", unsafe_allow_html=True)
st.markdown("### Using all-distilroberta-v1 model", unsafe_allow_html=True)

# Database Connection
@st.cache_resource
def create_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost"
    )

# If 'search_text' not in session state, initialize it
if 'search_text' not in st.session_state:
    st.session_state.search_text = ""

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Database Query Execution
def run_queries(search_text):
    """Run the database query based on the search text and return results."""
    conn = create_db_connection()
    with conn.cursor() as cur:
        pdf_links = []
        try:
            cur.execute("SELECT public.get_embedding_bert_f(%s);", (search_text,))
            vector_result = cur.fetchone()[0]

            cur.execute("""
                SELECT id, pdfpath, summary, 1 - (embeddings <=> %s::vector) as similarity
                FROM public.demopdf_bert
                ORDER BY similarity DESC
                LIMIT 5;
                """, (vector_result,))
            results = cur.fetchall()

            pdf_links = [(result[1], result[2], result[3]) for result in results]
        except Exception as e:
            st.error("An error occurred: " + str(e))
    return pdf_links

# UI for PDF Search
st.session_state.search_text = st.text_input("Enter text to search for PDF:",
                                             value=st.session_state.search_text,
                                             help="Type the content you're looking for in a PDF.")

# Search Functionality
if st.button('Search') or st.session_state.search_text:
    if st.session_state.search_text:
        with st.spinner("Searching PDFs..."):
            st.session_state.search_results = run_queries(st.session_state.search_text)
        if st.session_state.search_results:
            for id, (pdfpath, summary, similarity) in enumerate(st.session_state.search_results, start=1):
                st.markdown(f"**ID:** {id} | **Similarity:** {similarity:.2f}")
                st.markdown(f"**Summary:** {summary}")
                
                # Read the PDF file into memory (ensure the path is accessible)
                try:
                    with open(pdfpath, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    # Create a download button
                    st.download_button(label="Download PDF",
                                       data=pdf_bytes,
                                       file_name=os.path.basename(pdfpath),
                                       mime="application/pdf")
                except Exception as e:
                    st.error(f"Failed to load PDF {os.path.basename(pdfpath)}: {e}")
        else:
            st.error("No matching PDFs found.")
    else:
        st.error("Please enter some text to search for.")



