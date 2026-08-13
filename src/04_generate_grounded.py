import sys
from importlib.machinery import SourceFileLoader
from llm_client import local_grounded_response

retriever = SourceFileLoader("retriever", "src/03_retrieve_rerank.py").load_module()

def answer(query: str):
    contexts = retriever.retrieve(query, top_k=4)
    max_score = contexts[0]["score"] if contexts else 0
    if max_score < 0.015:
        return "I do not have enough information in the banking documents to answer this.", contexts
    return local_grounded_response(query, contexts), contexts

def main():
    query = " ".join(sys.argv[1:]) or "What documents are needed for a home loan?"
    response, contexts = answer(query)
    print(response)
    print("\nSources:")
    for ctx in contexts:
        print(f"- {ctx['chunk_id']}")

if __name__ == "__main__":
    main()
