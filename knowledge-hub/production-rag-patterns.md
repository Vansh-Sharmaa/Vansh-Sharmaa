# 📚 Production RAG Architectures & Advanced Retrieval Patterns

Naïve RAG fails on keyword precision, domain acronyms, and long documents. Production RAG combines dense embeddings, sparse lexical retrieval, and cross-encoder reranking.

---

## 🏛️ End-to-End Pipeline

```
Query ──┬──► Dense Retriever (Vector / FAISS) ─────► Top 50 Docs ──┬──► Reranker (Cross-Encoder) ──► Top 5 Docs ──► LLM
        └──► Sparse Retriever (BM25 / Keyword) ────► Top 50 Docs ──┘    (Reciprocal Rank Fusion)
```

---

## 🔄 Reciprocal Rank Fusion (RRF) Formulation

RRF aggregates ranked lists without requiring calibrated score normalization:

$$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:
- $M$ is the set of retrieval models (Dense, BM25).
- $r_m(d)$ is the rank position of document $d$ in system $m$.
- $k$ is a constant smoothing parameter (standard default: $k = 60$).

```python
def reciprocal_rank_fusion(dense_results: list[str], sparse_results: list[str], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    
    for rank, doc in enumerate(dense_results):
        scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank + 1)
        
    for rank, doc in enumerate(sparse_results):
        scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank + 1)
        
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)
```

---

## 🎯 Key Takeaways for Production
1. **Semantic Chunking**: Split along logical headers and semantic boundaries rather than fixed character counts.
2. **Contextual Compression**: Strip extraneous tokens before passing retrieved passages into prompt context.
3. **Evaluation Loop (RAGAS)**: Continually measure context relevance, faithfulness, and answer relevance.
