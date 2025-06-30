from llama_index.core.ingestion import IngestionPipeline
from ingestion.transformers import text_slitter , title_extractor,Questionanswers
import time

pipeline = IngestionPipeline(
    transformations=[
        text_slitter,
        title_extractor,
        Questionanswers
        ]
    )

def run_pipeline(docs):
    all_nodes = []
    for i, doc in enumerate(docs):
        print(f"📄 Processing document {i + 1}/{len(docs)}")
        nodes = pipeline.run(documents=[doc], in_place=True, show_progress=True)
        all_nodes.extend(nodes)
        time.sleep(30) 
    print("Document Processing done")
    time.sleep(10)
    time.sleep(30)
    return all_nodes
