# Planned GCN and evaluation

## Question

Does source-graph structure improve prediction of omitted information units compared with the same text and type features without graph connectivity?

## Input and output

One source graph per abstract. Nodes are source information units and a study node. Node inputs: text embeddings, concept-type one-hot representation and a summary-text embedding shared across that paper. Optional study-node supervision mask excludes study nodes from classification. Output: two logits per information-unit node, preserved versus omitted. A two-layer GCN with hidden dimension 32 or 64, ReLU and dropout is a proposed starting architecture, not an executed experiment. For message passing, add reverse edges/self-loops in a documented preprocessing step; retain original directed relations for interpretation. GCN ignores relation types initially; relation-aware models are extensions.

## Leakage controls

Keep all nodes and summary variants from one paper in one partition. Fit any learned preprocessing using training data only. Never input labels, retained/omitted status, summary graph membership, coverage, graph differences, exact matching decisions or any feature that defines the label. Gold labels must come from independently checked semantic alignment. Numerical information units require a consistent rubric for complete versus partial retention.

## Baselines and metrics

Compare majority class and logistic regression/MLP with identical non-graph features, plus a separate direct text/semantic-matching baseline. Assess omission-class precision, recall and F1, macro-F1 and confusion matrices. Report mean and standard deviation across several seeds. With only 15-30 papers, consider grouped cross-validation and report per-paper variability; a tiny held-out partition may be unstable. Do not treat related concept nodes as independent studies. Evaluate extraction quality separately on a manually audited subset.

## Remaining checks

Expand to 15-30 papers using recorded inclusion criteria. Freeze the summary prompt and version, log one or more controlled runs, annotate independently, adjudicate partial or distorted cases and compare the trained models. An omission need not indicate harm. Quantify demographic/limitation coverage descriptively and investigate any bias claim separately. A coverage index is experimental and cannot certify medical reliability.
