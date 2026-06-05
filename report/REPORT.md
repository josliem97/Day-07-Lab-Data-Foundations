# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** [Tên sinh viên]
**Nhóm:** [Tên nhóm]
**Ngày:** 05/06/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> Hai text chunk có high cosine similarity khi vector embedding của chúng hướng về cùng một phía trong không gian vector, tức là nội dung ngữ nghĩa của chúng tương tự nhau. Cosine similarity đo góc giữa hai vector — góc càng nhỏ, hai văn bản càng có ý nghĩa gần nhau, bất kể độ dài.

**Ví dụ HIGH similarity:**
- Sentence A: `"The dog ran across the field."`
- Sentence B: `"A dog was running through the meadow."`
- Tại sao tương đồng: Cả hai câu đều nói về một con chó đang di chuyển qua một khu vực mở, dùng các từ ngữ có nghĩa tương đương.

**Ví dụ LOW similarity:**
- Sentence A: `"The stock market closed at an all-time high today."`
- Sentence B: `"Scientists discovered a new species of deep-sea fish."`
- Tại sao khác: Hai câu thuộc hai domain hoàn toàn khác nhau (tài chính vs khoa học biển), không chia sẻ khái niệm nào.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Euclidean distance bị ảnh hưởng bởi độ dài của văn bản — văn bản dài tạo ra vector có độ lớn lớn hơn, dẫn đến khoảng cách lớn hơn dù nội dung giống nhau. Cosine similarity chỉ đo góc giữa các vector, không phụ thuộc vào độ lớn, nên hai đoạn văn cùng ý nghĩa nhưng khác độ dài vẫn cho điểm cao.

---

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

> Công thức: `num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))`
>
> `num_chunks = ceil((10000 - 50) / (500 - 50)) = ceil(9950 / 450) = ceil(22.11) = **23 chunks**`

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**

> `num_chunks = ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = ceil(24.75) = **25 chunks**`
>
> Overlap lớn hơn tạo ra nhiều chunks hơn vì mỗi bước nhảy (step = chunk_size - overlap) ngắn hơn. Lý do muốn overlap nhiều là để đảm bảo thông tin nằm ở ranh giới giữa hai chunk không bị "mất" — context được bảo toàn giữa các chunks liền kề, giúp retrieval bắt được những thông tin quan trọng bị cắt ngang.

---

## 2. Document Selection — Nhóm (10 điểm)

> ⚠️ **Phần này cần điền cùng nhóm.** Bảng dưới là template — nhóm cần thống nhất và điền vào.

### Domain & Lý Do Chọn

**Domain:** [ví dụ: Customer support FAQ, Vietnamese law, cooking recipes, ...]

**Tại sao nhóm chọn domain này?**
> *[Nhóm điền: 2-3 câu giải thích]*

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| | | | |
| | | | |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên đoạn văn AI/ML mẫu (chunk_size=150):

| Strategy | Chunk Count | Avg Length | Nhận xét |
|----------|-------------|------------|----------|
| `fixed_size` | 6 | 125.7 | Chia đều theo ký tự, có thể cắt giữa câu |
| `by_sentences` | 5 | 150.0 | Giữ được ranh giới câu, chunks dài và coherent hơn |
| `recursive` | 13 | 56.1 | Chia nhỏ nhất, nhiều chunks, phù hợp nội dung cần độ chính xác cao |

**Nhận xét:** `SentenceChunker` giữ ngữ nghĩa tốt nhất với avg_length cao — mỗi chunk chứa nhiều thông tin hơn. `RecursiveChunker` tạo nhiều chunks hơn, phù hợp khi cần precision nhưng có thể mất context. `FixedSizeChunker` đơn giản nhất nhưng dễ cắt giữa câu.

### Strategy Của Tôi

**Loại:** `SentenceChunker` (max_sentences_per_chunk=3)

**Mô tả cách hoạt động:**
> `SentenceChunker` phát hiện ranh giới câu bằng regex `(?<=[.!?])\s+|(?<=\.)\n`, tách văn bản thành từng câu riêng biệt, rồi gom nhóm theo `max_sentences_per_chunk`. Mỗi chunk là một nhóm tối đa 3 câu, đảm bảo ý trọn vẹn không bị cắt ngang.

**Tại sao tôi chọn strategy này?**
> SentenceChunker phù hợp nhất với các domain có cấu trúc văn xuôi tự nhiên (FAQ, tài liệu kỹ thuật, policy). Mỗi câu thường chứa một ý độc lập, nên gom theo câu giữ được semantic integrity tốt hơn so với cắt theo ký tự. Điều này giúp retrieval trả về context có nghĩa, không bị lủng lẳng giữa chừng.

### So Sánh: Strategy của tôi vs Baseline

| Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|----------|-------------|------------|--------------------|
| FixedSize (baseline) | 6 | 125.7 | Trung bình — có thể cắt giữa câu |
| **SentenceChunker (của tôi)** | **5** | **150.0** | **Tốt hơn — giữ ý trọn vẹn** |

### So Sánh Với Thành Viên Khác

> ⚠️ **Phần này điền sau khi nhóm chạy benchmark cùng nhau.**

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | SentenceChunker | | Coherent chunks | Chunk count ít |
| [Tên] | | | | |
| [Tên] | | | | |

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Dùng `re.split(r'(?<=[.!?])\s+|(?<=\.)\n', text)` để tách câu theo lookbehind pattern — tách sau dấu câu kết thúc mà không mất dấu câu đó. Sau đó gom mỗi nhóm `max_sentences_per_chunk` câu thành một chunk bằng `" ".join(group)`. Edge case xử lý: text rỗng trả về `[]`, câu ngắn hoặc không có dấu câu vẫn được gom vào chunk cuối cùng.

**`RecursiveChunker.chunk` / `_split`** — approach:
> `chunk()` gọi `_split(text, separators)` với danh sách separator đầy đủ. `_split()` dùng đệ quy: base case là khi text đã ngắn hơn `chunk_size` thì trả về `[text]`. Nếu chưa đủ ngắn, thử chia theo `separator[0]`, phần nào vẫn còn dài thì gọi đệ quy với `remaining_separators[1:]`. Khi hết separator, fallback về character-level splitting.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> `add_documents()` dùng `_make_record()` để embed từng doc thành vector rồi append vào `self._store` (list of dicts). `search()` embed query, rồi gọi `_search_records()` tính dot product giữa query embedding và mỗi stored embedding, sắp xếp giảm dần và trả về top-k. Mỗi result dict có keys: `id`, `content`, `metadata`, `score`.

**`search_with_filter` + `delete_document`** — approach:
> `search_with_filter()` filter trước: duyệt `self._store` và giữ lại chỉ những records có metadata khớp với tất cả key-value trong `metadata_filter`, rồi mới gọi `_search_records()` trên tập đã lọc. `delete_document()` dùng list comprehension để loại bỏ tất cả records có `id == doc_id`, trả về `True` nếu có ít nhất 1 record bị xóa.

### KnowledgeBaseAgent

**`answer`** — approach:
> `answer()` thực hiện 3 bước RAG: (1) gọi `store.search(question, top_k)` để retrieve các chunks liên quan nhất, (2) build prompt theo cấu trúc `[Context 1]: ... [Context 2]: ... Question: ... Answer:`, (3) gọi `llm_fn(prompt)` và trả về kết quả. Context được đánh số để LLM có thể tham chiếu, giúp tăng grounding quality.

### Test Results

```
platform win32 -- Python 3.12.8, pytest-9.0.3
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED

========================= 42 passed in 0.31s =========================
```

**Số tests pass:** 42 / 42 ✅

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

*Dùng `MockEmbedder` (deterministic hash-based embedding, dim=64). Chạy bằng `compute_similarity(embedder(a), embedder(b))`.*

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | The cat sat on the mat. | A cat is resting on a mat. | HIGH | **0.2933** | ✅ Cao nhất |
| 2 | Python is a programming language. | Python is used for machine learning. | HIGH | **-0.0824** | ❌ Bất ngờ |
| 3 | The sun rises in the east. | Football is played with 11 players. | LOW | **-0.0024** | ✅ Thấp |
| 4 | Machine learning uses data to train models. | Deep learning is a subset of machine learning. | HIGH | **-0.0035** | ❌ Bất ngờ |
| 5 | I love eating pizza. | The stock market crashed yesterday. | LOW | **0.0757** | ✅ Thấp |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Pair 2 và 4 là bất ngờ nhất: dù cả hai câu cùng đề cập đến "Python" hoặc "machine learning", MockEmbedder lại cho điểm âm — tức là vector hướng ngược chiều nhau. Điều này cho thấy MockEmbedder là **hash-based giả ngẫu nhiên**, không thực sự hiểu ngữ nghĩa như các model thực tế (BERT, OpenAI). Với real embedder (ví dụ `all-MiniLM-L6-v2`), Pair 2 và 4 sẽ cho điểm cao vì chúng chia sẻ domain và từ vựng. Bài học: kết quả retrieval phụ thuộc rất nhiều vào chất lượng embedding backend.

---

## 6. Results — Cá nhân (10 điểm)

> ⚠️ **Phần này điền sau khi nhóm thống nhất 5 benchmark queries.** Template sẵn dưới đây.

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu queries trả về chunk relevant trong top-3?** __ / 5

---

## 7. What I Learned (5 điểm — Demo)

> ⚠️ **Phần này điền sau buổi demo và thảo luận nhóm.**

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> *[Điền sau khi so sánh kết quả trong nhóm]*

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> *[Điền sau buổi demo]*

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> *[Điền sau khi phân tích failure case]*

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | __ / 10 |
| Chunking strategy | Nhóm | __ / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | __ / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | __ / 5 |
| **Tổng** | | **__ / 100** |
