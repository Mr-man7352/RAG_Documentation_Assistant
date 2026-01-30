# 📚 Documentation Assistant for GitHub API Docs

A **(RAG)** system that answers questions about GitHub REST API documentation using semantic search with MMR retriever + LLM generation.

This project demonstrates an end-to-end RAG pipeline including:

- Web ingestion
- Semantic chunking
- Embeddings
- Vector database indexing
- Retriever design
- Answer generation
- Retrieval quality evaluation
- Latency benchmarking

Designed to reflect **industry RAG architecture patterns** rather than tutorial-level prototypes.

---

# System Architecture

```

Web Docs
    ↓
HTML Loader
    ↓
Markdown Conversion
    ↓
Semantic Chunker
    ↓
Embeddings (Sentence Transformers)
    ↓
Qdrant Vector Store
    ↓
Retriever
    ↓
LLM Generator
    ↓
Answer + Sources

```

---

# Project Structure

```

RAG/
│
├── ingestion/
│ └── web_loader.py
│
├── processing/
│ └── chunker.py
│
├── vectorstore/
│ └── ingestion.py
│
├── generation/
│ └── rag_chain.py
│
├── notebooks/
│ ├── ingestion_test.py
│ ├── ingestion_pipeline_test.py
│ ├── chunking_test.py
│ ├── retrieval_test.py
│ ├── generation_test.py
│ ├── retrieval_eval_test.py
│ └── latency_test.py
│
├── requirements.txt
└── README.md

```


Each layer is independently testable — mirrors production RAG service layering.

---

# Data Source

Current ingestion source: https://docs.github.com/en/rest/issues/issues


Easily extensible to multiple documentation sources.

---

# Chunking Strategy (Industry Style)

Instead of naive fixed-size chunking, this system uses:

## Header-Aware Chunking

- Split on H1, H2 and H3 markdown headers
- Preserves semantic topic boundaries
- Aligns with user query intent

## Size Enforcement

- Target chunk size: ~1200 chars
- Max chunk size: 2000 chars
- Oversized chunks → recursively split
- Small chunks → merged intelligently

## Metadata Added Per Chunk

api_name
source_url
page_title
doc_type
contains_code
header_section


This improves retrieval filtering and answer grounding.

---

# Embeddings

Model: sentence-transformers/all-MiniLM-L6-v2

---

# Vector Store 

Vector DB : Qdrant (local in-memory mode)

---

# Generation Layer - Groq API

---

# Evaluation Implemented

This project includes measurable RAG evaluation — rarely done in beginner projects.

---

## Retrieval Metric — Hit@K

Measures whether correct doc appears in top-K retrieved chunks.

Example result:

Hit@5 = 75%
Hit@8 = 100%

## Latency Measurement -

Average Retrieval latency = 3.2 seconds

---

# Future Improvements

- Multi-source ingestion
- Hybrid retrieval (BM25 + dense)
- Hallucination detection
- Evaluation dashboards
- UI interface










