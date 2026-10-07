# Literature Review: Organ Transplant Donor–Recipient Matching
### Supporting Document for PBL Project — *Smart Organ Transplant Matching System*
**Prepared for:** Anirudh Yadav (2501330100073), B.Tech CSE–A, DSA-II (CCSE0301)
**Related to:** PBL Progress Report – I, Section 6 (Research/Literature Review)

---

## 1. Purpose of This Document

This document reviews the three research papers cited in the Month-1 PBL Progress Report, summarizes what each paper actually did, identifies the gaps left open by each, and explains how the proposed *Smart Organ Transplant Matching System* (a DSA-based project using Trees, Heaps, and Graphs) is positioned differently from — and is a deliberate simplification of — the approaches used in these papers.

The three papers reviewed are:

1. **Syed et al. (2024)** – *Potential of New 250-Nautical Mile Concentric Circle Allocation System for Improving the Donor/Recipient HLA Matching: Development of New Matching Algorithm.* Transplant Immunology 87, 102146.
2. **Majouni et al. (2025)** – *A Heterogeneous Bipartite Graph Framework for Donor-Recipient Matching in Kidney Transplantation.*
3. **Melehy et al. (2026)** – *Liver Transplant Donor-Recipient Matching with Offline Reinforcement Learning.* npj Digital Medicine 9:351.

---

## 2. Paper-by-Paper Review

### 2.1 Syed et al. (2024) — 250-Nautical Mile HLA Allocation Simulation

**What the paper is about:**
The paper studies whether the new US kidney allocation policy (the 250-nautical-mile concentric-circle rule introduced in 2018) can be used to find *immunologically better-matched* kidney donors for patients, instead of just any ABO-compatible donor.

**What they actually did:**
- Used real SRTR (Scientific Registry of Transplant Recipients) data for 672 waitlisted patients and 6,558 deceased donors around University of Toledo Medical Center (UTMC), from 2014–2019.
- Built an in-house **simulation/allocation algorithm** that:
  - Imputes high-resolution HLA types from low-resolution data (using haplotype frequency tables).
  - Calculates a **Hydrophobic Mismatch Score (HMS)** — a continuous, amino-acid-level immunogenicity score — for every possible donor–recipient pair.
  - Enforces **ABO blood-type compatibility** as a hard constraint.
  - Optionally enforces **KDPI ≤ 50%** (Kidney Donor Profile Index, a donor-quality score).
  - Picks the lowest-HMS (least immunogenic) available donor for each recipient, removing that donor from the pool once used (a greedy one-to-one assignment).
- Compared the simulated matches against a real historical cohort (2000–2010) using Kaplan–Meier survival analysis.

**Key results:**
- 99.8% of patients could be matched with a low-immunogenicity (HMS ≤ 10), KDPI ≤ 50% donor.
- Simulated matches had far lower average HMS (1.4) than real-world transplants (6.3).
- Projected median graft survival rose from 13.4 years (real cohort) to 18.2 years (simulated), a gain of ~4.9 years per transplant.
- Each patient typically had access to 100+ potential well-matched donors within the 250-mile radius (median ~141–229 donors per year, depending on year).

**How it works, structurally:** This is essentially a **greedy bipartite assignment algorithm** — for each recipient, search all eligible donors, filter by hard constraints (ABO, KDPI), rank by a continuous immunogenicity score (HMS), and assign the best available one. No machine learning is used; it is a rules + scoring + greedy-selection simulation.

---

### 2.2 Majouni et al. (2025) — Heterogeneous Bipartite Graph + GNN Framework

**What the paper is about:**
This is a **methodology/architecture paper** (not yet a fully evaluated system) proposing a graph neural network (GNN) approach to donor–recipient matching for kidney transplants, framed as a "feature set matching" problem.

**What they actually did:**
- Modeled donors and recipients as the two node sets of a **heterogeneous bipartite graph** built from SRTR data (5,000 donor nodes, 5,000 recipient nodes; donors have 26 features, recipients have their own feature vector).
- Defined **four types of edges**, each encoding a different kind of domain knowledge:
  1. **Compatibility edges** — connect donor–recipient pairs that actually transplanted and survived past a threshold (5 or 8 years). Sparse, one-to-one.
  2. **Knowledge-driven edges** — derived from the Baskin-Bey Recipient Risk Score (RRS) and a Deceased Donor Score (DDS, 0–39 points, computed from age, hypertension history, estimated GFR via the CKD-EPI equation, HLA mismatch, and cause of death). Donors are graded A–D by DDS and matched to recipient risk groups RG1–RG4.
  3. **Blood-type and cluster-based edges** — encode ABO compatibility rules (O → universal donor, AB → universal recipient, etc.) and cluster recipients/donors with historically higher match-success likelihood.
  4. **Time-based edges** — capture waitlist urgency, organ viability windows, and disease progression.
- The resulting graph has ~18 million edges connecting 5,000 donors to 5,000 recipients.
- Proposed pipeline: embed the heterogeneous graph → pass through a **Graph Neural Network** → project donors and recipients into a **shared embedding space** → compute a compatibility score via **dot product** → output P(Donor | Recipient).

**Key results:**
- This paper is largely **conceptual/architectural** — it presents the graph construction and GNN pipeline design in detail but does **not report trained-model performance metrics** (no AUROC, accuracy, or survival outcomes are given in this short paper). It positions the GNN training and evaluation as **future work**.

**How it works, structurally:** Multi-relational **graph representation learning**. Instead of one scalar score (like HMS), it encodes several different *kinds* of relationships as different edge types in the same graph, then lets a GNN learn a compatibility embedding rather than relying on a single hand-engineered formula.

---

### 2.3 Melehy et al. (2026) — Liver Transplant Matching with Offline Reinforcement Learning

**What the paper is about:**
Unlike the other two papers (which are essentially "given a donor, pick the best static match"), this paper reframes donor-recipient matching for **liver** transplantation as a **sequential decision-making problem over time**: at every point on the waitlist, should the clinician **wait**, **delist**, or **transplant** the patient with an available organ?

**What they actually did:**
- Used SRTR data: 45,635 liver-transplant candidates (2017–2022), converted into **Markov Decision Process (MDP) episodes** — each patient's MELD score (severity-of-liver-disease score) over time forms a trajectory of states.
- At each state (time step), the possible **actions** are: Wait, Delist, or Transplant (with a specific available donor).
- Designed a **reward function** that combines:
  - Short-term reward/penalty from the change in MELD score.
  - Long-term reward/penalty for terminal outcomes: graft failure, successful transplant, waitlist death, or recovery-delisting.
- Trained an **offline Reinforcement Learning** model using **Conservative Q-Learning (CQL)** — a Double DQN variant with a conservatism regularizer, since the model must learn from historical data without live experimentation.
- Compared against baselines: simple MELD-threshold rules (e.g., "transplant whenever MELD ≥ 15"), and static supervised-learning predictive models (logistic regression, XGBoost).

**Key results:**
- The RL model avoided **73%** of donor-recipient pairs that led to real-world graft failure or death (GFPR), while still preserving **93%** of the real successful transplants (GSPR).
- It identified alternative donors for **47%** of patients who, in reality, died waiting.
- It outperformed both naive MELD-threshold rules and static ML predictive models on these clinically meaningful metrics simultaneously (the static/threshold models could only optimize one outcome at the expense of another).

**How it works, structurally:** This is a **temporal, policy-learning** approach — it doesn't just score a single donor-recipient pair; it learns *when* to act across a whole patient trajectory, balancing competing risks (death from waiting vs. death from a bad transplant) over time.

---

## 3. Side-by-Side Comparison

| Aspect | Syed et al. (2024) | Majouni et al. (2025) | Melehy et al. (2026) |
|---|---|---|---|
| Organ | Kidney | Kidney | Liver |
| Core technique | Rule-based greedy simulation + immunogenicity score (HMS) | Heterogeneous bipartite graph + GNN (proposed) | Offline Reinforcement Learning (CQL / MDP) |
| Data source | SRTR | SRTR | SRTR |
| Matching philosophy | Best static match per patient at allocation time | Learned similarity/compatibility embedding | Sequential decision over time (wait/delist/transplant) |
| Time dimension considered? | No (single-point allocation) | Only partially (time-based edges as a concept) | Yes — core to the model |
| Validated with outcomes? | Yes (graft-survival gain, p<0.001) | No (architecture proposed, no reported evaluation) | Yes (GFPR, GSPR, CIR, CRR metrics) |
| Computational complexity | Low–moderate (greedy search + scoring) | Very high (GNN training, 18M edges) | Very high (deep RL training, 214K+ states) |
| Real-time / interactive use | No — batch simulation | No — research prototype | No — offline analysis, "not intended for operational use" (stated by authors) |
| Requires high-resolution HLA typing | Yes | Partially (uses HLA mismatch as one DDS input) | No (liver uses MELD, not HLA) |

---

## 4. Gaps Identified Across the Three Papers

After reviewing all three papers together, the following gaps stand out — and these gaps are the actual **justification** for a DSA-first project like the Smart Organ Transplant Matching System:

1. **All three approaches are computationally heavy, data-hungry, and research-grade — not deployable as a lightweight, transparent decision-support tool.**
   Syed et al. need high-resolution HLA imputation; Majouni et al. need a GNN trained on an 18-million-edge graph; Melehy et al. need to train a Q-network over 1.25 million iterations. None of these are things a hospital's waitlist software could run instantly on a laptop or explain to a coordinator in real time.

2. **None of the three focuses on the *data-structure* problem of maintaining a live, constantly changing waiting list.**
   All three treat the waiting list as a **static batch dataset** (a fixed SRTR snapshot) that is processed once, offline. In reality, patients are added, removed, or re-prioritized continuously. None of the papers discuss how to efficiently **insert, delete, search, or re-rank** patients in real time — this is precisely a classic tree/heap data-structures problem.

3. **Explainability and traceability are weak, especially in the ML/GNN and RL approaches.**
   Majouni et al.'s GNN produces a similarity score from a learned embedding space that is hard for a clinician to interpret. Melehy et al.'s CQL model is a black-box Q-function. Only Syed et al.'s HMS-based approach is reasonably transparent, but it still requires specialized immunogenetics expertise to interpret.

4. **Geographic/paired-exchange chains and urgency-based prioritization are handled inconsistently.**
   Syed et al. handle geography (250-mile radius) but not urgency ranking. Majouni et al. mention time-based/urgency edges only conceptually, without an evaluated implementation. Melehy et al. handle severity (MELD) over time but not multi-donor chain relationships (e.g., paired kidney exchange).

5. **No paper combines "fast search over a large candidate pool" with "graph-based compatibility" with "urgency-based prioritization" in one lightweight, unified structure.**
   Each paper solves one slice of the problem (matching score, graph relationships, or sequential timing) using a heavyweight technique, but none integrates ordered search + priority ranking + relationship-graph traversal into a single efficient system.

---

## 5. How the Proposed Solution (Smart Organ Transplant Matching System) Differs

The current project deliberately does **not** try to replicate the statistical/ML sophistication of these papers (HLA immunogenicity modeling, GNN embeddings, or offline RL policies are out of scope for a DSA-II course project). Instead, it targets the structural gap identified above: **efficient, explainable, real-time organization of the matching problem using classical data structures.**

| Research Paper Technique | Proposed Project's Analogous Piece | Why It's Different |
|---|---|---|
| Greedy HMS-based donor search (Syed et al.) | **Graph / adjacency list** of donor–recipient compatibility (blood group, tissue type) | Same idea of "search compatible donors for a recipient," but using a simple, explainable adjacency structure instead of amino-acid-level immunogenicity scoring — feasible to compute instantly without specialized lab data. |
| Multi-relational compatibility graph + GNN (Majouni et al.) | **Graph representation of donor–recipient relationships**, including potential paired-exchange chains | Keeps the *idea* of representing multiple compatibility relationships as a graph, but replaces the learned GNN embedding with direct graph traversal (e.g., BFS/DFS or adjacency lookups) — transparent and traceable, no training data or GPU required. |
| MELD-based sequential decisions over time (Melehy et al.) | **Max-Heap based urgency prioritization** of the recipient waiting list | Captures the same core need — "who should be prioritized right now" — using a heap's O(log n) insert/extract-max instead of a trained RL policy. Much simpler to maintain and reason about, at the cost of not learning long-term optimal timing strategies. |
| Static batch allocation on a fixed dataset (all three) | **AVL Tree** for the waiting list, enabling live insert/delete/search as patients register, get transplanted, or are removed | Directly addresses Gap #2 — none of the three papers model the waitlist as a dynamic, continuously updated structure. |
| Black-box scoring (GNN, RL) | Clearly defined tree/heap/graph operations with visible intermediate state | Directly addresses Gap #3 (explainability) — every match/priority decision can be traced back to a specific comparison, traversal, or heap operation. |

**In short:** the reviewed papers optimize primarily for *predictive/statistical accuracy* using domain-specific medical scoring (HLA/HMS), learned graph embeddings (GNN), or learned temporal policies (RL) — all of which require large labeled datasets, domain expertise, and heavy computation, and none of which is intended for real-time list management (Melehy et al. explicitly state their model is "not intended for operational use in its current form"). The proposed Smart Organ Transplant Matching System instead targets the **systems/data-structures layer that all three papers implicitly assume already exists** — a fast, transparent, continuously maintainable way to store, search, rank, and connect donor and recipient records — using Trees (waitlist organization), Heaps (urgency prioritization), and Graphs (compatibility relationships), which are the Unit 1 and Unit 2 topics of the DSA-II course.

---

## 6. Conclusion

All three papers confirm that donor-recipient matching is a genuinely hard, high-stakes problem that current allocation systems handle imperfectly — whether the limitation is geographic-only matching without deep immunogenicity (implicit in the real-world baseline Syed et al. compare against), a lack of trained/evaluated learning models (Majouni et al.), or the acknowledged non-operational status of state-of-the-art RL models (Melehy et al.). None of them, however, addresses the more foundational systems question of how to organize a constantly changing candidate/donor pool for fast search, ranking, and relationship-tracing — which is the specific gap this PBL project's tree-, heap-, and graph-based design is intended to explore at an educational/prototype level.

---

## 7. References

1. Syed, F.J., Bekbolsynov, D., Green II, R.C., Kaur, D., Ekwenna, O., Sindhwani, P., Rees, M., & Stepkowski, S. (2024). Potential of new 250-nautical mile concentric circle allocation system for improving the donor/recipient HLA matching: Development of new matching algorithm. *Transplant Immunology*, 87, 102146. https://doi.org/10.1016/j.trim.2024.102146

2. Majouni, S., Tennankore, K., Abidi, S., Vinson, A., Worthen, G., & Abidi, S.S.R. (2025). A Heterogeneous Bipartite Graph Framework for Donor-Recipient Matching in Kidney Transplantation. *Studies in Health Technology and Informatics*.

3. Melehy, A., Feng, J., Amara, D., Agopian, V.G., & Bui, A.A.T. (2026). Liver transplant donor-recipient matching with offline reinforcement learning. *npj Digital Medicine*, 9, 351. https://doi.org/10.1038/s41746-026-02529-1