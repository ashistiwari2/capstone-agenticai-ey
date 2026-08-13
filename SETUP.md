# Setup Guide

## 1. Create environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
```

The current implementation runs locally without any cloud key. Optional variables are reserved for future LLM integration.

## 3. Build indexes

```bash
python src/01_ingest_chunk.py
python src/02_embed_index.py
```

## 4. Test retrieval

```bash
python src/03_retrieve_rerank.py "What documents are needed for a home loan?"
```

## 5. Test grounded answer generation

```bash
python src/04_generate_grounded.py "What fees are charged on a personal loan?"
```

## 6. Run the agent

```bash
python src/05_agent_graph.py
```

## 7. Run evaluation

```bash
python src/06_evaluate.py
```

Evaluation output is written to:

```text
outputs/evaluation_report.json
```
