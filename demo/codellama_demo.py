from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import logging
import langchain
from langchain.chains import LLMChain
import os
import csv
import re

langchain.debug = True

logging.basicConfig()
logging.getLogger("langchain.codellama").setLevel(logging.DEBUG)
LLAMA_MODEL = "qwen2.5-coder:32b"
JAVA_DIRECTORY = (
    "/Users/tulingma/Documents/School/UCLA/263/project/CS263_Final_Project/testcode3"
)
OUTPUT_FILE = "/Users/tulingma/Documents/School/UCLA/263/project/CS263_Final_Project/security_report.txt"


def extract_cwe_items(response_text):
    """
    Extracts CWE number and title pairs from a plain-text response.
    """
    pattern = r"(CWE-\d+):\s*(.+)"
    return re.findall(pattern, response_text)


def analyze_java_files(java_dir, output_csv_path):
    results = []

    with open(output_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "CWE Number", "CWE Title"])

        for root, _, files in os.walk(java_dir):
            for file in files:
                if file.endswith(".java"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        code = f.read()

                    print(f"Analyzing: {file}")
                    try:
                        response = chain.run({"code": code})
                        print(f"Response: {response}")
                        cwe_items = extract_cwe_items(response)

                        if cwe_items:
                            for number, title in cwe_items:
                                writer.writerow([file, number, title])
                        else:
                            writer.writerow([file, "None", "No security issues found"])

                    except Exception as e:
                        print(f"ERROR analyzing {file}: {e}")

    print(f"\n✅ CSV report saved to: {output_csv_path}")


# Initialize the vector db and Ollama LLM
ollama_llm = Ollama(model=LLAMA_MODEL)

# Prompt template for security analysis
prompt = PromptTemplate(
    input_variables=["code"],
    template=(
        "Review the attached code and identify any potential security issues. There may or may not be any security issues in the code. If there is an issue, return the CWE number. Do not report theoretical or non-impactful CWEs. Return only the CWE number and title.\n\n"
        "Code:\n{code}\n\n"
    ),
)

# Create the RunnableSequence
chain = LLMChain(llm=ollama_llm, prompt=prompt)

analyze_java_files(JAVA_DIRECTORY, OUTPUT_FILE)
