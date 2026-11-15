# P0 — Implementation literature map

**Updated coverage:** the [interactive literature library](literature/index.html) now analyzes all 23 unique articles present in the local source folder. Use its [research-role map](literature/research-map.html) for current proposed uses and baseline recommendations. The inventory notes below describe the earlier triage snapshot; subsequent analyses supersede its file-availability notes.

Date: 2026-11-13. Current work: P0.1; P1.4 is deferred. No P0 task is complete yet.

## Review scope

First two pages of local PDFs were extracted for metadata, abstracts, and introductory context. This is source triage, not a complete methods/equations/code audit. Proposed implementation uses below are our mappings, not claims that each paper implements the whole proposed system. Local PDFs do not independently authenticate every publication claim.

24 PDF files were inventoried, with 21 distinct byte hashes. Distinct hashes are not necessarily distinct articles. Twelve of the fifteen principal references were matched by DOI in local opening pages. LA-UPAHEM, Gao, and Aghdam were not found in this folder; their publisher records were located online. No source PDFs were modified.

## Principal implementation references

| ID | Paper | Role | Later phases | Availability |
|---|---|---|---|---|
| R01 | [Du / LA-UPAHEM](https://doi.org/10.1016/j.apenergy.2026.127976) | Core; adapted baseline candidate | P3, P8 | Publisher record; local PDF missing |
| R02 | [Li / DARC](https://doi.org/10.3390/en19163817) | Core; adapted repair baseline | P3, P6, P7 | Local PDF |
| R03 | [Huang / EECL](https://doi.org/10.1016/j.enbuild.2024.114378) | Core; causal/BN baseline candidate | P2, P5 | Local PDF |
| R04 | [Gao](https://doi.org/10.1016/j.enbuild.2024.113889) | Core; probabilistic baseline candidate | P2, P5 | Publisher record; local PDF missing |
| R05 | [Li / AFDD](https://doi.org/10.1016/j.buildenv.2025.114104) | Core; rule-based agentic baseline | P2, P5, P6 | Local PDF |
| R06 | [El Makroum](https://doi.org/10.1016/j.rineng.2026.109857) | Core; scheduling baseline candidate | P3, P7 | Local PDF |
| R07 | [Jia / STAR](https://doi.org/10.1016/j.enbuild.2026.117763) | Core; novelty collision; conditional baseline | P4, P5, P6 | Local PDF |
| R08 | [Ren](https://doi.org/10.3390/en19133098) | Safety helper; supplementary RL comparison | P1, P3, P4, P6 | Local PDF |
| R09 | [Aghdam](https://doi.org/10.1016/j.enbuild.2026.116978) | Residential Twin helper; novelty collision | P3, P4 | Publisher record; local PDF missing |
| R10 | [Wu](https://doi.org/10.1016/j.apenergy.2026.129073) | High-priority preference/authorization helper | P2, P3, P6 | Local PDF |
| R11 | [Zhang](https://doi.org/10.1016/j.apenergy.2026.127540) | Preference helper | P2, P3 | Local PDF |
| R12 | [Hwang](https://doi.org/10.1016/j.energy.2025.136162) | Twin/evidence helper | P4 | Local PDF |
| R13 | [Barricelli](https://doi.org/10.1080/0144929X.2026.2672579) | Interaction helper; novelty collision | P4, P6, P9 | Local PDF |
| R14 | [Wang](https://doi.org/10.1016/j.jmsy.2025.11.020) | Maintenance helper; novelty collision | P4, P6 | Local PDF |
| R15 | [Rezaei](https://doi.org/10.1016/j.egyai.2026.100853) | Architecture review; novelty framing | P7, P9 | Local PDF |

## R01 — Du / LA-UPAHEM

Adaptive home energy management to self-motivated user preferences via iterative LLM-augmented reinforcement learning

[DOI / publisher](https://doi.org/10.1016/j.apenergy.2026.127976)

Preference-to-control translation, iterative adaptation, metrics, and adaptation overhead. DRL remains a comparison, not our core controller.

## R02 — Li / DARC

DARC: A Constraint-Diagnostic LLM Agent Framework for Day-Ahead Dispatch of Campus-Level Integrated Energy Microgrids Under Natural-Language Preferences and Forecast Uncertainty

[DOI / publisher](https://doi.org/10.3390/en19163817)

Checker/Projector contracts, schedule repair, and grounded Critic feedback. Main experiments use a rule-based Decomposer and two LLM modules. Constraint diagnosis is distinct from five-family causal diagnosis.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/DARC A Constraint-Diagnostic LLM Agent Framework for Day-Ahead Dispatch of Campus-Level Integrated Energy Microgrids Under Natural-Language Preferences and Forecast Uncertainty.pdf>)

## R03 — Huang / EECL

An entropy-based causality framework for cross-level faults diagnosis and isolation in building HVAC systems

[DOI / publisher](https://doi.org/10.1016/j.enbuild.2024.114378)

Eigen-Entropy Causal Learning learns BN structure from data. Extract fault/symptom variables and cross-level evaluation; this does not itself supply our temporal SCM or active-test policy.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/An entropy-based causality framework for cross-level faults diagnosis and isolation in building HVAC systems.pdf>)

## R04 — Gao

Integrated building fault detection and diagnosis using data modeling and Bayesian networks

[DOI / publisher](https://doi.org/10.1016/j.enbuild.2024.113889)

Topology and expert knowledge mapped to building-wide Bayesian diagnosis. Full-text review pending.

## R05 — Li / AFDD

Agentic fault detection and diagnosis for building HVAC systems using AI agent, ontology, and diagnosis rules

[DOI / publisher](https://doi.org/10.1016/j.buildenv.2025.114104)

Ontology, generalized diagnostic rules, evidence access, and reports. Separate recommendations from experimentally verified recovery.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Agentic fault detection and diagnosis for building HVAC systems using AI agent , ontology, and diagram rules.pdf>)

## R06 — El Makroum

Agentic AI home energy management system: A large language model framework for residential load scheduling

[DOI / publisher](https://doi.org/10.1016/j.rineng.2026.109857)

Orchestrator plus three specialist agents, ReAct tools, and MILP comparison. Abstract claims an open-source release; code availability still needs inspection. Adapt device coverage explicitly.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/#Agentic AI home energy management system A large language model framework for residential load scheduling.pdf>)

## R07 — Jia / STAR

A data-driven iterative digital twin framework for dynamic building energy performance: Integrating virtual sensing and anomaly diagnosis

[DOI / publisher](https://doi.org/10.1016/j.enbuild.2026.117763)

Perception–diagnosis–optimization–update cycle, graph-random-walk attribution, and exploration/validation roles. Office retrofit optimization differs from residential operational recovery.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/A data-driven iterative digital twin framework for dynamic building energy performance, Integrating virtual sensing and anomaly diagnosis.pdf>)

## R08 — Ren

A Digital-Twin-Aided Safe Multi-Agent Reinforcement Learning Framework for Renewable-Integrated Residential Energy Management

[DOI / publisher](https://doi.org/10.3390/en19133098)

EV/battery constraints, synchronization, degradation parameters, and safety projection. MASAC agents are RL agents, not LLM-agent topologies.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/A Digital-Twin-Aided Safe Multi-Agent Reinforcement Learning Framework for Renewable-Integrated Residential Energy Management.pdf>)

## R09 — Aghdam

Digital twin assisted real-time energy management system for smart homes

[DOI / publisher](https://doi.org/10.1016/j.enbuild.2026.116978)

Residential Twin integration and real-time energy management assumptions. Full-text review pending.

## R10 — Wu

Human-in-the-loop preference calibration for home energy management via LLM-enabled contract-constrained language interfaces

[DOI / publisher](https://doi.org/10.1016/j.apenergy.2026.129073)

Structured preference events, explicit versus vague requests, confirmation, bounded updates, and MPC authority. Issue year 2027; available online 20 October 2026.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Human-in-the-loop preference calibration for home energy management.pdf>)

## R11 — Zhang

Large language model-enhanced home energy management with dynamic user preference elicitation and hierarchical data-sharing

[DOI / publisher](https://doi.org/10.1016/j.apenergy.2026.127540)

Preference elicitation, historical knowledge, reference actions, and information sharing. Its DRL framework need not be adopted to use preference mechanisms.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Large language model-enhanced home energy management with dynamic user preference elicitation and hierarchical data-sharing.pdf>)

## R12 — Hwang

Digital twin-enabled building energy management system for information fusion and energy efficiency

[DOI / publisher](https://doi.org/10.1016/j.energy.2025.136162)

Brick ontology, virtual models, and operational-signature classification. Information fusion does not establish recovery intervention performance.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Digital twin-enabled building energy management system for information fusion and energy efficiency.pdf>)

## R13 — Barricelli

A smart home platform integrating an energy-aware digital twin and an LLM-enabled conversational agent

[DOI / publisher](https://doi.org/10.1080/0144929X.2026.2672579)

Natural-language automation, conflict detection, and feedback. Twin plus LLM integration alone cannot be our novelty claim.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/#A smart home platform integrating an energy-aware digital twin and an LLM-enabled conversational agent.pdf>)

## R14 — Wang

Agentic digital twin-embedded maintenance methodology for energy equipment: A self-evolving operational paradigm

[DOI / publisher](https://doi.org/10.1016/j.jmsy.2025.11.020)

Memory/planning/decision workflow and Twin interaction; industrial boiler maintenance requires explicit adaptation to HEMS.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Agentic digital twin-embedded maintenance methodology for energy equipment A self-evolving operational paradigm.pdf>)

## R15 — Rezaei

From systematic evidence to agentic architectures: A systematic review and framework for large language model–driven smart grids

[DOI / publisher](https://doi.org/10.1016/j.egyai.2026.100853)

Role taxonomy, layered architecture, verification, and governance. Review/framework source, not automatically an executable baseline.

[Local PDF](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/From systematic evidence to agentic architectures, A systematic review and framework for large language model–driven smart grids.pdf>)

## R16 — Additional priority diagnosis paper

Mosteiro-Romero et al. (2026), Whole building HVAC diagnostic Bayesian networks for comfort-related fault detection and diagnosis: Application, evaluation and operational testing. [Publisher](https://www.sciencedirect.com/science/article/pii/S0360132326010668). DOI: 10.1016/j.buildenv.2026.115265. Local PDF not found; publisher abstract and TU Delft record inspected.

Recommended for P2/P5: coupled faults, knowledge/data parameter estimation, simultaneous-fault experiments, and sensor uncertainty. DBN here means Diagnostic Bayesian Network, not Dynamic Bayesian Network. Reported miss rates exceed 25% in all cases; limitations matter alongside accuracy. Full-text baseline feasibility remains pending.

## Additional local supporting sources

These are supporting sources, not mandatory implementation baselines:
- [AI-Powered Building Ecosystems A Narrative Mapping Review on the Integration of Digital Twins and LLMs for Proactive Comfort, IEQ, and Energy Management](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/#AI-Powered Building Ecosystems A Narrative Mapping Review on the Integration of Digital Twins and LLMs for Proactive Comfort, IEQ, and Energy Management.pdf>).
- [Automated building energy modeling for energy retrofits using a large language model-based multi-agent framework](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/#Automated building energy modeling for energy retrofits using a large language model-based multi-agent framework.pdf>).
- [A review on digital twin application in photovoltaic energy systems challenges and opportunities](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/A review on digital twin application in photovoltaic energy systems challenges and opportunities.pdf>).
- [A systematic review of transformers and large language models in the energy sector, twards agentic digital twins](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/A systematic review of transformers and large language models in the energy sector, twards agentic digital twins.pdf>).
- [Agentic Artificial Intelligence for Smart Grids A Comprehensive Review of Autonomous, Safe, and Explainable Control Frameworks](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Agentic Artificial Intelligence for Smart Grids A Comprehensive Review of Autonomous, Safe, and Explainable Control Frameworks.pdf>).
- [Artificial intelligence and machine learning for smart grids, from foundational paradigms to emerging technologies with digital twin and large language model-driven intelligence](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Artificial intelligence and machine learning for smart grids, from foundational paradigms to emerging technologies with digital twin and large language model-driven intelligence.pdf>).
- [DataSet, The CityLearn Challenge 2022 Overview, Results, and Leasons Learned](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/DataSet, The CityLearn Challenge 2022 Overview, Results, and Leasons Learned.pdf>).
- [Digital twins in renewable energy systems A comprehensive review of](<A:/University/Master/3rd Semester/LLM Course/Working/Literature review/Digital twins in renewable energy systems A comprehensive review of.pdf>).

The CityLearn Challenge 2022 paper is benchmark background. Pinned CityLearn 3.2.0 source, selected Alameda data, and recovered custom assets remain authoritative for current simulator behavior.

## P0 review order

1. Huang + Gao + whole-building Bayesian diagnosis: causes, dependencies, observability, identifiability, uncertainty.
2. STAR + AFDD: Twin adaptation, evidence, rules, and attribution.
3. DARC + Wu: action contracts, constraints, authorization, repair, and verification.
4. El Makroum + LA-UPAHEM: agent and scheduling baselines, preference adaptation.
5. Ren + Aghdam + Hwang + Zhang: safety, Twin, and preference details.
6. Wang + Barricelli + Rezaei and reviews: novelty boundaries.

## Specification extraction contract

For each implementation candidate record: precise algorithm/equations and page references; inputs/outputs; information access; data requirements; code/license availability; constraints; metrics; adaptation changes; reproducibility gaps. Label exact reproduction, adapted implementation, or inspiration.

The list does not yet establish an agreed mathematical foundation for dynamic SCM inference, action-dependent value of information, calibrated abstention, or safe active probing. Additional primary methods sources may be necessary.

## Next P0 deliverable

A specification matrix: requirement → supporting paper/page → proposed mechanism → simulator feasibility → open decision → acceptance evidence. Start with P0.1–P0.3: research scope, five degradation definitions, and observed/latent/evaluator-only information boundaries. Then define component contracts (P0.4) and hypotheses/metrics/versioning (P0.5). Preserve existing architecture choices; unresolved details require explicit decisions.
