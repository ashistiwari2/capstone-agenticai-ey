# Evaluation Rubric

| Area | What is evaluated | Evidence |
|---|---|---|
| Ingestion | Documents are loaded and chunked cleanly | `outputs/chunks.json` |
| Retrieval | Hybrid search returns relevant chunks | `03_retrieve_rerank.py` output |
| Grounding | Answers cite source chunks and abstain when unsupported | `04_generate_grounded.py` output |
| Tool use | EMI calculator is invoked for calculation questions | `05_agent_graph.py` output |
| HITL | Approval-sensitive requests pause for human approval | `05_agent_graph.py` output |
| Evaluation | Metrics are generated and saved | `outputs/evaluation_report.json` |
| Safety | PII is redacted from logs | `src/utils/pii_filter.py` |
