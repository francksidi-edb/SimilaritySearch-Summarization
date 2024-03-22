from sentence_transformers import SentenceTransformer

# Define a sample piece of text
sample_text = "This is a test sentence for encoding."

# Load the Sentence Transformer model
model_name = "all-distilroberta-v1"
print(f"Loading model '{model_name}'...")
model = SentenceTransformer(model_name)

# Generate embeddings for the sample text
print("Generating embeddings...")
embeddings = model.encode([sample_text])

# Print the generated embeddings
print("Embeddings generated:")
print(embeddings)

# Determine and print the size (dimensionality) of the embeddings vector
vector_size = embeddings.shape[1]  # Embeddings shape is (num_samples, vector_size)
print(f"The size (dimensionality) of the embeddings vector is: {vector_size}")
