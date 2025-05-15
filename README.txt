## Setup

Create new `venv`

    python3 -m venv venv

Activate `venv`

    source venv/bin/activate

Install requirements

    pip install -r requirements.txt

Download and setup LLM server. Download and install ollama from https://ollama.com. Note this tool is used to pull open source models

    ollama pull codellama 

## Demos

    cd demo

Example. Run llm demo

    python3 codellama_demo.py
