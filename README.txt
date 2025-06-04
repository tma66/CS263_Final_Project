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
During the first phase of our approach, we want to evaluate LLM's abilities for detecting vulnerabilities, with and without guidance. Dataset comes from OWASP and contains 110 test cases, stored under `detection/benchmark`

    cd detection/open_llm # if evaluating open source models

Evaluate without guidance

    python3 evaluate_general.py

Evaluate with guidance

    python3 evaluate_specific.py