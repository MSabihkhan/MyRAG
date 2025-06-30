from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from sentence_transformers import SentenceTransformer
from llama_index.core  import Settings
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
llm = None
# 2️⃣ Initialize Google LLM (Gemini)
def add_api_key(gemini_api_key):
    os.environ['GOOGLE_API_KEY'] = gemini_api_key
    llm = GoogleGenAI(model="gemini-2.0-flash")
    Settings.llm = llm
# 3️⃣ Initialize Google GenAI-based embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5", device="cpu")

# 4️⃣ Apply global Settings (optional)
Settings.llm = llm
Settings.embed_model = embed_model
