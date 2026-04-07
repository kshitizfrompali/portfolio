# NLP & LLM Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25 | 🏢 = Reported at specific companies

---

## Basic NLP

**Q: What is NLP?**
Natural Language Processing — techniques to process and understand human language using computers. Includes tokenization, POS tagging, NER, sentiment analysis, text classification, and language generation.

---

**Q: What is tokenization?**
Splitting text into smaller units (tokens) — words, subwords, or characters. The first step in most NLP pipelines. Handles punctuation, contractions, and language-specific rules.

---

**Q: What is Named Entity Recognition (NER)?** ⭐
Identifying and classifying named entities in text — persons, organizations, dates, medical terms, etc. spaCy's `ner` component does this. In clinical NLP, NER extracts diagnoses, medications, and dates from doctor notes.

---

**Q: What is Part-of-Speech (POS) tagging?**
Labeling each word with its grammatical role (noun, verb, adjective, etc.). Used as a feature in downstream NLP tasks. spaCy's `tagger` component handles this.

---

**Q: What is spaCy?** ⭐
Production-grade NLP library for Python. Provides tokenization, POS tagging, NER, dependency parsing, and custom pipeline components. Fast (Cython internals), designed for real workloads rather than research. I used it for clinical text processing — extracting medical entities and dates from patient notes.

---

**Q: What is stanza?**
NLP library from Stanford NLP group. Strong at scientific and clinical text. Better multilingual support than spaCy. Slower but more accurate on specialized domains. I used stanza for medical text where spaCy's accuracy wasn't sufficient for clinical terminology.

---

**Q: What is negation detection?** ⭐ (Healthcare NLP)
Identifying when an entity is negated in text — "patient has no fever" vs "patient has fever". Critical in clinical NLP — without it, NLP incorrectly flags denied conditions as present. I used NegSpacy (spaCy extension) to mark negated entities before passing results to the coding pipeline.

---

**Q: What is the difference between rule-based and ML-based NLP?**
Rule-based: hand-crafted patterns (regex, dependency rules) — fast, explainable, no training data, brittle to variation.
ML-based: learns from labeled data — generalizes better, needs examples, less interpretable.
Hybrid often works best: rule-based for structured patterns (dates), ML-based for entity recognition.

---

## LLMs

**Q: What is a Large Language Model (LLM)?** ⭐ 🔥
A neural network trained on large amounts of text using self-supervised learning. Learns to predict the next token, which results in emergent capabilities: reasoning, code generation, question answering. Examples: GPT-4, Claude, Llama.

---

**Q: What is a transformer architecture?** ⭐ 🔥
The neural network architecture behind modern LLMs. Key innovation: self-attention mechanism — allows the model to weigh relationships between all tokens in the input simultaneously. "Attention Is All You Need" (2017) paper introduced it.

---

**Q: What is a token in LLMs?** ⭐
The basic unit of LLM input/output. Not exactly a word — tokenizers split text into subwords (BPE, WordPiece). "ChatGPT" might be 1 token, "Hepatocellular" might be 3-4 tokens. Token count affects cost and context window limits.

---

**Q: What is a context window?** ⭐ 🔥
The maximum number of tokens an LLM can process at once (input + output). GPT-4: 128K tokens. Claude 3: 200K tokens. Beyond the context window, the model "forgets" earlier content. For long documents, you need chunking or retrieval strategies.

---

**Q: What is prompt engineering?** ⭐ 🔥 (AI engineering, every company)
Designing LLM inputs to get reliable, structured output. Techniques: system prompts (role/persona), few-shot examples, chain-of-thought, output format specification (JSON schema). In the HCC extraction pipeline, few-shot examples reduced malformed output by ~60%.

---

**Q: What is the difference between zero-shot, one-shot, and few-shot prompting?** 🔥
Zero-shot: just the instruction, no examples. One-shot: one example. Few-shot: 3-10 examples. More examples improve reliability for complex tasks but use more tokens. For structured extraction, few-shot with 3-5 examples is typically the sweet spot.

---

**Q: What is hallucination in LLMs?** ⭐ 🔥 (every AI interview)
When an LLM generates confident but incorrect or fabricated information. Root cause: LLMs are trained to produce plausible text, not necessarily factual text. Mitigations: RAG (ground answers in retrieved documents), structured output with validation, asking the model to cite sources, human review for critical outputs.

---

**Q: What is RAG (Retrieval-Augmented Generation)?** ⭐ 🔥
Combining a retrieval system (vector search over a document store) with an LLM. Instead of relying on the model's parametric memory, relevant documents are retrieved and included in the prompt as context. Reduces hallucination and allows using up-to-date or private information.

---

**Q: What is a vector embedding?** ⭐ 🔥
A dense numerical representation of text in a high-dimensional space. Similar texts are close in vector space. Generated by embedding models (OpenAI `text-embedding-ada-002`, Cohere, sentence-transformers). Used for semantic search, similarity, and RAG retrieval.

---

**Q: What is a vector database?** 🔥
A database optimized for storing and querying vector embeddings. Supports approximate nearest neighbor (ANN) search. Examples: Pinecone, Weaviate, Chroma, pgvector (PostgreSQL extension). Core infrastructure for RAG pipelines.

---

**Q: What is fine-tuning vs prompting?** 🔥 (AI engineering roles)
Prompting: giving instructions at inference time — no training cost, easy to iterate. Fine-tuning: training the model on domain-specific examples — better performance on specialized tasks, needs labeled data, expensive. For most production use cases, prompt engineering first; fine-tune only if prompting hits a ceiling.

---

## Advanced LLMs

**Q: How do you integrate an LLM into a production system reliably?** ⭐ 🔥 (top question at AI companies)
1. Validate LLM output schema with Pydantic — reject malformed responses
2. Structured output (JSON mode, function calling) for consistent format
3. Retry with exponential backoff on API errors
4. Log every input/output for debugging and audit
5. Idempotent downstream processing — handle duplicate LLM outputs safely
6. Set timeouts — LLMs can be slow under load
7. Monitor latency, error rate, and token costs

In the SLM service: LLM output arrived via SQS, Pydantic validated schema, idempotent DB writes handled duplicates.

---

**Q: What are the main challenges of running LLMs in production?** ⭐ 🔥
- **Latency**: 1-10s per request depending on model/length
- **Cost**: token-based pricing accumulates at scale
- **Reliability**: non-deterministic output, occasional failures
- **Hallucinations**: factually wrong output
- **Observability**: hard to debug black-box models
- **Context limits**: large documents need chunking

---

**Q: What is function calling / tool use in LLMs?** 🔥
Allowing LLMs to call structured functions by outputting a structured function call (name + arguments) instead of free text. The calling code executes the function and feeds the result back to the model. Used to build agents that can use tools (search, calculators, DB queries).

---

**Q: What is an AI agent?** 🔥 (every AI startup)
An LLM that can take actions using tools in a loop — observe, think, act, repeat. The agent decides which tool to call, interprets results, and continues until the task is done. Frameworks: LangChain, LlamaIndex, Claude's tool use API.

---

**Q: What is the difference between LangChain and direct API calls?** 🔥
LangChain provides abstractions: chains, agents, memory, document loaders, vector store integrations. Useful for rapid prototyping. Direct API calls give more control and less abstraction overhead — better for production systems where you need predictable behavior.

---

**Q: What is context stuffing vs RAG?** 🔥
Context stuffing: put all relevant documents directly in the prompt. Works for small datasets (< context window). RAG: retrieve only the most relevant chunks. Scales to large datasets, reduces token cost, but retrieval quality matters — bad retrieval = bad answers.

---

**Q: How do you evaluate LLM output quality?** 🔥 (Senior AI roles)
- **Human evaluation**: gold standard but expensive
- **LLM-as-judge**: use another LLM to evaluate output (GPT-4 grading Claude output)
- **Reference-based metrics**: BLEU, ROUGE for summarization
- **Task-specific metrics**: F1 for extraction, accuracy for classification
- **Behavioral testing**: write test cases that check specific behaviors

For HCC extraction I tracked precision/recall against manually labeled examples — critical for medical coding accuracy.

---

**Q: What is quantization in LLMs?** 🔥
Reducing model weight precision (float32 → float16 → int8 → int4) to reduce memory and speed up inference with minimal accuracy loss. Lets you run large models on smaller hardware. GGUF format (llama.cpp) enables quantized inference on CPU.

---

**Q: What is the difference between Claude, GPT-4, and open-source LLMs?** 🔥
Claude (Anthropic): strong at instruction following, long context, safety-focused, constitutional AI training. GPT-4 (OpenAI): broad capability, well-tested in production, large ecosystem. Open-source (Llama 3, Mistral): run on your own infrastructure (data privacy), customizable, slower iteration on safety. Choose based on data privacy requirements, cost, and capability needs.

---
