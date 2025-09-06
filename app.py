import streamlit as st
from rag_system import RAGSystem
import tempfile
import os

st.set_page_config(
    page_title="RAG PDF Chat",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG PDF Chat Application")
st.markdown("Upload PDF reports and ask questions about their content!")

@st.cache_resource
def initialize_rag():
    return RAGSystem()

rag = initialize_rag()

with st.sidebar:
    st.header("📄 Document Management")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload PDF reports to analyze"
    )
    
    if uploaded_files:
        if st.button("Process PDFs"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                try:
                    chunks_count = rag.add_pdf(tmp_file_path, uploaded_file.name)
                    st.success(f"✅ {uploaded_file.name}: {chunks_count} chunks processed")
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                finally:
                    os.unlink(tmp_file_path)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("All files processed!")
            st.rerun()
    
    st.divider()
    
    use_web_search = st.checkbox("🌐 Enhanced with Web Search", 
                                help="Include current web information in answers")
    
    st.divider()
    
    loaded_docs = rag.get_loaded_documents()
    if loaded_docs:
        st.subheader("📋 Loaded Documents")
        for doc in loaded_docs:
            st.write(f"• {doc}")
        
        if st.button("🗑️ Clear All Documents"):
            rag.clear_knowledge_base()
            st.success("All documents cleared!")
            st.rerun()
    else:
        st.info("No documents loaded yet. Upload PDFs to get started!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your uploaded documents..."):
    if not rag.get_loaded_documents() and not use_web_search:
        st.warning("Please upload and process some PDFs first, or enable web search!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            search_text = "Searching documents and web" if use_web_search else "Searching documents"
            with st.spinner(f"{search_text} and generating response..."):
                response, sources = rag.query(prompt, use_web_search=use_web_search)
                
                if use_web_search:
                    web_used = "Web Search" in sources
                    print(f"🌐 Web search enabled: {'✅ Used' if web_used else '❌ Not used'}")
            
            st.markdown(response)
            
            if sources:
                source_types = []
                if any(src != "Web Search" for src in sources):
                    source_types.append("📄 PDF")
                if "Web Search" in sources:
                    source_types.append("🌐 Web")
                
                source_indicator = " + ".join(source_types) if source_types else "📄 PDF"
                st.caption(f"**Sources:** {source_indicator}")
        
        st.session_state.messages.append({"role": "assistant", "content": response})