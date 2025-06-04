## Setup

Create new `venv`

    python3 -m venv venv

Activate `venv`

    source venv/bin/activate

Install requirements

    pip install -r requirements.txt

Download and setup LLM server. Download and install ollama from https://ollama.com. Note this tool is used to pull open source models

    ollama pull qwen2.5-coder:32b 

## Detecting Secure Code
During the first phase of our approach, we want to evaluate LLM's abilities for detecting vulnerabilities, with and without guidance. Dataset comes from OWASP and contains 110 test cases, stored under `detection/benchmark`.

    cd detection/open_llm # if evaluating open source models

### Evaluate without guidance

    python3 evaluate_general.py

### Evaluate with guidance

    python3 evaluate_specific.py

## Generating Secure Code
During the second phase of our approach, we want to evaluate LLM's abilities to generate secure code based on different scenarios. Scenarios are stored under `generation/prompts.csv` and contain 50 real world scenarios with potential for CWEs if not careful.

    cd generation/open_llm # if evaluating open source models

### Generate code

    python3 generate.py

### Evaluate with Bandit

    bandit --severity-level all -r qwen2.5-coder-32b-cwe-output # if evaluating qwen. change llm model as necessary

### Evaluate with CodeQL
CodeQL CLI needs to be first installed. The instructions can be found [here](https://codeql.github.com/docs/codeql-cli/getting-started-with-the-codeql-cli/). 

#### Usage of DB Creation Scripts
Create CodeQL databases by invoking the provided shell script.
The first parameter is the path to the source root of the files generated from LLM.
The second parameter is the name the created db should be given. It will be created in the folder the script is executed in.

##### Example

`sh create_db_python.sh ~/qwen2.5-coder-32b-cwe-output python_llm_db`


#### Usage of DB Analysis Scripts
The script for analysis of CodeQL database by invoking separate script.
The first parameter is the name of the query set to be executed.
The second parameter is the path to the database.
The third parameter is the output path for the results.

The results will be printed in csv format.

##### Example 

`sh analyse_db.sh python-security-and-quality.qls python_llm_db ~/results/python_results_sec_extended.csv`