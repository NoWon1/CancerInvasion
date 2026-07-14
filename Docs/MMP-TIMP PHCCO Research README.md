# Modeling Cell-Type-Specific MMP Dynamics and ECM Remodeling in the Tumor Microenvironment

> A Python-based CompuCell3D simulation of tumor invasion, extracellular-matrix remodeling, protease–inhibitor dynamics, and immune-cell exclusion.

## At a Glance

| Item | Description |
|---|---|
| **Research area** | Computational oncology and tumor-microenvironment modeling |
| **Core framework** | Cellular Potts Model / Glazier–Graner–Hogeweg model |
| **Simulation platform** | CompuCell3D |
| **Primary language** | Python |
| **Main biological signals** | Matrix metalloproteinases, tissue inhibitors of metalloproteinases, growth factors, and chemoattractants |
| **Primary outputs** | Tumor invasion morphology, extracellular-matrix degradation, cell population dynamics, and immune infiltration |

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Research Objectives](#research-objectives)
- [Computational Framework](#computational-framework)
  - [Cellular Potts Model](#cellular-potts-model)
  - [Hamiltonian](#hamiltonian)
  - [Monte Carlo Step Logic](#monte-carlo-step-logic)
- [Model System](#model-system)
  - [Agent-Based Components](#agent-based-components)
  - [Chemical Fields](#chemical-fields)
- [Implementation and Parameterization](#implementation-and-parameterization)
  - [Adhesion Energy Matrix](#adhesion-energy-matrix)
  - [Cellular and Structural Constraints](#cellular-and-structural-constraints)
  - [Diffusion and Reaction Parameters](#diffusion-and-reaction-parameters)
- [Results and Key Findings](#results-and-key-findings)
  - [Impact of MMP Diffusion](#impact-of-mmp-diffusion)
  - [Tumor Density and Heterogeneity](#tumor-density-and-heterogeneity)
  - [ECM Architecture and T-Cell Exclusion](#ecm-architecture-and-t-cell-exclusion)
- [Biological and Therapeutic Implications](#biological-and-therapeutic-implications)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Repository Structure](#repository-structure)
  - [Running the Simulation](#running-the-simulation)
- [Conclusion](#conclusion)
- [References](#references)

---

## Project Overview

Metastasis is the primary driver of cancer-related mortality. It involves tumor-cell detachment, migration through the extracellular matrix (ECM), intravasation, circulation, and colonization of distant organs [[1]](#ref-1) [[2]](#ref-2) [[3]](#ref-3). Tumor invasion is strongly regulated by the tumor microenvironment (TME), which includes tumor cells, stromal components, immune cells, and the structural ECM scaffold [[1]](#ref-1) [[4]](#ref-4).

Matrix metalloproteinases (MMPs) are zinc-dependent endopeptidases that degrade ECM proteins such as collagen and laminin [[1]](#ref-1) [[2]](#ref-2). Their activity also releases sequestered growth factors and produces bioactive matrix fragments that alter cell behavior [[1]](#ref-1) [[5]](#ref-5) [[6]](#ref-6). Tissue inhibitors of metalloproteinases (TIMPs) regulate this activity by forming stable 1:1 complexes with active MMPs [[1]](#ref-1) [[7]](#ref-7).

This repository documents a research project developed for the **Param Hansa Centre for Computational Oncology (PHCCO) Summer Training Program**. The project uses a fully Python-based CompuCell3D simulation to examine how pro-tumorigenic MMPs, immune-regulated MMPs, and TIMP secretion shape tumor invasion and ECM integrity [[2]](#ref-2).

## Problem Statement

The collective spatial effects of heterogeneous tumor and immune-cell populations—each producing different levels of MMPs and TIMPs—are difficult to predict experimentally [[8]](#ref-8) [[9]](#ref-9). Tumor heterogeneity, including epithelial-like and mesenchymal-like cancer-cell states, further complicates invasion dynamics [[10]](#ref-10).

The model addresses two central questions:

1. How do MMP diffusion and tumor-cell density alter the transition between cohesive and dispersed invasion?
2. How does ECM remodeling influence immune-cell access to the tumor core?

## Research Objectives

1. Integrate an agent-based model to simulate tumor and immune-cell interactions in diffusing MMP and TIMP fields [[1]](#ref-1) [[2]](#ref-2).
2. Quantify how MMP diffusion constants influence cohesive collective invasion versus dispersed individual migration [[2]](#ref-2).
3. Investigate MMP8, primarily secreted by neutrophils, as a potential metastasis suppressor that strengthens cell–ECM adhesion and modulates epithelial–mesenchymal transition [[1]](#ref-1).
4. Model immune exclusion, where dense or improperly remodeled ECM prevents cytotoxic T lymphocytes from reaching the tumor mass [[4]](#ref-4) [[7]](#ref-7).

## Computational Framework

The simulation uses the **Cellular Potts Model (CPM)**, also called the **Glazier–Graner–Hogeweg (GGH) model**, implemented in CompuCell3D [[1]](#ref-1) [[7]](#ref-7). This framework combines discrete cellular mechanics with continuous partial differential equation solvers for chemical fields, making it suitable for multiscale tumor modeling [[8]](#ref-8) [[11]](#ref-11).

### Cellular Potts Model

Cells occupy collections of lattice sites. Their movement and shape changes emerge from stochastic pixel-copy attempts that are accepted or rejected according to the change in effective system energy.

### Hamiltonian

The total effective energy is represented as:

$$
H = H_{\text{adhesion}} + H_{\text{volume}} + H_{\text{surface}} + H_{\text{chemotaxis}}
$$

The terms represent:

- **Adhesion energy:** Contact energy between cell types, ECM components, and the surrounding medium. Lower contact energy $J$ indicates stronger adhesion [[9]](#ref-9).
- **Volume constraint:** Penalizes deviation from target volume $V_t$.
- **Surface constraint:** Penalizes deviation from target surface area $S_t$.
- **Chemotaxis energy:** Biases movement along relevant chemical gradients.

Volume and surface penalties are controlled by Lagrange multipliers $\lambda_v$ and $\lambda_s$ [[12]](#ref-12) [[13]](#ref-13).

### Monte Carlo Step Logic

Each Monte Carlo Step (MCS) follows this sequence:

1. **Pixel selection:** Randomly select a lattice site and an adjacent neighbor [[14]](#ref-14).
2. **Energy calculation:** Compute the change in effective energy, $\Delta H$, caused by copying the source-cell index into the target site [[1]](#ref-1).
3. **Acceptance rule:**
   - Accept automatically when $\Delta H \leq 0$.
   - When $\Delta H > 0$, accept with probability:

$$
P(\text{accept}) = e^{-\Delta H / T}
$$

where $T$ represents effective membrane fluctuation [[1]](#ref-1) [[14]](#ref-14).

4. **Time scaling:** Approximately 1,000 MCS corresponds to 24–36 hours of biological time; the model uses an effective scale of about 86.4 seconds per MCS [[15]](#ref-15).

## Model System

The model represents a heterogeneous tumor environment containing epithelial-like cancer cells, mesenchymal-like cancer cells, immune cells, and a degradable ECM.

### Agent-Based Components

| Agent | Modeled behavior |
|---|---|
| **Cancer1 — epithelial-like** | High cell–cell adhesion and low cell–ECM adhesion; forms cohesive spheroids and tends to invade collectively [[1]](#ref-1) [[2]](#ref-2). |
| **Cancer2 — mesenchymal-like** | Low cell–cell adhesion and high cell–ECM adhesion; displays dispersed, motile behavior associated with advanced invasion [[1]](#ref-1) [[2]](#ref-2). |
| **CD8+ T cells** | Generated at the model boundary, chemotax toward the tumor, and eliminate tumor cells according to a configurable killing probability [[1]](#ref-1) [[2]](#ref-2) [[7]](#ref-7). |
| **Extracellular matrix** | Multicomponent collagen–laminin structure. Laminin transitions to a lysed state when local proteolytic conditions exceed the degradation threshold [[1]](#ref-1) [[2]](#ref-2). |

### Chemical Fields

The chemical environment is simulated with CompuCell3D's `DiffusionSolverFE` steppable.

#### MMP and TIMP

Cancer cells secrete MMPs and TIMPs after contact with laminin. ECM degradation occurs only when the local ratio satisfies:

$$
\frac{\text{MMP}}{\text{TIMP}} > 2.0
$$

[[1]](#ref-1)

#### Growth Factor

The ECM releases growth factor during cell interaction or matrix degradation. Cancer-cell `TargetVolume` is modeled as a function of local growth-factor concentration, enabling nutrient-dependent growth [[1]](#ref-1).

#### Chemoattractant

Tumor cells produce a chemoattractant that recruits immune cells from the model boundary. This creates a dynamic competition between tumor expansion and immune-mediated destruction [[1]](#ref-1) [[2]](#ref-2).

## Implementation and Parameterization

Parameters were derived from experimental and computational literature, including work by Kumar *et al.* and Prasanna *et al.*, to reproduce biologically plausible invasion phenotypes [[1]](#ref-1) [[10]](#ref-10) [[16]](#ref-16) [[17]](#ref-17).

### Adhesion Energy Matrix

Lower contact energy indicates stronger adhesion [[13]](#ref-13).

| Agent Type 1 | Agent Type 2 | Contact Energy $J$ |
|---|---:|---:|
| Medium | Medium | 0 |
| Medium | Cancer cell | 15 |
| Medium | ECM fiber | 0 |
| Cancer cell | Cancer cell | 5 |
| Cancer cell | ECM fiber | 10 |
| ECM fiber | ECM fiber | 1 |

### Cellular and Structural Constraints

| Cell Type | Target Volume (pixels) | $\lambda_{\text{volume}}$ | Target Surface | $\lambda_{\text{surface}}$ |
|---|---:|---:|---:|---:|
| Cancer cell | 100 | 5.0 | 35 | 2.0 |
| ECM fiber | 15 | 100.0 | 20 | 50.0 |
| Medium | N/A | 0 | N/A | 0 |

### Diffusion and Reaction Parameters

The MMP diffusion constant is the primary sensitivity-analysis variable [[13]](#ref-13).

| Field / Property | Parameter | Numerical Value |
|---|---|---:|
| MMP diffusion constant | `D_mmp` | 0.005–0.05 |
| MMP decay constant | `delta_mmp` | 0.005 |
| Secretion rate | `lambda_sec` | 0.01–0.1 s⁻¹ |
| Degradation threshold | `MMP/TIMP` ratio | > 2.0 |
| Neighbor order | `NeighborOrder` | 1–2 |

## Results and Key Findings

Tumor invasion was quantified through cell-count and total-cell-volume trajectories over time [[1]](#ref-1).

### Impact of MMP Diffusion

| Diffusion regime | Observed behavior |
|---|---|
| **Low — $D = 0.005$** | Proteolysis remains near the cell membrane, producing irregular localized paths and jagged invasion boundaries. Localized TIMP activity leads to inconsistent control, and individual cells may detach prematurely [[2]](#ref-2). |
| **Intermediate — $D = 0.01$–$0.02$** | Produces the most robust and compact collective invasion. MMPs diffuse far enough to generate a smooth path while remaining concentrated enough for TIMPs to maintain an inhibitory boundary [[2]](#ref-2). |
| **High — $D = 0.05$** | MMPs become diluted across a larger area. Local concentration may fall below the degradation threshold unless tumor density is high, leading to erratic invasion and weak inhibitor control [[1]](#ref-1) [[2]](#ref-2). |

**Central finding:** Intermediate MMP diffusion produced the most organized collective invasion front.

### Tumor Density and Heterogeneity

Higher initial tumor density produced a collective proteolytic cloud that degraded the ECM more uniformly than isolated cells [[2]](#ref-2).

Epithelial-like Cancer1 cells showed strong invasion as a cohesive mass but were more sensitive to excessive MMP diffusion. Mesenchymal-like Cancer2 cells were less dependent on a concentrated proteolytic front and continued to migrate through partially degraded ECM using stronger cell–ECM adhesion [[1]](#ref-1) [[2]](#ref-2).

### ECM Architecture and T-Cell Exclusion

Dense collagen regions and areas with low MMP diffusion created physical barriers to immune-cell movement. Even under strong chemotactic signaling, T cells accumulated at the tumor periphery and often failed to reach the internal tumor core [[4]](#ref-4) [[7]](#ref-7).

This supports the interpretation that remodeled ECM can act as a **physical shield** against immune surveillance.

## Biological and Therapeutic Implications

The results indicate that metastatic potential depends not only on MMP production but also on enzyme transport, inhibitor localization, tumor density, and matrix resistance [[8]](#ref-8) [[9]](#ref-9).

Key implications include:

- **Transport-aware MMP targeting:** Modifying protease transport or MMP:TIMP stoichiometry may be more effective than simply reducing total MMP abundance [[1]](#ref-1) [[3]](#ref-3).
- **Matrix normalization:** The anti-metastatic role of MMP8 supports strategies that favor adhesion and ECM stability rather than indiscriminate matrix degradation [[1]](#ref-1) [[4]](#ref-4).
- **Combination immunotherapy:** Effective immune treatment may require simultaneous reduction of ECM-mediated exclusion through matrix-degrading agents or adhesion modulators [[4]](#ref-4) [[7]](#ref-7).
- **Computational treatment testing:** The model provides a platform for evaluating how protease inhibition, matrix remodeling, and immune-cell activity interact before experimental validation.

## Getting Started

### Prerequisites

- CompuCell3D with Python 3 support [[2]](#ref-2).
- Familiarity with CompuCell3D project components:
  - `.cc3d` project file
  - Python steppables
  - XML configuration [[18]](#ref-18) [[19]](#ref-19)

### Repository Structure

```text
project-root/
├── Simulation.py
├── Steppables.py
├── Simulation.xml
└── <project-name>.cc3d
```

| File | Purpose |
|---|---|
| `Simulation.py` | Initializes the simulation and registers steppables. |
| `Steppables.py` | Implements MMP/TIMP secretion, ECM degradation, immune-cell recruitment, tumor-cell proliferation, and mitosis [[1]](#ref-1) [[18]](#ref-18). |
| `Simulation.xml` | Defines lattice dimensions, Potts parameters, cell types, diffusion fields, and initial conditions [[13]](#ref-13) [[18]](#ref-18). |
| `<project-name>.cc3d` | CompuCell3D project definition used by Player or Twedit++. |

### Running the Simulation

1. Launch **CompuCell3D Player** or **Twedit++**.
2. Open the repository's `.cc3d` project file.
3. Configure experimental parameters, such as:
   - MMP `DiffusionConstant` in `Simulation.xml`
   - `killing_probability` in `Steppables.py`
   - Tumor density and cell-type proportions
   - MMP and TIMP secretion rates
4. Run the simulation.
5. Monitor:
   - Cell sorting and invasion morphology
   - Chemical concentration gradients
   - ECM degradation and lysed regions
   - Tumor and immune-cell population dynamics [[2]](#ref-2) [[14]](#ref-14)

## Conclusion

This project demonstrates that cell-type-specific proteolytic dynamics strongly influence tumor invasion. The spatial regulation of MMPs and TIMPs—together with diffusion, tumor heterogeneity, and matrix structure—determines whether invasion remains cohesive or becomes dispersed and metastatic [[1]](#ref-1) [[2]](#ref-2).

The model also shows how ECM architecture can exclude T cells from the tumor core. These findings provide a computational foundation for studying matrix-targeted therapies, immune-access strategies, and combination treatments [[3]](#ref-3) [[4]](#ref-4) [[8]](#ref-8).

## References

> **Note:** Citation numbering has been preserved from the source document.

1. <a id="ref-1"></a>**Final Report — IISc PHCCO**.
2. <a id="ref-2"></a>**Report**.
3. <a id="ref-3"></a>**The role of MMPs in metastasis and tumorigenesis: ECM remodeling**. ResearchGate.
4. <a id="ref-4"></a>**Extracellular matrix remodeling in tumor progression and immune escape: From mechanisms to treatments**. PubMed Central.
5. <a id="ref-5"></a>**Matrix Metalloproteinases in the senescence-associated secretory phenotype: Remodeling the tumor microenvironment**.
6. <a id="ref-6"></a>**Matrix Metalloproteinases Shape the Tumor Microenvironment in Cancer Progression**. PubMed Central.
7. <a id="ref-7"></a>**PHCCO Project Document**.
8. <a id="ref-8"></a>**An Interplay Between Reaction–Diffusion and Cell–Matrix Adhesion Regulates Multiscale Invasion in Early Breast Carcinomatosis**. PubMed Central.
9. <a id="ref-9"></a>**Interactive dynamics of matrix adhesion and reaction–diffusion predict diverse multiscale strategies of cancer-cell invasion**. bioRxiv.
10. <a id="ref-10"></a>**Formation of motile cell clusters in heterogeneous model tumors: The role of cell–cell alignment**. arXiv.
11. <a id="ref-11"></a>**Cellular Potts Modeling of Tumor Growth, Tumor Invasion, and Tumor Evolution**. Frontiers.
12. <a id="ref-12"></a>**Developing a CompuCell3D Simulation**.
13. <a id="ref-13"></a>**CancerInvasion.xml**.
14. <a id="ref-14"></a>**Introduction to CompuCell3D**.
15. <a id="ref-15"></a>**Agent-based modeling reveals impacts of cell adhesion and matrix remodeling on cancer collective-cell migration phenotypes**. bioRxiv.
16. <a id="ref-16"></a>**MedChat POC Technical Documentation**.
17. <a id="ref-17"></a>**A hybrid computational model of cancer spheroid growth with ribose-induced collagen stiffening**. PubMed Central.
18. <a id="ref-18"></a>**Create Your First CompuCell3D Project**. CC3D Reference Manual 4.9.0.
19. <a id="ref-19"></a>Swat, M. H., Belmonte, J. M., and Zaitlen, B. L. **CompuCell3D Python Scripting Manual**, Version 3.6.0.
20. <a id="ref-20"></a>**CompuCell3D Reference Manual — `docs/cc3d_python.rst`**. GitHub.
21. <a id="ref-21"></a>**Scripting inside CompuCell3D**.