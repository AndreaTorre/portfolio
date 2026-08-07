The material was produced during the Artificial Intelligence course of the Master’s Degree in Computer Science at the University of Milano-Bicocca.


## Paper presentation
It includes a presentation on “To Believe or Not to Believe,” in which the article was analyzed and personally presented during the lectures.

## Exam project

This project investigates how factual hallucinations emerge in Retrieval-Augmented
Generation systems and how they can be detected through response-pattern analysis.
The experiments use a closed-domain collection of Italian legal documents concerning
the Bologna bombing, together with a set of fact-oriented questions and reference
answers.
The pipeline divides each source document into overlapping chunks and creates both
a dense semantic index and a sparse lexical index. Dense retrieval uses normalized
sentence embeddings and FAISS, while sparse retrieval uses BM25. A hybrid strategy
combines the normalized scores produced by the two methods. Retrieved passages
are then provided to llama-3.3-70b-versatile to generate the final answers.
Two prompting strategies are compared: a strict context-only instruction and a more
permissive context-assisted instruction. Responses are evaluated against both the
reference answers and the retrieved evidence using precision, recall, F1 and faithfulness.
Automated evaluation is complemented by manual inspection of false-positive claims,
which are classified as missing evidence, incomplete reference answers or genuine
factual hallucinations.

### Results

On the 15 questions associated with non-empty source documents, context-only
prompting achieved higher mean precision and recall than context-assisted prompting:
0.63 versus 0.46 precision and 0.53 versus 0.49 recall. Mean faithfulness
was similar, reaching approximately 0.79 and 0.78, respectively. Manual analysis
identified 6 genuine hallucinations for the context-only configuration and 10
for the context-assisted configuration, suggesting that stricter grounding reduced
unsupported factual additions.

### Technologies and methods

Python, Sentence Transformers, all-MiniLM-L6-v2, FAISS, BM25, LangChain, Llama3.3 70B, RAGAS, Pandas

