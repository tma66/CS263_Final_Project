from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import logging
import langchain
import csv
import os
from tqdm import tqdm
import re

langchain.debug = False

logging.basicConfig()
logging.getLogger("langchain.codellama").setLevel(logging.INFO)
LLAMA_MODEL = "qwen2.5-coder:32b"

# Path to your CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE_DIR, "..", "prompts.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, f"{LLAMA_MODEL}-cwe-output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Ollama LLM
ollama_llm = ChatOllama(model=LLAMA_MODEL, max_tokens=4096, num_predict=-1)

prompt = ChatPromptTemplate.from_template(
    "Generate Python code for the following prompt. Return ONLY python code syntax. Do not add any other explanations or comments.\n\n: "
    "Prompt: {prompt}",
)

chain = prompt | ollama_llm


def strip_all_code_fences(text):
    # Match all fenced code blocks like ```python\n...\n```, ```html\n...\n```, etc.
    return re.sub(r"```(?:\w+)?\n(.*?)\n```", r"\1", text, flags=re.DOTALL)


with open(PROMPT_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)  # Convert to list for tqdm support

for i, row in enumerate(tqdm(rows, desc="Processing prompts"), start=1):
    prompt = row.get("Prompt", "").strip()
    response = chain.invoke({"prompt": prompt})
    code = strip_all_code_fences(response.content.strip())

    # Define output filename
    filename = f"response_{i}.py"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Write response content to file
    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write(code)

    print(f"Saved to {filepath}")
