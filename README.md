# Documentation Assistant for GitHub REST API Docs

This repository is a small retrieval-augmented generation pipeline built around one GitHub REST API documentation page:

- Source page: https://docs.github.com/en/rest/issues/issues
- Retrieval backend: local in-memory Qdrant
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Generation model: Groq-hosted llama-3.1-8b-instant

The codebase covers ingestion, markdown-aware chunking, vector indexing, retrieval, answer generation, and a few script-based evaluation helpers.

## What The Code Actually Does

The current pipeline is:

```text
GitHub Docs page
  -> fetch HTML with requests
  -> extract <main id="main-content">
  -> convert extracted HTML to markdown
  -> split by markdown headers
  -> enforce chunk size limits
  -> embed chunks with MiniLM
  -> index into Qdrant (:memory:)
  -> retrieve relevant chunks
  -> generate an answer with Groq
```

Important scope notes:

- The implementation currently ingests a single documentation URL, not a multi-source corpus.
- Qdrant is used in in-memory mode only, so indexed data is not persisted across runs.
- The generator returns a text answer only. It does not return structured source citations.
- The scripts in notebooks/ are regular Python scripts, not Jupyter notebooks.

## Project Structure

```text
.
├── generation/
│   └── rag_chain.py
├── ingestion/
│   ├── __init__.py
│   └── web_loader.py
├── notebooks/
│   ├── chunking_test.py
│   ├── generation_test.py
│   ├── ingestion_pipeline_test.py
│   ├── ingestion_test.py
│   ├── latency_test.py
│   ├── llm_judge_eval.py
│   ├── retrieval_eval.py
│   ├── retrieval_test.py
│   └── run_llm_eval.py
├── processing/
│   └── chunker.py
├── vectorstore/
│   ├── __init__.py
│   └── ingestion.py
├── requirements.txt
└── README.md
```

## Components

### Ingestion

ingestion/web_loader.py:

- Fetches a documentation URL with requests.
- Parses HTML with BeautifulSoup.
- Extracts only the page's main content from main-content.
- Returns the extracted HTML fragment plus source metadata.

### Chunking

processing/chunker.py:

- Converts the extracted HTML fragment to markdown with markdownify.
- Splits on markdown headers #, ##, and ###.
- Uses RecursiveCharacterTextSplitter for oversized sections.
- Merges adjacent chunks smaller than the configured minimum size.

Default chunking parameters:

- Minimum chunk size: 400 characters
- Target chunk size: 1200 characters
- Maximum chunk size: 2000 characters
- Recursive overlap: 100 characters

Chunk metadata currently includes:

- api_name
- source_url
- page_title
- doc_type
- contains_code

The code does not explicitly add a header_section metadata field.

### Vector Store

vectorstore/ingestion.py:

- Uses HuggingFaceEmbeddings with all-MiniLM-L6-v2.
- Creates a QdrantVectorStore from the generated chunks.
- Stores vectors in Qdrant using location=:memory:.
- Reuses the same vector store instance within a run if more chunks are added.

### Retrieval And Generation

generation/rag_chain.py:

- Builds a retriever from the vector store with MMR search.
- Uses k=12, fetch_k=20, and lambda_mult=0.7.
- Sends retrieved context and the user question to ChatGroq.
- Returns the model response as plain text.

The prompt instructs the model to stay grounded in the retrieved documentation and include endpoint details when available.

## Evaluation Helpers

The repository includes small evaluation scripts rather than a packaged benchmark framework.

notebooks/retrieval_eval.py:

- Evaluates Hit@K over four hard-coded questions.
- Treats retrieval as a hit when an expected keyword appears in the retrieved chunk text.

notebooks/latency_test.py:

- Measures end-to-end generation latency across four hard-coded questions.
- Prints per-question latencies and an average.

notebooks/llm_judge_eval.py:

- Defines LLM-based scoring helpers for groundedness, relevance, completeness, and hallucination rate.
- Uses Groq for evaluation, including a 3-run average for hallucination scoring.

notebooks/run_llm_eval.py:

- Runs the generation pipeline over four questions.
- Aggregates average judge scores.

These scripts do not guarantee any fixed metrics. Reported values depend on the current model behavior, retrieval results, network conditions, and the source page content at runtime.

## Setup

Install the listed dependencies:

```bash
pip install -r requirements.txt
```

Generation and LLM-based evaluation also require Groq support and an API key. The code imports langchain_groq, so install it if it is not already available in your environment:

```bash
pip install langchain-groq
export GROQ_API_KEY="your_api_key_here"
```

## Running The Scripts

The scripts currently import modules using the RAG.* namespace. Make sure your environment/package layout supports that import path before running them.

Examples:

```bash
python notebooks/ingestion_pipeline_test.py
python notebooks/retrieval_test.py
python notebooks/generation_test.py
python notebooks/retrieval_eval.py
python notebooks/latency_test.py
python notebooks/run_llm_eval.py
```

## Current Limitations

- Single source URL only
- No persistent vector database storage
- No user interface
- No packaged CLI or application entrypoint
- Evaluation sets are small and manually defined
- Several scripts are experiment-style and assume a specific import layout

## Possible Next Improvements

- Support multiple documentation sources
- Add persistent Qdrant storage
- Add hybrid retrieval or reranking
- Package the project so scripts run cleanly without import-path setup
- Add source citation formatting in generation output










