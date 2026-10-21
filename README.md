# Ultimate RAG Course for Developers

A practical, developer-focused course on building Retrieval-Augmented Generation (RAG) systems with Python. The playlist is designed to be **90% hands-on practice and 10% theory**, taking you from a baseline RAG pipeline to production deployment.

> Chapter code lives in numbered folders (`01_...` through `07_...`). The `notes/` folder contains accompanying visual notes, organized by chapter and episode.

## Course playlist

[Watch the Ultimate RAG Course for Developers on YouTube](https://www.youtube.com/playlist?list=PLJ1a2S34HAJ4)

## Technology stack

- Python 3+
- OpenAI
- LangChain and LangGraph
- LangSmith
- Qdrant
- Ragas
- Docker

## Chapters

| Chapter | Code | Topics |
| --- | --- | --- |
| 1. Baseline RAG | [`01_baseline_rag/`](01_baseline_rag/) · [`notes/01_baseline_rag/`](notes/01_baseline_rag/) | What RAG is; document loading and chunking; embeddings; storing documents in a vector database; retrieval; answer generation; a complete baseline pipeline. |
| 2. Better Ingestion and Chunking | [`02_better_ingestion_chunking/`](02_better_ingestion_chunking/) · [`notes/02_better_ingestion_chunking/`](notes/02_better_ingestion_chunking/) | Loading different document types, metadata, and chunking strategies. |
| 3. Advanced Retrieval | [`03_advance_retrival/`](03_advance_retrival/) · [`notes/03_advance_retrival/`](notes/03_advance_retrival/) | Limitations of baseline RAG, metadata filtering, top-k and similarity thresholds, hybrid search, and reranking. |
| 4. Query and Context Engineering | [`04_query_context_engineering/`](04_query_context_engineering/) · [`notes/04_query_context_engineering/`](notes/04_query_context_engineering/) | Query rewriting, multi-query retrieval, context selection and compression, MMR, grounded answers, and citations. |
| 5. RAG Evaluation and Optimization | [`05_rag_evaluation_optimization/`](05_rag_evaluation_optimization/) · [`notes/05_evaluation_optimization/`](notes/05_evaluation_optimization/) | Evaluate retrieval and generation, then optimize RAG quality, cost, and latency. |
| 6. LangGraph and RAG | [`06_langgraph_rag/`](06_langgraph_rag/) · [`notes/06_langgraph_rag/`](notes/06_langgraph_rag/) | LangGraph fundamentals and conditional RAG workflows. |
| 7. Production RAG | [`07_production_rag/`](07_production_rag/) · [`notes/07_production_rag/`](notes/07_production_rag/) | Build a RAG API with FastAPI, add tracing and observability with LangSmith, and deploy the application. |

## Getting started

### Prerequisites

- Python 3+
- An OpenAI API key for examples that call OpenAI
- Docker, for examples that use containerized services such as Qdrant

### Set up the environment

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Configure the environment variables required by an example in a local `.env` file. Check that chapter's code for the variable names it reads. Keep API keys private and never commit `.env` files.

Start with the code in `01_baseline_rag/`, then follow the numbered chapter folders in order. Each folder contains the code for its chapter; individual scripts and setup steps can vary by episode. The project also includes sample data under `datasource_documents/`, `mix_documents/`, and `evaluation_documents/`.

For the production chapter, see [`07_production_rag/README.md`](07_production_rag/README.md) for instructions to launch the FastAPI example.

## Connect with LoopKaka

- [Discord community](https://discord.com/invite/BZwkqTsbND)
- [LinkedIn](https://www.linkedin.com/in/sangrambadi/)
- [LoopKaka website](https://loopkaka.com/)
- [Udemy courses](https://www.udemy.com/user/sangram-badi/)
- [Instagram](https://www.instagram.com/tech.loopkaka)
- [WhatsApp channel](https://www.whatsapp.com/channel/0029Vb8N8cK3gvWUWIITKL3o)
