\# Cognitive Crowbar – Non-Verbal Edition (v0.1)



Local-only, AI-free tooling for mapping cognition in \*\*non-verbal agents\*\*:

animals, pre-verbal humans, or any system that expresses cognition through

behaviour and signals instead of language.



This repository is a \*\*sister project\*\* to

\[`Cognitive\_Crowbar`](https://github.com/instance001/Cognitive\_Crowbar).



Where Cognitive Crowbar works on \*\*text + self-report\*\*, this non-verbal

edition works on \*\*behavioural time-series\*\*:



\- movement intensity

\- object switching

\- gaze shifts

\- task phase changes

\- other coded behaviours



It does \*\*not\*\* try to read minds or infer emotions. It only detects:



\- periods of high vs low behavioural entropy

\- transitions between states (search → insight → execution)

\- recurring patterns in problem solving or friction

\- simple episode-level metrics you can compare across agents or species



All processing is:



\- local-only

\- AI-free

\- transparent

\- based on simple, auditable heuristics



---



\## What this tool does



Given a CSV file of timestamped behaviour:



\- segments it into \*\*episodes\*\* (short windows of time)

\- computes simple metrics per episode:

&nbsp; - event density

&nbsp; - behaviour diversity

&nbsp; - switching rate

\- flags episodes as:

&nbsp; - `high\_entropy` (chaotic / exploratory)

&nbsp; - `low\_entropy` (focused / stable)

&nbsp; - `transition` (sudden shift in pattern)

\- saves everything as JSON for downstream analysis.



This lets animal behaviourists, cognitive ethologists, and AI researchers

see \*\*cognitive dynamics\*\* instead of just raw behaviour lists.



---



\## Example input format



Minimal CSV format (you can add more columns later):



```csv

timestamp\_sec,agent\_id,behavior

0.0,mouse\_01,explore

0.7,mouse\_01,explore

1.2,mouse\_01,rear

2.0,mouse\_01,groom

3.4,mouse\_01,explore

5.1,mouse\_01,manipulate\_object



Place files like this in examples/.

Quickstart



From the repo root:



\# 1) Segment a session into episodes and compute metrics

python crowbar\_nonverbal\_v0\_1.py segment \\

&nbsp; --input examples/sample\_session\_mouse.csv \\

&nbsp; --out examples/generated\_profile/episodes.json



\# 2) Summarise high / low / transition episodes

python crowbar\_nonverbal\_v0\_1.py summarize \\

&nbsp; --episodes examples/generated\_profile/episodes.json \\

&nbsp; --out examples/generated\_profile/state\_summary.json



The resulting JSON files are mechanistic only. They tell you:



&nbsp;   where entropy spikes



&nbsp;   where behaviour stabilises



&nbsp;   where sharp transitions happen



They do not interpret motivations, emotion, or “intelligence”.

Status



&nbsp;   v0.1 – reference implementation for simple CSV event logs



&nbsp;   Local-only, AI-free, stdlib-only Python



&nbsp;   Designed as a building block for future cross-species cognition mapping



License



AGPL-3.0. Fork it, extend it, cite it – but keep derivatives open.



This repository is part of the wider Symbound open cognitive

infrastructure: tooling for safe, transparent, substrate-agnostic

cognition engineering.

