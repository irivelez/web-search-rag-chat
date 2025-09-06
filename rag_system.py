from openai import OpenAI
from vector_store import VectorStore
from pdf_processor import PDFProcessor
from web_search import WebSearcher
import os
from dotenv import load_dotenv

load_dotenv()

class RAGSystem:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vector_store = VectorStore()
        self.pdf_processor = PDFProcessor()
        self.web_searcher = WebSearcher()
    
    def add_pdf(self, pdf_path: str, pdf_name: str = None):
        """Process and add PDF to the knowledge base"""
        if pdf_name is None:
            pdf_name = os.path.basename(pdf_path)
        
        chunks = self.pdf_processor.process_pdf(pdf_path)
        self.vector_store.add_documents(chunks, pdf_name)
        return len(chunks)
    
    def query(self, question: str, use_web_search: bool = False) -> tuple[str, list[str]]:
        """Query the RAG system with a question"""
        relevant_docs = self.vector_store.similarity_search(question, n_results=5)
        
        if not relevant_docs and not use_web_search:
            return "I don't have any relevant documents to answer your question. Please upload some PDFs first.", []
        
        context_parts = []
        sources = []
        
        if relevant_docs:
            pdf_context = "\n\n".join([doc["content"] for doc in relevant_docs])
            context_parts.append(f"PDF Documents Context:\n{pdf_context}")
            pdf_sources = list(set([doc["metadata"]["source"] for doc in relevant_docs]))
            sources.extend(pdf_sources)
        
        if use_web_search:
            web_results = self.web_searcher.search(question)
            if web_results:
                print(f"💡 Using {len(web_results)} web results for context")
                web_context = self.web_searcher.format_search_results(web_results)
                context_parts.append(f"Current Web Information:\n{web_context}")
                sources.append("Web Search")
            else:
                print("⚠️ No web results found or web search failed")
        
        if not context_parts:
            return "I don't have enough information to answer your question. Please upload some PDFs or enable web search.", []
        
        full_context = "\n\n" + "="*50 + "\n\n".join(context_parts)
        
        prompt = f"""Based on the following context, please answer the question comprehensively.

{full_context}

Question: {question}

Please provide a detailed answer based on the available context. If you're using information from multiple sources, please integrate them thoughtfully. If the context doesn't contain enough information to fully answer the question, please state what information is available and what might be missing.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content, sources
    
    def get_loaded_documents(self):
        """Get list of loaded documents"""
        return self.vector_store.get_all_documents()
    
    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base"""
        self.vector_store.clear_collection()