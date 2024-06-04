import streamlit as st
import os
import psycopg2
from PIL import Image
import time
import ast

# Streamlit page configuration
st.set_page_config(
    page_title="Text Search with EDB Postgres",
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
logo_path = "edb_new.png"
display_header(logo_path)

# Main App Title
st.title('Text Search')
st.markdown("### Powered by EDB Postgresql and PGAI extension", unsafe_allow_html=True)

# Database Connection
@st.cache_resource
def create_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="localhost",
        port = 15432
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
    conn.autocommit = True  # Enable autocommit for creating the database
    with conn.cursor() as cur:
        pdf_links = []
        try:
            

            cur.execute(f"""SELECT data from pgai.retrieve('{search_text}', 2, 'txt_embeddings_dynamic');""")
            results = cur.fetchall()

            pdf_links = [result[0] for result in results]
        except Exception as e:
            st.error("An error occurred: " + str(e))
    return pdf_links

# UI for PDF Search
st.session_state.search_text = st.text_input("Enter text to search in files:",
                                             value=st.session_state.search_text,
                                             help="Type the content you're looking for in a txt file.")

# Search Functionality
if st.button('Search') or st.session_state.search_text:
    if st.session_state.search_text:
        with st.spinner("Searching PDFs..."):
            st.session_state.search_results = run_queries(st.session_state.search_text)
        if st.session_state.search_results:
            for id, text_info in enumerate(st.session_state.search_results, start=1):
                text_info_j = ast.literal_eval(text_info)["text_id"]
                st.markdown(f"**ID:** {id} | **Text Name:** {text_info_j}")
        else:
            st.error("No matching PDFs found.")
    else:
        st.error("Please enter some text to search for.")



