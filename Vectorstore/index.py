from llama_index.core import VectorStoreIndex,StorageContext
from config.settings import embed_model
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

def buildindexandvectorstore(all_nodes):
    index = VectorStoreIndex(all_nodes,embed_model=embed_model )
    
    # db = chromadb.PersistentClient(path ="./chromadb")
    
    # chroma_collection = db.get_or_create_collection("quickstart")
    
    # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return index
