# Glossary (Repo Excerpt)

For the full glossary, see: https://github.com/instance001/Whatisthisgithub/blob/main/GLOSSARY.md

This file contains only the glossary entries for this repository. Mapping tag legends and global notes live in the full glossary.

## Cognitive_Crowbar_nonverbal
| Term | Alternate term(s) | Alt map | External map | Relation to existing terminology | What it is | What it is not | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cognitive Crowbar — Non-Verbal v0.1 | nonverbal crowbar | ~ | ~ | Behavioural time-series reflection tool | Local, AI-free CLI that segments timestamped behaviour CSVs into episodes, computes event density/diversity/switching rate, labels episodes high_entropy/low_entropy/transition, outputs JSON summaries | Not emotion/mind reading; not diagnostic; no ML | Cognitive_Crowbar_nonverbal/README.md |
| Episode segmentation | segment | ~ | ~ | Windowing step | Converts raw behaviour stream into fixed windows and computes metrics per episode | Not clustering by semantics; purely temporal/heuristic | Cognitive_Crowbar_nonverbal/README.md |
| State summary | summarize | ~ | ~ | Label aggregation | Summarizes high/low/transition episodes into state_summary.json | Not an interpretive report; no inferred motivations | Cognitive_Crowbar_nonverbal/README.md |
