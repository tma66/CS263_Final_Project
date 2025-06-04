from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import logging
import langchain
import os
import csv
import re
from tqdm import tqdm

langchain.debug = False

logging.basicConfig()
logging.getLogger("langchain.codellama").setLevel(logging.INFO)
LLAMA_MODEL = "qwen2.5-coder:32b"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JAVA_DIRECTORY = os.path.join(BASE_DIR, "..", "benchmark")
OUTPUT_FILE = os.path.join(BASE_DIR, "security_report.txt")


def extract_cwe_items(response_text):
    """
    Extracts CWE number and title pairs from a plain-text response.
    """
    pattern = r"(CWE-\d+):\s*(.+)"
    return re.findall(pattern, response_text)


def analyze_java_files(java_dir, output_csv_path, chain):
    with open(output_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "CWE Number", "CWE Title"])

        for root, _, files in os.walk(java_dir):
            code_files = [file for file in files if file.endswith((".py", ".java"))]
            for file in tqdm(code_files, desc=f"Analyzing files in {root}"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        code = f.read()

                    print(f"\nAnalyzing: {file}")
                    response = chain.invoke(
                        {
                            "code": code,
                        }
                    )
                    print(f"Response: {response}")
                    cwe_items = extract_cwe_items(response.content)

                    if cwe_items:
                        for number, title in cwe_items:
                            writer.writerow([file, number, title])
                    else:
                        writer.writerow([file, "None", "No security issues found"])

                except Exception as e:
                    print(f"ERROR analyzing {file}: {e}")

    print(f"\n✅ CSV report saved to: {output_csv_path}")


# Initialize the vector db and Ollama LLM
ollama_llm = ChatOllama(model=LLAMA_MODEL)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a static analysis tool. Review the following code for real, impactful security vulnerabilities. There may or may not be any security issues in the code.\n"
            "If you find a security issue, return **only** the CWE number and title in the format:\n"
            "CWE-<number>: <title>\n"
            "Example:\nCWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')\n\n"
            "OR if no vulnerabilities are found, return **only** None instead\n\n"
            "Example:\nNone\n\n"
            "Do not add any other explanations or comments. Do not return None with a CWE\n\n",
        ),
        ("human", "{code}"),
    ]
)

chain = prompt | ollama_llm

analyze_java_files(JAVA_DIRECTORY, OUTPUT_FILE, chain)
