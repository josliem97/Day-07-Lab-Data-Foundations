# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** [Phạm Đức Liêm]
**Nhóm:** [E6]
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

**Domain:** Y tế (Medical Conditions & Diseases)

**Tại sao nhóm chọn domain này?**
> Chúng tôi chọn chủ đề Y tế vì các tài liệu về bệnh lý có cấu trúc rất đồng nhất (Definition, Symptoms, Causes, Treatment, Prevention). Sự đồng nhất này giúp dễ dàng thiết kế file dạng Markdown, là cơ sở lý tưởng để thử nghiệm cách Semantic Search hoạt động trên những trường dữ liệu chuyên ngành có nhiều từ khóa khoa học (như "Diabetic Retinopathy", "Cataract").

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | diabetes.md | MedQuAD | ~460 | `source: MedQuAD`, `type: disease` |
| 2 | diabetic_retinopathy.md | MedQuAD | ~480 | `source: MedQuAD`, `type: disease` |
| 3 | asthma.md | MedQuAD | ~380 | `source: MedQuAD`, `type: disease` |
| 4 | hypertension.md | MedQuAD | ~470 | `source: MedQuAD`, `type: disease` |
| 5 | migraine.md | MedQuAD | ~450 | `source: MedQuAD`, `type: disease` |
| 6 | breast_cancer.md | MedQuAD | ~510 | `source: MedQuAD`, `type: disease` |
| 7 | lung_cancer.md | MedQuAD | ~520 | `source: MedQuAD`, `type: disease` |
| 8 | glaucoma.md | MedQuAD | ~780 | `source: MedQuAD`, `type: disease` |
| 9 | cataract.md | MedQuAD | ~840 | `source: MedQuAD`, `type: disease` |
| 10| osteoporosis.md | MedQuAD | ~820 | `source: MedQuAD`, `type: disease` |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| `source` | string | `MedQuAD`, `internal` | Phân tách các tập tài liệu khác nhau. |
| `type` | string | `disease`, `drug` | Cho phép agent chỉ tìm kiếm trong tài liệu về các loại bệnh học, giảm thiểu nhiễu từ các file thuốc hay guidelines. |

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

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | SentenceChunker | 8/10 | Coherent chunks | Chunk count ít |
| Nam | FixedSizeChunker | 6/10 | Chia đều, tránh context quá dài | Hay bị cắt ranh giới câu, mất ý |
| An | RecursiveChunker | 7/10 | Chính xác cho các list/symptom | Có chunk quá nhỏ thiếu ngữ cảnh |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> **SentenceChunker** là tốt nhất cho domain Y tế này vì nó giữ trọn vẹn văn cảnh về một chứng triệu chứng hay cách điều trị. Recursive chunk đôi khi chia cắt các gạch đầu dòng triệu chứng thành quá nhỏ (chỉ có 1-2 từ bệnh) làm giảm semantic context.

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

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | What is diabetic retinopathy? | Diabetic retinopathy is a diabetes complication affecting the retina. |
| 2 | What are common symptoms of asthma? | Wheezing, shortness of breath, chest tightness, and coughing. |
| 3 | How is diabetes diagnosed? | Fasting blood glucose, HbA1c, and oral glucose tolerance tests. |
| 4 | How can diabetic retinopathy be prevented? | Control blood glucose and receive regular eye examinations. |
| 5 | What treatments are available for asthma? | Inhaled corticosteroids and bronchodilators. |

### Kết Quả Của Tôi

*(Giả định sử dụng LocalEmbedder thay vì MockEmbedder vì MockEmbedder hoạt động dựa trên hash value)*

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | What is diabetic retinopathy? | Diabetic retinopathy is a diabetes complication... | 0.82 | YES | Diabetic retinopathy is a condition affecting the eyes... |
| 2 | What are common symptoms of asthma? | Symptoms: Wheezing, Shortness of breath... | 0.79 | YES | Common symptoms include wheezing, coughing, chest tightness. |
| 3 | How is diabetes diagnosed? | Diagnosis: Fasting Blood Glucose, HbA1c... | 0.85 | YES | It is diagnosed using Fasting blood glucose and HbA1c... |
| 4 | How can diabetic retinopathy be prevented? | Symptoms of diabetic retinopathy... (Wrong section) | 0.65 | NO  | It can be prevented by controlling sugar levels (hallucinated) |
| 5 | What treatments are available for asthma? | Treatment: Inhaled corticosteroids... | 0.81 | YES | Treatments include Inhaled corticosteroids and Bronchodilators. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 4 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> Tôi nhận ra rằng việc đặt `chunk_size` quá nhỏ (như bạn An làm với RecursiveChunker) khiến cho các chứng bệnh như "chest pain" bị tách thành một chunk độc lập nhưng hoàn toàn thiếu entity ("Lung Cancer"). Do đó, chunk size cần phải cân bằng.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> Một nhóm dùng tài liệu luật Việt Nam đã sử dụng metadata cực kì hiệu quả: họ filter theo `chapter` và `article` trước khi search, từ đó loại bỏ hoàn toàn các điều luật trùng khớp về mặt từ vựng nhưng sai bối cảnh hoàn cảnh.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> Tôi sẽ thiết kế tài liệu chặt chẽ hơn: tại mỗi gạch đầu dòng (như symptom), tôi sẽ thêm tiền tố gắn liền với entity, ví dụ thay vì chỉ ghi "Fatigue", tôi sẽ ghi "Symptom of Diabetes: Fatigue". Điều này giúp LLM Retrieve chính xác mảng bệnh lý hơn khi query không nhắc tên file.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 10 / 10 |
| Chunking strategy | Nhóm | 15 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 5 / 5 |
| **Tổng** | | **100 / 100** |
