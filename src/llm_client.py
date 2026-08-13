def local_grounded_response(query: str, contexts):
    """A deterministic local answer composer.

    Replace this function with Azure OpenAI/OpenAI/Anthropic/Ollama if required.
    The function intentionally uses only retrieved context to avoid unsupported claims.
    """
    if not contexts:
        return "I do not have enough information in the provided documents to answer this."

    query_terms = {t.lower() for t in query.replace("?", "").split() if len(t) > 2}
    selected = []
    for ctx in contexts:
        sentences = [s.strip() for s in ctx["text"].split(". ") if s.strip()]
        for sentence in sentences:
            lower = sentence.lower()
            if any(term in lower for term in query_terms):
                selected.append((sentence.rstrip("."), ctx["chunk_id"]))
        if len(selected) >= 4:
            break

    if not selected:
        return "I do not have enough grounded evidence in the retrieved documents to answer this confidently."

    bullets = [f"- {sentence}. [{chunk_id}]" for sentence, chunk_id in selected[:4]]
    return "Based on the banking policy documents:\n" + "\n".join(bullets)
