from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import logging
import langchain
from langchain.chains import LLMChain

langchain.debug = True

logging.basicConfig()
logging.getLogger("langchain.codellama").setLevel(logging.DEBUG)
LLAMA_MODEL = "codellama"


# Initialize the vector db and Ollama LLM
ollama_llm = Ollama(model=LLAMA_MODEL)

# RAG prompt
template = """Write a Python function to {task}. Return just the python code and nothing else.
"""

prompt = PromptTemplate(
    input_variables=["task"],
    template=template,
)

task = "Calculate sqrt of pi"

# Create the RunnableSequence
chain = LLMChain(llm=ollama_llm, prompt=prompt)

response = chain.invoke({"task": task})
print(response["text"])
