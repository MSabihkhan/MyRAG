import streamlit as st
from ingestion.loader import load_docs, save_uploaded_files, load_user_docs
from ingestion.pipeline import run_pipeline
from Vectorstore.index import buildindexandvectorstore
from chat.engine import create_chat_engine
from config.settings import add_api_key
import os
import nest_asyncio
nest_asyncio.apply()

# Modified setup function to handle API keys
def setup(file_paths=None, gemini_api_key=None):
    try:
        # Set API key if provided
        if gemini_api_key:
            add_api_key(gemini_api_key)
        
        if file_paths is None:
            docs = load_docs()
        else:
            docs = load_user_docs(file_paths)
            
        nodes = run_pipeline(docs)
        index = buildindexandvectorstore(nodes)
        
        # Pass API key to chat engine creation
        chat_engine = create_chat_engine(index)
        
        st.session_state.chat_engine = chat_engine
        st.session_state.messages = []
        st.session_state.docs_loaded = True
        st.success("✅ All set! Start chatting.")
    except Exception as e:
        st.error(f"Failed to process: {e}")
        st.session_state.docs_loaded = False

# Page config
st.set_page_config(
    page_title="Modular RAG Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state init
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

# Header
st.title("🧠 Modular RAG Chatbot")
st.markdown("Upload documents → Process pipeline → Start chatting.")

# Sidebar for actions
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # Gemini API key section
    api_key = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        value=st.session_state.gemini_api_key,
        help="Get your API key from: https://aistudio.google.com/app/apikey"
    )
    
    # Save API key to session state when changed
    if api_key != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = api_key
        # Clear chat engine when key changes
        if "chat_engine" in st.session_state:
            del st.session_state.chat_engine
        st.session_state.docs_loaded = False
        st.rerun()
    
    st.header("📄 Document Handling")
    
    # Document processing button
    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True,
        help="Upload PDF, TXT, or DOCX files to chat with"
    )
    
    # Show uploaded files
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        with st.expander("📋 Uploaded Files"):
            for file in uploaded_files:
                st.write(f"• **{file.name}** ({file.size:,} bytes)")
    

    process_btn = st.button("🚀 Process Uploads", 
                            disabled=len(uploaded_files)==0,
                            type="primary")
    # Process uploaded files
    if process_btn and uploaded_files:
        with st.spinner("Processing documents..."):
            temp_dir, file_paths = save_uploaded_files(uploaded_files)
            setup(file_paths=file_paths, gemini_api_key=st.session_state.gemini_api_key)

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []

# Chat UI
if st.session_state.docs_loaded:
    for msg in st.session_state.messages:
        role = "🤖 Assistant:" if msg["role"] == "assistant" else "👤 You:"
        st.markdown(f"**{role}** {msg['content']}")

    if prompt := st.chat_input("Ask something from your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_engine.chat(prompt)
                response_text = str(response)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.markdown(f"**🤖 Assistant:** {response_text}")
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.error(error_msg)
else:
    if not st.session_state.gemini_api_key:
        st.warning("⚠️ Please enter a Gemini API key in the sidebar")
    else:
        st.info("⚠️ Upload documents and click 'Process Uploads' or load default documents")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using LlamaIndex modules.")