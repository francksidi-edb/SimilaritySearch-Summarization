import argparse
import psycopg2
from PIL import Image


def _create_db_connection():
        """Create and return a database connection."""
        return psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="localhost",
            port = 15432
        )

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("model_name", help="enter the encoder name", type=str)
        parser.add_argument("s3_bucket_name", help="enter your s3 bucket name", type=str)
        args = parser.parse_args()
        conn = _create_db_connection()
        conn.autocommit = True  # Enable autocommit for creating the database

        cursor = conn.cursor()
        cursor.execute("create extension IF NOT EXISTS pgai cascade;")
        cursor.close()
        with conn.cursor() as cur:
                cur.execute(f"""
                        SELECT pgai.create_s3_retriever(
                        'txt_embeddings_dynamic',
                        'public',
                        '{args.model_name}',
                        'text',
                        '{args.s3_bucket_name}',
                        '');""")
                cur.execute("""
                        SELECT pgai.refresh_retriever('txt_embeddings_dynamic');""")
                cur.close

if __name__ == "__main__":
    main()