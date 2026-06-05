import os
import json
import sys
sys.path.insert(0, '.')

from src.models import Document
from src.chunking import SentenceChunker
from src.store import EmbeddingStore
from src.agent import KnowledgeBaseAgent

data_dir = 'd:/AI_VINUNI/LAB7/Day-07-Lab-Data-Foundations/data'

# 1. Load documents
docs = []
for fname in os.listdir(data_dir):
    if fname.endswith('.md'):
        with open(os.path.join(data_dir, fname), 'r', encoding='utf-8') as f:
            content = f.read()
        docs.append(Document(id=fname, content=content, metadata={"src": fname}))

# 2. Chunk documents
chunker = SentenceChunker(max_sentences_per_chunk=3)
chunked_docs = []
for doc in docs:
    chunks = chunker.chunk(doc.content)
    for i, c in enumerate(chunks):
        chunked_docs.append(Document(id=f"{doc.id}_chunk_{i}", content=c, metadata={"src": doc.id}))

print(f"Total original docs: {len(docs)}")
print(f"Total chunks: {len(chunked_docs)}")

# 3. Store in EmbeddingStore
# We will just use MockEmbedder fallback, since students use MockEmbedder
store = EmbeddingStore(collection_name="benchmark_medical")
store.add_documents(chunked_docs)

# 4. Agent
def dummy_llm(prompt):
    # Dummy LLM just to avoid dependencies, but usually we just want retrieval metrics
    return "Based on context, the answer is generated."

agent = KnowledgeBaseAgent(store=store, llm_fn=dummy_llm)

# 5. Load benchmark queries
with open(os.path.join(data_dir, 'benchmark_questions.json'), 'r', encoding='utf-8') as f:
    queries = json.load(f)

# 6. Evaluate
print("\n=== BENCHMARK RESULTS ===")
correct = 0
for i, q in enumerate(queries, 1):
    question = q['question']
    expected_doc = q['expected_doc']
    
    # search top 3
    results = store.search(question, top_k=3)
    top_1_doc = results[0]['metadata']['src'] if results else "None"
    top_3_docs = [r['metadata']['src'] for r in results] if results else []
    
    is_correct = expected_doc in top_3_docs
    if is_correct:
        correct += 1
        
    print(f"[{i}] Query: {question}")
    print(f"    Expected: {expected_doc}")
    print(f"    Retrieved Top-1: {top_1_doc} (Chunk: {results[0]['content'][:50]}...)")
    print(f"    Top-3 contained Expected: {is_correct}")

print(f"\nRecall@3: {correct}/{len(queries)} = {correct/len(queries)*100:.1f}%")
