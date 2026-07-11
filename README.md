**TL;DR Summary:**

* This repository houses a 100% Python-based agent-based model (ABM) developed in CompuCell3D (CC3D).


* The simulation investigates how the spatial dynamics of Matrix Metalloproteinases (MMPs) and Tissue Inhibitors of Metalloproteinases (TIMPs) govern tumor invasion and Extracellular Matrix (ECM) remodeling.


* It integrates heterogeneous tumor cell populations, immune cell infiltration, and diffusing proteolytic fields to quantify conditions that lead to cohesive collective invasion versus immune exclusion.



---

# Modeling Cell-Type-Specific MMP Dynamics and ECM Remodeling

## Table of Contents

1. [Project Overview]
2. [Computational Framework]
3. [Biological Agents and Chemical Fields]
4. [Key Findings]
5. [Implementation and Setup]
6. [Repository Structure]

## Project Overview

Metastasis is a multi-step process fundamentally regulated by the tumor microenvironment (TME), which includes tumor cells, stromal components, immune cells, and the structural scaffold of the ECM. Central to matrix remodeling is the activity of MMPs, which degrade ECM components like collagen and laminin, facilitating tumor cell transit and releasing sequestered growth factors. To maintain homeostasis, MMP activity is tightly controlled by TIMPs through stable 1:1 stoichiometric complexes.

This project simulates the spatial interactions of tumor and immune cells under varying MMP and TIMP diffusion rates. The primary objectives are:

* Integrating an agent-based model to simulate spatial cellular interactions in the presence of diffusing proteolytic fields.


* Quantifying how MMP diffusion constants dictate the transition between cohesive collective invasion and dispersed individual migration.


* Modeling the "immune exclusion" phenomenon where a dense or poorly remodeled ECM prevents cytotoxic T-lymphocytes (CTLs) from reaching the tumor core.



## Computational Framework

The simulation is built upon the Cellular Potts Model (CPM), also known as the Glazier-Graner-Hogeweg (GGH) model, implemented via CompuCell3D.

* **The Hamiltonian:** System evolution is driven by the minimization of total effective energy. The Hamiltonian includes adhesion, volume, surface, and chemotaxis constraints.


* 
**Monte Carlo Steps (MCS):** The simulation utilizes successive MCS logic evaluating pixel-copy attempts against the Hamiltonian. Unfavorable configurations may be accepted based on a Boltzmann probability function to prevent the system from getting trapped in local energy minima.


* 
**Time Scaling:** 1000 MCS is calibrated to approximately 24 to 36 hours of real-time.



## Biological Agents and Chemical Fields

The model utilizes a heterogeneous environment with specific agent behaviors and chemical reactions:

**Agent-Based Components:**

* **Cancer1 (Epithelial-like):** Exhibits high cell-cell adhesion and low cell-ECM adhesion. These cells form stable, cohesive spheroids.


* 
**Cancer2 (Mesenchymal-like):** Demonstrates low cell-cell adhesion and high cell-ECM adhesion, representing a motile, dispersed phenotype.


* 
**Immune Cells (CD8+ T cells):** Generated at the periphery, these cells migrate via chemotaxis and execute a defined killing probability upon contact with tumor cells.


* **Extracellular Matrix (ECM):** Composed of collagen and laminin fibers. Laminin transitions to a lysed state upon proteolytic degradation.



**Chemical Fields:**

* **MMP and TIMP Dynamics:** Secreted by cancer cells upon contact with laminin. The matrix degrades only if the local MMP:TIMP concentration ratio exceeds 2.0.


* **Growth Factor (GF):** Secreted by the ECM during interaction or degradation. It drives nutrient-dependent growth by increasing the target volume of cancer cells.


* 
**Chemoattractant:** Secreted by tumor cells to recruit immune cells, establishing a dynamic competition between tumor expansion and immune destruction.



## Key Findings

Simulation outputs quantify invasion through cell volume and count dynamics over time.

* **Low MMP Diffusion (D = 0.005):** Proteolytic activity remains localized to the cell membrane. This causes irregular invasion paths and ineffective regulation by TIMPs, resulting in jagged boundary degradation.


* **Intermediate MMP Diffusion (D = 0.01 - 0.02):** Produces the most robust, compact, and directional collective invasion. The MMP signal creates a smooth path while remaining concentrated enough for TIMPs to maintain an inhibitory boundary.


* **High MMP Diffusion (D = 0.05):** The MMP signal becomes excessively diluted. Matrix degradation becomes erratic, and invasion only succeeds when tumor densities overcome the dilution effect.


* **Tumor Density and Heterogeneity:** Higher initial tumor densities create a collective "proteolytic cloud" leading to uniform ECM degradation. Cancer1 cells show higher invasion potential but are highly sensitive to MMP signal dilution compared to Cancer2 cells.


* **Immune Exclusion:** Dense collagen networks or regions with low MMP diffusion function as structural barriers. Immune cells become trapped at the periphery, validating the concept of the ECM as a physical shield against immune surveillance.



## Implementation and Setup

**Prerequisites:**

* CompuCell3D (Standard installation compatible with Python 3.x).


* Basic understanding of CC3D project structures (.cc3d, XML, Python Steppables).



**Running the Simulation:**

1. Clone the repository and launch the CompuCell3D Player or Twedit++.


2. Open the `.cc3d` project file.


3. Adjust parameters directly in the configuration files (e.g., `MMP DiffusionConstant` in the XML or `killing_probability` in the Python Steppables).


4. Execute the simulation to monitor real-time visualization of cell sorting, chemical gradients, and matrix degradation.



## Repository Structure

The repository strictly follows the supported CC3D format for modularity and portability.

* 
`CancerInvasion.cc3d`: The main project manifest file linking the scripts.


* 
`Simulation/CancerInvasion.xml`: Defines lattice dimensions, Potts parameters (Temperature, NeighborOrder), cellular energy constraints, and initial field diffusion conditions.


* 
`Simulation/CancerInvasion.py`: The entry point that initializes simulation objects and registers steppables.


* 
`Simulation/CancerInvasionSteppables.py`: Contains custom Python logic for cell dynamics, tracking, MMP/TIMP secretion rules, degradation conditions, and error-handling simulation cleanup mechanics.
