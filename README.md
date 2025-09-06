# Enhanced RAG PDF Chat Application

A powerful RAG (Retrieval Augmented Generation) application that combines PDF document analysis with real-time web search to provide comprehensive, up-to-date answers.

## 🚀 Key Features

### Core RAG Functionality
- **PDF Upload & Processing**: Drag and drop multiple PDF files with real-time progress tracking
- **Intelligent Text Processing**: Advanced chunking (1000 words, 200-word overlap) and cleaning
- **Vector Storage**: Local ChromaDB with OpenAI embeddings for semantic similarity search
- **Smart Chat Interface**: Streamlit-based UI with persistent conversation history

### 🌐 Enhanced Web Search Integration
- **Hybrid Search**: Combines local PDF knowledge with current web information
- **Real-time Web Search**: Serper.dev API integration for up-to-date information
- **Source Attribution**: Clear indicators showing PDF, Web, or combined sources
- **Debug Logging**: Console output showing actual search results and API calls

### 📊 Advanced Features
- **Document Management**: View loaded documents, clear storage, batch processing
- **Error Handling**: Graceful fallbacks when web search fails
- **Real Source Verification**: Display actual URLs and snippets from web searches
- **Flexible Search Modes**: Toggle between PDF-only and enhanced web search

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
- **Real-time UI** - Progress indicators, status updates, source attribution

## ⚙️ Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API keys in `.env`:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

3. **Run the application:**
```bash
streamlit run app.py
```

## 🔧 Usage

### Basic PDF Chat
1. Upload PDF reports using the sidebar
2. Click "Process PDFs" to index the documents
3. Ask questions about your documents in the chat interface

### Enhanced Web Search
1. Enable "🌐 Enhanced with Web Search" checkbox in the sidebar
2. Ask questions to get answers combining PDF content with current web information
3. Monitor console output to see actual web search results and sources

### Debug & Verification
- **Console Logging**: Watch terminal for detailed search operation logs
- **Source Attribution**: See which sources (PDF/Web) contributed to each answer
- **Real URLs**: View actual web sources found by the search API

## 📁 File Structure

- `app.py` - Main Streamlit application with UI and chat logic
- `rag_system.py` - Enhanced RAG orchestration with hybrid search
- `vector_store.py` - ChromaDB vector storage and similarity search
- `pdf_processor.py` - PDF text extraction and intelligent chunking
- `web_search.py` - Serper.dev API integration with logging
- `requirements.txt` - Python dependencies
- `.env` - API key configuration

## 🔍 How It Works

1. **PDF Processing**: Documents are extracted, cleaned, and chunked for optimal retrieval
2. **Vector Storage**: Text chunks are embedded and stored in local ChromaDB
3. **Hybrid Search**: User queries trigger both PDF similarity search and web search
4. **Context Fusion**: Relevant PDF chunks and web results are combined intelligently
5. **AI Response**: OpenAI generates comprehensive answers using combined context
6. **Source Attribution**: Users see exactly which sources contributed to the response

## 💡 Benefits

- **Comprehensive Answers**: Combines historical PDF knowledge with current information
- **Source Transparency**: Always know where information comes from
- **Flexible Usage**: Works with PDF-only or enhanced web search modes
- **Cost Effective**: Uses efficient APIs (Serper.dev at $0.30/1000 queries)
- **Local Storage**: Your documents stay private in local vector database