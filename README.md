# Smart Organ Transplant Matching System

> A DSA-based organ transplant matching system that intelligently connects donors with suitable recipients using efficient waitlist search, compatibility-relationship modelling, urgency-based prioritization, and fast candidate retrieval.

---

## Project Overview

The **Smart Organ Transplant Matching System** aims to go beyond manual, ad-hoc donor-recipient matching.

Instead of relying on slow manual comparison of waiting lists, the proposed system evaluates multiple factors such as:

- Blood Group Compatibility
- Tissue / HLA Compatibility
- Medical Urgency Score
- Organ Type
- Registration Date / Waiting Time
- Hospital / Location

The core focus of this project is to demonstrate how **Data Structures and Algorithms** can be applied to build an efficient, transparent organ-matching engine — organizing a constantly changing waiting list and tracing donor–recipient compatibility without relying on heavyweight machine-learning models.

---

## Proposed Workflow

```
Donor / Recipient Registration
              ↓
   Blood Group & Organ-Type Filtering
              ↓
   Graph-Based Compatibility Discovery
              ↓
      AVL Tree — Waitlist Retrieval
              ↓
   Tissue / HLA Compatibility Check
              ↓
   Urgency Scoring (Medical Severity)
              ↓
       Max Heap — Priority Ranking
              ↓
   Best-Matched Donor–Recipient Pair
```

---

## DSA Used

| DSA | Purpose |
|---|---|
| **Binary Tree** | Hierarchical organization of recipient waiting-list records |
| **AVL Tree** | Balanced, efficient search/insert/delete as patients register or leave the list |
| **Graph** | Donor–Recipient–Organ compatibility relationships |
| **Adjacency List / Matrix** | Efficient storage of compatibility connections, including paired-exchange chains |
| **BFS / DFS** | Exploring compatible donors and multi-hop exchange chains |
| **Heap (Max Heap)** | Priority-based ranking of recipients by medical urgency |
| **Tree Traversal** | Systematic listing/processing of waiting-list records |

### Why these structures?

- **AVL Tree** → Keeps the recipient waiting list balanced for fast O(log n) search, insert, and delete as the list constantly changes
- **Graph** → Represents the many-to-many compatibility relationships between donors, recipients, and organ types (including paired kidney exchanges)
- **BFS/DFS** → Explores connected/compatible donors and traces possible exchange chains
- **Max Heap** → Efficiently retrieves the most medically urgent recipient first, without re-sorting the entire list

---

## Matching Model

The planned matching/urgency score combines:

```
Blood Group Compatibility
+ Tissue / HLA Compatibility
+ Medical Urgency
+ Waiting Time
+ Organ Viability Window
```

The exact weighting will be finalized and evaluated during implementation.

---

## Research

Review 1 covered three major research directions:

1. **250-Nautical Mile HLA Allocation Simulation (Syed et al., 2024)** — greedy, rule-based donor allocation using an amino-acid-level immunogenicity score (HMS) and KDPI thresholds, benchmarked against real SRTR outcomes.
2. **Heterogeneous Bipartite Graph + GNN Framework (Majouni et al., 2025)** — multi-relational donor–recipient graph (compatibility, knowledge-driven, blood-type, time-based edges) intended for Graph Neural Network–based compatibility scoring.
3. **Offline Reinforcement Learning for Liver Matching (Melehy et al., 2026)** — models donor-recipient matching as a sequential wait/delist/transplant decision problem using Conservative Q-Learning over MELD-score trajectories.

### Research-Gap Identification

- All three approaches are **computationally heavy and data-hungry** (high-resolution HLA imputation, GNN training over millions of edges, RL training over 1M+ iterations) — not deployable as a lightweight, real-time tool.
- None of them treat the waiting list as a **live, continuously changing structure**; all process a fixed, static batch snapshot of data.
- The GNN and RL approaches are largely **black-box / hard to explain** to a clinician or coordinator.
- Urgency-based prioritization and geographic/graph-based compatibility are handled **separately and inconsistently** across the three papers — none unify fast search, urgency ranking, and relationship-graph traversal in one lightweight system.

### Research Direction

The project explores extending compatibility-based matching into:

**Dynamic waitlist management (AVL Tree) + Graph-based compatibility discovery (Adjacency List/BFS-DFS) + Urgency-based Top-priority selection (Max Heap)**

---

## Current Progress — Review 1

### Completed

- Problem understanding
- Requirement analysis
- Literature review (3 research papers)
- Research-gap identification
- DSA-II Unit 1: Trees
- DSA-II Unit 2: Graphs
- DSA-to-project mapping
- Initial data model (donor/recipient records)
- Initial graph model (compatibility relationships)
- Matching workflow design
- DSA implementation planning

### Next

- AVL Tree implementation (waiting list)
- Graph + Adjacency List implementation
- BFS / DFS for compatibility discovery
- Candidate filtering (blood group, organ type)
- Urgency-score calculation
- Max Heap implementation
- Priority-based donor–recipient matching
- Frontend & backend integration
- Testing and performance evaluation

> **Current status:** Review 1 — Research & Initial DSA Design
> **Progress:** 25%
> **Implementation:** Planned for Review 2

---

## Future Scope

- Explainable match recommendations (trace every decision back to a tree/heap/graph operation)
- Paired-exchange chain discovery (multi-donor/multi-recipient cycles)
- Geographic/location-aware matching
- Dynamic re-prioritization as urgency changes
- Waitlist analytics and trend tracking
- Integration with real registry-style datasets for evaluation

---

## Academic Focus

The main objective is **not just to build another matching application**.

The project focuses on demonstrating how **DSA can solve the underlying waitlist-management and compatibility-retrieval problem efficiently**, in contrast to the heavier ML/GNN/RL techniques used in current research literature.

```
AVL Tree → Dynamic Waitlist Management
Graph → Compatibility Discovery
BFS/DFS → Exchange-Chain Exploration
Max Heap → Urgency-Based Top Priority Selection
```

**Course:** Data Structure and Algorithms-II (CCSE0301)
**Project:** Smart Organ Transplant Matching System
**Student:** Anirudh Yadav (2501330100073)
**Review:** 1
**Progress:** 25%