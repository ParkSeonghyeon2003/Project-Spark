from langchain_openai import ChatOpenAI
from config import settings

def get_llm(schema=None):
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.TEMPERATURE,
        streaming=True
    )

    if schema:
        return llm.with_structured_output(schema)
    
    return llm