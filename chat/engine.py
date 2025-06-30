from llama_index.core.memory import ChatMemoryBuffer
from config.settings import llm


def create_chat_engine(index):
    memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt="You are an AI assistant with access to a knowledge base. "
                "Use the retrieved context to answer questions accurately. "
                "Remember our conversation history to provide coherent responses."
    )
    return chat_engine
