## Slide 1 — Title

Time: 35 seconds. This is a preliminary evidence presentation for Project 3, Bias and Trust Analysis in Healthcare AI Summaries. Our narrower topic is information omissions in AI-generated summaries of exercise and sleep research in adults. We prepared a small reproducible feasibility pilot. The saved summaries, extraction records and annotations were AI-assisted. Independent student review and graph model training remain next steps. We will separate those planned tasks from what the pilot currently demonstrates.

## Slide 2 — Research question and scope

Time: 45 seconds. Our question is whether a summary retains the source information a reader needs to interpret a study. We focus on exercise interventions and sleep in adults. We audit information units such as participant characteristics, intervention duration, measurement methods, numerical results and qualifications. In this pilot, a unit is preserved when its full predefined meaning appears in the summary and omitted when it does not. This does not mean that every omitted detail is harmful. A general outcome can be retained while its exact effect size is missing. Partial or distorted cases will need separate adjudication as we expand the dataset.

## Slide 3 — Three papers form the pilot

Time: 45 seconds. We chose three public, cited research abstracts for a feasibility test. Baron and colleagues studied aerobic training in women with insomnia. Gale and colleagues studied evening activity breaks in healthy adults. Siu and colleagues compared tai chi, exercise and a control in older adults with insomnia. The populations and interventions differ, which is useful for testing the representation but prevents a single clinical conclusion. This is a purposive pilot, not a systematic review. We saved one AI-authored summary per abstract, with ten selected information units per paper. Exact citations and original licenses appear in the repository and on the final slide. Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC10138891/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11256039/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC7885034/

## Slide 4 — Full pipeline and midterm boundary

Time: 60 seconds. This diagram shows the full project, including future work. For the midterm we have cited abstracts, saved summaries, structured source and summary alignments, graph exports and descriptive results. The assistant authored these language outputs in this session. Our Python component validates text anchors and replays saved outputs rather than making live LLM calls. Two independent student reviews, controlled future generations and model training are still pending. The graph model is planned as a simple GCN, with a non-graph comparison. Solid green stages indicate the current feasibility implementation. Dashed stages indicate work remaining for the final project.

## Slide 5 — Working component and label definition

Time: 50 seconds. Our structured record stores a concept ID, type, source evidence, summary evidence and a provisional label. For example, Gale's abstract reports 28 participants and the saved summary says 28 adults, so the sample size is preserved. The abstract also reports a mean age of 25.6 years, which the saved summary does not state, so that specific unit is omitted. The Python validator checks that evidence strings occur in the stored texts. This is an integrity check, not proof of semantic correctness. The independent review columns in the CSV are blank so the team can review without pretending that human validation is already complete. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11256039/

## Slide 6 — First graph comparison

Time: 60 seconds. Here is the Gale paper's graph using the selected source information units. The study is connected to ten typed units and the intervention has assessed-for links to outcomes. The summary projection contains six of those units. Teal units are represented in the saved summary; orange outlines locate absent source units for comparison. These are source-aligned audit graphs, not exhaustive medical knowledge graphs. The smaller summary graph follows from our selected alignment and is not independent evidence of model success. The editable graph files and offline HTML viewer let us inspect each unit. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11256039/

## Slide 7 — 20 of 30 selected units are preserved

Time: 50 seconds. Across the three saved summaries, the provisional audit labels 20 of 30 selected units preserved and ten omitted. Baron has seven preserved and three omitted, Gale six and four, and Siu seven and three. The denominator is ten selected units per abstract, chosen during pilot development. These numbers describe our saved summaries and annotation choices. They are not GCN accuracy, an estimate for all medical summaries, or a clinical trust score. A future controlled study needs a frozen unit-selection rubric, independently reviewed labels and more source papers. Data: repository results/results.json.

## Slide 8 — Graph statistics are reproducible

Time: 40 seconds. This table reports graph sizes calculated by the script. Each source has eleven nodes: one study node and ten information-unit nodes. Source edge counts differ because outcome-unit counts differ. The summary graphs retain the study node and preserved units only. Total degree means in-degree plus out-degree. All edge endpoints are checked, and the degree sum equals twice the number of directed edges when counting both ends. GraphML exports and CSV statistics allow independent inspection. The source schema creates hub-and-spoke graphs, so graph size itself cannot establish medical importance or justify GCN superiority. Data: repository results/graph_statistics.csv.

## Slide 9 — Degree distributions expose a simple schema

Time: 35 seconds. Most selected units are leaves, while each study node links to all ten selected units. This concentration shows that our first graph schema is simple. The source graph distribution reflects our representation, not an independently discovered clinical network. We should enrich and validate meaningful relations as the corpus grows and test whether connectivity improves prediction over text features alone. If it does not, that negative finding is still valuable. Data: computed degree distributions from results/results.json.

## Slide 10 — Preliminary findings and their limits

Time: 60 seconds. Our first observation is that a summary can retain the broad sleep result while leaving out its magnitude or uncertainty. Gale's abstract reports an additional 27.7 minutes asleep with a 95 percent confidence interval from 2.3 to 52.4 minutes; our saved summary retains only the direction. Second, Siu's abstract calls the absolute improvements modest, while that qualification is absent from its saved summary. Third, population details such as women counts may be omitted while sample size remains. These are observations about these exact summaries. We cannot infer that all omissions are harmful, that the summaries are demographically biased or that clinical advice is reliable. Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC11256039/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC7885034/

## Slide 11 — GCN and evaluation plan

Time: 60 seconds. The planned prediction task is preserved versus omitted for each source information-unit node. A two-layer GCN will receive concept type, source-unit text embeddings and a summary-text representation, with source graph connectivity. The study node will be excluded from the classification loss. We will compare against logistic regression or an MLP using the same non-graph features and a separate text-matching baseline. All nodes and variants from one paper must remain in the same split. We must exclude labels, summary graph membership, coverage and graph differences from model inputs because those reveal the answer. We will report omission precision, recall and F1 plus macro-F1 and a confusion matrix across multiple seeds. No model has been trained at this checkpoint. GCN reference: https://arxiv.org/abs/1609.02907

## Slide 12 — Next steps and presentation readiness

Time: 45 seconds. Our immediate next step is for both students to independently review the provisional annotations and resolve disagreements. We will then collect fifteen to thirty papers with explicit inclusion criteria, freeze the prompt and annotation guide, and run a controlled generation protocol with recorded model metadata. Afterward we will train and compare the GCN and baselines. For this midterm, the code package already includes the saved data, graphs, statistics, validation log and run instructions. The GitHub folder is repository-ready but not published because no destination repository was supplied. Before submission we must add our partner's name, review the material, rehearse and use the Canvas deadline. The presentation supports preliminary findings and next steps rather than a completed project.

## Slide 13 — References and disclosure

Time: 15 seconds. These are the three pilot sources and the planned GCN reference. Article licenses and links are recorded with the data. The assistant authored the initial summaries, code and provisional annotations in this session; our independent review remains pending. We can demonstrate the offline graph viewer or show a source-and-summary example during questions.
