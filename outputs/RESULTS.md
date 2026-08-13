# Capstone Results

## Scenario

Scenario A: Banking Support Agent

## Pipeline status

| Step | Status | Notes |
|---|---:|---|
| Ingest and chunk | Done | Banking text files are chunked into JSON |
| Embed and index | Done | Local TF-IDF and BM25 index created |
| Hybrid retrieval | Done | BM25 + vector similarity fused with RRF |
| Grounded generation | Done | Answers include citations to source chunks |
| Agent tools | Done | EMI calculator available |
| Human approval | Done | Loan approval-like actions require approval |
| Evaluation | Done | Local metrics written to JSON |

## Example output

Run:

```bash
python src/04_generate_grounded.py "What documents are needed for a home loan?"
```

Expected behavior:

- Retrieves relevant loan policy chunks
- Answers only from provided context
- Includes citations like `[loan_policy.txt#chunk-1]`

## Notes for final submission

Add screenshots in `outputs/screenshots/` after running the scripts locally.
