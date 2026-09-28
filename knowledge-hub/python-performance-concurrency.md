# 🐍 High-Performance Python: Memory Management & Concurrency

Techniques for writing low-latency, memory-efficient Python code for ML inference pipelines and backend microservices.

---

## 💾 Memory Optimization with `__slots__` and Buffer Protocols

### 1. Reducing Object Overhead with `__slots__`
Standard Python objects use an internal `__dict__` to store dynamic attributes, consuming significant memory when instantiated millions of times.

```python
class DataPointSlots:
    __slots__ = ('embedding_id', 'vector', 'timestamp')
    def __init__(self, embedding_id: int, vector: list[float], timestamp: float):
        self.embedding_id = embedding_id
        self.vector = vector
        self.timestamp = timestamp
```

### 2. Zero-Copy Slicing with `memoryview`
Avoid copying multi-megabyte binary payloads (e.g., audio, images, serialized embeddings) by utilizing buffer views:

```python
raw_bytes = bytearray(b"X" * 10_000_000)
# Zero memory allocation slice:
view = memoryview(raw_bytes)[1000:5000]
```

---

## ⚡ Concurrency: Async I/O vs Multiprocessing

| Workload Type | Bottleneck | Recommended Model | Python Primitive |
|---------------|------------|-------------------|------------------|
| LLM API Calls / Web Requests | Network I/O | Async Event Loop | `asyncio.gather()` / `aiohttp` |
| Tokenization / Preprocessing | CPU Bound | Process Pool | `concurrent.futures.ProcessPoolExecutor` |
| Vector Dot Product / Linear Algebra | Compute / SIMD | C/C++ Extensions | NumPy / BLAS / PyTorch (releases GIL) |

```python
import asyncio

async def fetch_llm_inference(prompt: str, client) -> str:
    response = await client.chat.completions.create(
        model="llama3-8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def batch_process(prompts: list[str], client):
    tasks = [fetch_llm_inference(p, client) for p in prompts]
    return await asyncio.gather(*tasks)
```
