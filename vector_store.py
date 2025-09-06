import chromadb
from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = "pdf_documents"
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "PDF document chunks"}
        )
    
    def add_documents(self, chunks: List[str], pdf_name: str):
        """Add document chunks to vector store"""
        embeddings = []
        for chunk in chunks:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=chunk
            )
            embeddings.append(response.data[0].embedding)
        
        ids = [f"{pdf_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": pdf_name, "chunk_index": i} for i in range(len(chunks))]
        
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
    
    def similarity_search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar documents"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_embedding = response.data[0].embedding
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
    
    def get_all_documents(self) -> List[str]:
        """Get list of all processed documents"""
        results = self.collection.get()
        sources = set()
        for metadata in results["metadatas"]:
            sources.add(metadata["source"])
        return list(sources)
    
    def clear_collection(self):
        """Clear all documents from collection"""
        self.chroma_client.delete_collection(self.collection_name)
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "PDF document chunks"}
        )