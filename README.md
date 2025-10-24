# Chanakya — Legal Help AI Bot

Chanakya is an experimental AI-powered legal assistant built as a collection of Jupyter notebooks and supporting code. It’s designed to demonstrate approaches for ingesting legal documents, building retrieval components (RAG), and answering user questions with context-aware responses. The project is notebook-first so you can inspect, experiment, and iterate quickly.

> Note: This repository appears to be notebook-heavy. The README below is written to help researchers, developers, and contributors get started with the typical workflow used for notebook based AI projects. Adjust environment and dependency commands to match the repository's actual files.

Table of contents
- About
- Features
- Quick demo
- Requirements
- Installation
- Configuration / Environment variables
- Typical workflow (how to run the notebooks)
- Architecture & components
- Data, privacy & legal disclaimer
- Contributing
- License
- Acknowledgements & References

About
-----
Chanakya (the "legal help AI bot") is intended to showcase how to:
- Ingest legal text (statutes, case law, contracts).
- Create embeddings and vector stores for retrieval.
- Use a large language model (LLM) to produce concise, contextualized answers with sources.
- Prototype pipelines inside Jupyter notebooks so each step is transparent and reproducible.

Features
--------
- Notebook-based demonstrations for data ingestion, embedding creation, and question-answering (RAG).
- Example code for connecting to hosted LLMs (OpenAI, Anthropic, etc.) and/or running local transformer models.
- Utilities for chunking documents, building/ querying a vector database (FAISS, Pinecone, Weaviate placeholders).
- Example prompts and evaluation snippets to check answer fidelity and source attribution.

Quick demo
----------
1. Create and activate a Python environment (recommended).
2. Install dependencies (see Requirements).
3. Set required environment variables (API keys).
4. Launch Jupyter Notebook / Lab:
   - jupyter lab
   - Open the notebook named something like `01_ingest_and_index.ipynb`, run cells to index sample documents.
   - Open the RAG / QA notebook (e.g., `02_query_bot.ipynb`) and run queries against the index.

Requirements
------------
- Python 3.8+ (3.10+ recommended)
- Jupyter Notebook or JupyterLab
- Basic libraries (examples below — adapt for actual repo):
  - pip install jupyterlab ipykernel pandas numpy tqdm
  - pip install sentence-transformers transformers faiss-cpu
  - pip install langchain openai tiktoken  # if using OpenAI + LangChain
  - pip install pinecone-client  # optional if using Pinecone
  - pip install weaviate-client  # optional
- Reasonable RAM / disk for embeddings and any local model files.

Installation
------------
Recommended: create an isolated virtual environment.

- Using venv
  python -m venv .venv
  source .venv/bin/activate    # macOS / Linux
  .venv\Scripts\activate       # Windows
  pip install --upgrade pip
  pip install -r requirements.txt

- If you don't have a `requirements.txt`, install the common packages listed under Requirements.

Configuration / Environment variables
-------------------------------------
Create a `.env` file or set environment variables in your shell. Typical variables used by notebooks in RAG projects:

- OPENAI_API_KEY=sk-...
- HUGGINGFACE_API_KEY=hf_...
- PINECONE_API_KEY=...
- PINECONE_ENV=...
- PINECONE_INDEX=...
- WEAVIATE_URL=...
- LOCAL_EMBEDDING_MODEL=/path/to/embedding/model
- LOCAL_LLM_MODEL=/path/to/llm/model

Keep keys secret and do not commit `.env` to the repository.

Typical workflow
----------------
1. Document ingestion
   - Read PDFs / text / DOCX.
   - Clean and split long documents into chunks with overlap (for context preservation).
2. Embedding generation
   - Use sentence-transformers, OpenAI embeddings, or another embedder.
   - Save embeddings to a vector store (FAISS local, Pinecone, Weaviate, or SQLite + quantized vectors).
3. Indexing
   - Build index and associate metadata (title, url, source, chunk id, original doc offsets).
4. Querying (RAG)
   - Given a user question, retrieve top-k relevant chunks.
   - Format a prompt that includes retrieved context and ask the LLM to answer and cite sources.
5. Evaluation and iteration
   - Validate answers for correctness and hallucination.
   - Adjust chunk size, retriever settings, prompt engineering.

Architecture & components
-------------------------
A typical structure for a notebook-first RAG project:

- notebooks/
  - 01_ingest_and_index.ipynb        # ingest documents, chunking, build index
  - 02_build_embeddings.ipynb        # embedding generation
  - 03_query_and_respond.ipynb       # retrieval + LLM responses
  - 99_experiments.ipynb             # experiments and evaluation
- src/ (optional)
  - data_loader.py
  - chunker.py
  - embedder.py
  - retriever.py
  - rag_agent.py
- data/
  - sample_docs/                     # example documents for tests/demos
- models/
  - local models or model pointers (not committed)

Data, privacy & legal disclaimer
-------------------------------
- Chanakya is intended for research / prototyping only. It is NOT legal advice.
- The system may hallucinate or produce incorrect/legally dangerous statements. Always consult a qualified lawyer for legal decisions.
- If you use real client data, ensure you comply with relevant privacy laws, handling, and secure storage (do not upload sensitive personal data to public API endpoints unless explicitly allowed).
- Remove API keys and secrets from notebooks before sharing.

Contributing
------------
Contributions, issues, and feature requests are welcome.

- If you open issues, include reproducible steps and environment details.
- Keep notebooks tidy: clear outputs before committing if you intend to keep repo size small.
- If adding heavy model files or datasets, reference them but do not commit large binaries — use pointers, download scripts, or Git LFS.

Suggested workflow for contributors
- Fork the repo
- Create a branch with a descriptive name
- Add/modify notebooks or scripts
- Open a pull request with a clear description of changes and how to run them

License
-------
Include a license that fits your needs (MIT, Apache-2.0, etc.). If the repo currently doesn't have one, add a LICENSE file. Example: MIT License.

Acknowledgements & references
-----------------------------
- Inspired by many open-source RAG / retrieval + LLM projects.
- Helpful libraries: LangChain, sentence-transformers, Hugging Face Transformers, FAISS, Pinecone.

Contact
-------
Maintainer: xPritam07
- GitHub: https://github.com/xPritam07

---

If you’d like, I can:
- Add a ready-to-commit README.md file into the repository with this content.
- Generate a requirements.txt with the most-likely dependencies.
- Inspect the repository and tailor the README to the actual notebooks and files (I’ll need permission to read the repo contents).
Please tell me which of those you'd like me to do next.
