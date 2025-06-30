from llama_index.core.extractors import TitleExtractor,QuestionsAnsweredExtractor
from llama_index.core.node_parser import SentenceSplitter
from config.settings import llm


text_slitter = SentenceSplitter(separator=" ", chunk_size=1024 , chunk_overlap=128)
title_extractor = TitleExtractor(llm=llm , nodes=5)
Questionanswers = QuestionsAnsweredExtractor(llm = llm ,questions=2)
