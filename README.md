# Web Search + RAG Chat

Chat with your PDFs and get answers enhanced with real-time web search

## 🎯 What It Does

Upload PDF documents and ask questions. The system searches your documents AND the web simultaneously, giving you answers that combine historical knowledge with up-to-date information. 
Perfect for research, due diligence, or staying current on any topic.

## 🛠️ Tech Stack

**Backend:**
- **Python** - Core application language
- **OpenAI API** (v1.54.0) - Embeddings (text-embedding-ada-002) & Chat (gpt-3.5-turbo)
- **ChromaDB** (v0.4.15) - Local vector database
- **Serper.dev API** - Web search functionality
- **PyMuPDF** - PDF text extraction
- **httpx** (v0.27.0) - HTTP client for API calls

**Frontend:**
- **Streamlit** - Interactive web interface

## 🚀 Quick Start

```bash

# 1. Clobe & Install dependencies:
git clone https://github.com/irivelez/web-search-rag-chat.git
cd web-search-rag-chat
pip install -r requirements.txt


# 2. Configure API keys in `.env`:

OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here


# 3. Run the application:

streamlit run app.py
```

Open http://localhost:8501 and start chatting!


## 📁 File Structure

- `app.py` - Main Streamlit application with UI and chat logic
- `rag_system.py` - Enhanced RAG orchestration with hybrid search
- `vector_store.py` - ChromaDB vector storage and similarity search
- `pdf_processor.py` - PDF text extraction and intelligent chunking
- `web_search.py` - Serper.dev API integration with logging
- `requirements.txt` - Python dependencies
- `.env` - API key configuration

## 💡 Why This Exists
Someone in my LinkedIn audience asked: "Un RAG con alguna db de vectores, con patrón sencillo" This is the answwer - a hybrid RAG system that never gets outdated.

## 🔍 How It Works

1. **PDF Processing**: Documents are extracted, cleaned, and chunked for optimal retrieval
2. **Vector Storage**: Text chunks are embedded and stored in local ChromaDB
3. **Hybrid Search**: User queries trigger both PDF similarity search and web search
4. **Context Fusion**: Relevant PDF chunks and web results are combined intelligently
5. **AI Response**: OpenAI generates comprehensive answers using combined context
6. **Source Attribution**: Users see exactly which sources contributed to the response

---
⚡️ Built in 3 hours • Part of https://thexperiment.dev/
