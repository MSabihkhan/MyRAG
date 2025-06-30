from ingestion.loader import load_docs
from ingestion.pipeline import run_pipeline
from Vectorstore.index import buildindexandvectorstore
from chat.engine import create_chat_engine
docs = load_docs()
nodes = run_pipeline(docs)
index = buildindexandvectorstore(nodes)
chat_engine = create_chat_engine(index)

while True:
    user_input = input("User: ")
    response = chat_engine.chat(user_input)
    print("Bot:", response.response)
    print("*************************")