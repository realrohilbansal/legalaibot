import faiss
import numpy as np
import os

def load_vector_db(db_path, embeddings, data=None):
    # Check if the vector database file exists
    if os.path.exists(db_path):
        # Load the FAISS index
        index = faiss.read_index(db_path)
    else:
        # Create the FAISS index if it doesn't exist
        if data is None:
            raise ValueError("Data must be provided to create the vector database.")
        index = create_vector_db(embeddings, data, db_path)
    return index

def save_vector_db(vector_db, db_path):
    # Save the FAISS index
    faiss.write_index(vector_db, db_path)

def create_vector_db(embeddings, data, db_path):
    # Assuming `data` is a list of texts
    vectors = embeddings.embed_documents(data)
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    faiss.write_index(index, db_path)
    return index
