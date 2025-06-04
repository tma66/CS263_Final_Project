from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import logging
import langchain
import os
import csv
import re
from tqdm import tqdm
import csv

langchain.debug = False

logging.basicConfig()
logging.getLogger("langchain.codellama").setLevel(logging.INFO)
LLAMA_MODEL = "qwen2.5-coder:32b"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JAVA_DIRECTORY = os.path.join(BASE_DIR, "..", "benchmark")
OUTPUT_FILE = os.path.join(BASE_DIR, "security_report.txt")
GROUND_TRUTH_FILE = os.path.join(JAVA_DIRECTORY, "ground_truth.csv")


def csv_to_dict(filepath):
    result = {}
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                result[key] = value
    return result


def extract_cwe_items(response_text):
    """
    Extracts CWE number and title pairs from a plain-text response.
    """
    pattern = r"(CWE-\d+):\s*(.+)"
    return re.findall(pattern, response_text)


def analyze_java_files(java_dir, output_csv_path, chain):
    ground_truth = csv_to_dict(GROUND_TRUTH_FILE)
    print(f"Ground truth loaded: {len(ground_truth)} items")

    with open(output_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "CWE Number", "CWE Title"])

        for root, _, files in os.walk(java_dir):
            java_files = [file for file in files if file.endswith(".java")]
            for file in tqdm(java_files, desc=f"Analyzing files in {root}"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        code = f.read()

                    print(f"\nAnalyzing: {file}")
                    filename = os.path.splitext(file)[0]
                    ground_truth_value = ground_truth.get(filename, "None")
                    response = chain.invoke(
                        {
                            "cwe": ground_truth_value,
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
            "You are a static analysis tool. Review the following code for the following CWE vulnerability: CWE-{cwe}. This CWE may or may not exist in the code.\n"
            "If the CWE exists, return **only** the CWE number and title in the format:\n"
            "CWE-<number>: <title>\n"
            "Example:\nCWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')\n\n"
            "OR if the CWE does not exist, return **only** None instead\n\n"
            "Example:\nNone\n\n"
            "Do not add any other explanations or comments. Do not return None with a CWE\n\n",
        ),
        ("human", "{code}"),
    ]
)

chain = prompt | ollama_llm

analyze_java_files(JAVA_DIRECTORY, OUTPUT_FILE, chain)
