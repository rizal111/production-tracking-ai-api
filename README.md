<div align="center">
  <h1 align="center">Production Tracking RAG AI API</h1>
  <p align="center">
    Python API server for Retrieval-Augmented Generation (RAG) LlamaIndex with <a href="https://platform.openai.com/docs/models/gpt-4.1-mini">OpenAI Platform GPT-4.1-mini</a> over MySQL for Project Production Tracking.
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Web App</a>
  </p>
</div>

### Built With

<div align="center">
    <a href="https://docs.llamaindex.ai">
        <img src="https://www.llamaindex.ai/llamaindex.svg" alt="Next.js" width="200" height="100" />
    </a>
    <p align="center">
    LlamaIndex is Opensource RAG framework for building LLM-powered agents over data</p>
</div>

### Installation

Python Dependency
 ```sh
   pip install --no-cache-dir -r requirements.txt
   ```

### Running Dev

 ```sh
   fastapi dev main.py
   ```

### Deploying 

 ```sh
   uvicorn main:app --host 0.0.0.0 --port 80
   ```