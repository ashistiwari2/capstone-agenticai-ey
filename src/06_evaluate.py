import json
from importlib.machinery import SourceFileLoader
from config import OUTPUT_DIR

generator = SourceFileLoader("generator", "src/04_generate_grounded.py").load_module()
retriever = SourceFileLoader("retriever", "src/03_retrieve_rerank.py").load_module()

TEST_SET = [
    {"query": "What documents are needed for a home loan?", "expected_source": "loan_policy.txt"},
    {"query": "What is EMI?", "expected_source": "faq_emi.txt"},
    {"query": "What fees are charged on personal loans?", "expected_source": "fee_structure.txt"},
    {"query": "What happens if suspicious activity is detected?", "expected_source": "fraud_policy.txt"},
    {"query": "How can I close my account?", "expected_source": "account_closure.txt"},
]

def has_citation(answer):
    return "[" in answer and "]" in answer

def evaluate():
    rows = []
    hits = 0
    cited = 0
    for item in TEST_SET:
        contexts = retriever.retrieve(item["query"], top_k=3)
        top_sources = [c["source"] for c in contexts]
        hit = item["expected_source"] in top_sources
        if hit:
            hits += 1
        answer, _ = generator.answer(item["query"])
        citation_ok = has_citation(answer)
        if citation_ok:
            cited += 1
        rows.append({
            "query": item["query"],
            "expected_source": item["expected_source"],
            "top_sources": top_sources,
            "retrieval_hit_at_3": hit,
            "answer_has_citation": citation_ok,
            "answer": answer,
        })
    report = {
        "retrieval_hit_at_3": round(hits / len(TEST_SET), 3),
        "citation_rate": round(cited / len(TEST_SET), 3),
        "test_cases": rows,
    }
    out = OUTPUT_DIR / "evaluation_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report, out

def main():
    report, out = evaluate()
    print(json.dumps(report, indent=2))
    print(f"\nWrote evaluation report to {out}")

if __name__ == "__main__":
    main()
