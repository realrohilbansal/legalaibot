from langchain.embeddings import OpenAIEmbeddings
import os

def get_openai_embeddings(key):
    return OpenAIEmbeddings(model="text-embedding-ada-002", api_key=key)
