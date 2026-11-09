# Full pipeline and checkpoint boundary

```mermaid
flowchart TD
 A[Public abstracts and citations] --> B[LLM summaries]
 A --> C[LLM structured source extraction]
 B --> D[LLM structured summary extraction]
 C --> E[Evidence validation and concept alignment]
 D --> E
 E --> F[Source and summary graphs]
 F --> G[Descriptive coverage and graph statistics]
 E --> H[Independent review and labels]
 H --> I[Paper grouped train validation test split]
 I --> J[GCN and non graph baseline training]
 J --> K[Held out evaluation and reader feedback]
```

Current checkpoint: A-G implemented as saved assistant-generated outputs and deterministic replay. Independent review H and trained evaluation I-K remain future work. The graph model uses source graph plus text features, never label-derived aligned graph differences.
