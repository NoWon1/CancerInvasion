# **Modeling Cell-Type-Specific MMP Dynamics and ECM Remodeling in the Tumor Microenvironment**

# **Project Overview**

Metastasis remains the primary driver of cancer-related mortality, accounting for the vast majority of cancer deaths globally \[cite: 1, 2\]. This multi-step process involves the detachment of tumor cells from the primary site, their transit through the extracellular matrix (ECM), intravasation into the circulatory system, and the eventual colonization of distant organs \[cite: 1, 3\]. The invasion of cancer cells into the surrounding tissue is fundamentally regulated by the tumor microenvironment (TME), which consists of a complex interplay between tumor cells, stromal components, immune cells, and the structural scaffold of the ECM \[cite: 1, 4\].

Central to this remodeling process is the activity of matrix metalloproteinases (MMPs), a family of zinc-dependent endopeptidases capable of degrading various protein components of the ECM, such as collagen and laminin \[cite: 1, 2\]. The activity of these enzymes is not only structural but also regulatory, as the degradation of the matrix liberates sequestered growth factors (GF) and generates bioactive fragments that influence cell behavior \[cite: 1, 5, 6\]. To maintain physiological homeostasis, the action of MMPs is strictly controlled by tissue inhibitors of metalloproteinases (TIMPs), which form stable 1:1 stoichiometric complexes with the active sites of MMPs \[cite: 1, 7\].

This repository documents a comprehensive research project developed for the Param Hansa Centre for Computational Oncology (PHCCO) Summer Training Program. The research team developed a 100% Python-based simulation using the CompuCell3D (CC3D) environment to investigate how the balance between pro-tumorigenic MMPs, immune-regulated MMPs, and TIMP secretions governs the spatial dynamics of tumor invasion and the architectural integrity of the ECM \[cite: 2\].

# **Problem Statement and Research Objectives**

Despite the known roles of specific MMPs and TIMPs, the collective spatial dynamics resulting from heterogeneous cell populations—each secreting varying levels of these molecules—remains difficult to predict using purely experimental methods \[cite: 8, 9\]. Tumor heterogeneity, characterized by the presence of both epithelial-like and mesenchymal-like cells, further complicates the invasion landscape \[cite: 10\]. There is a critical need to understand how varying diffusion rates of proteolytic enzymes and the density of the tumor population influence the effectiveness of immune cell infiltration and the overall rate of metastatic spread \[cite: 2, 7\].

The primary objectives of this research included:

* Integrating an agent-based model (ABM) to simulate the spatial interactions of tumor and immune cells in the presence of diffusing MMP and TIMP fields \[cite: 1, 2\].  
* Quantifying the influence of MMP diffusion constants on the transition between cohesive collective invasion and dispersed individual migration \[cite: 2\].  
* Investigating the role of MMP8—primarily secreted by neutrophils—as a potential metastasis suppressor that enhances cell-ECM adhesion and modulates the epithelial-mesenchymal transition (EMT) \[cite: 1\].  
* Modeling the "immune exclusion" phenomenon, where a dense or inappropriately remodeled ECM prevents cytotoxic T-lymphocytes (CTLs) from reaching the tumor mass \[cite: 4, 7\].

# **Computational Framework and Methodology**

The simulation was developed using the Cellular Potts Model (CPM), also known as the Glazier-Graner-Hogeweg (GGH) model, implemented through the CompuCell3D simulation environment \[cite: 1, 7\]. This framework was chosen for its ability to integrate discrete cellular mechanics with continuous partial differential equation (PDE) solvers for chemical fields, making it ideal for modeling the multiscale nature of tumor progression \[cite: 8, 11\].

## **The Cellular Potts Model Hamiltonian**

The system's evolution is driven by the minimization of total effective energy, represented by the Hamiltonian (H). Every pixel-copy attempt in the simulation is evaluated against this energy function to determine its probability of acceptance \[cite: 1\]. The Hamiltonian for this model is defined as the sum of several energy constraints:

H \= H\_adhesion \+ H\_volume \+ H\_surface \+ H\_chemotaxis

The adhesion term (H\_adhesion) calculates the energy associated with the contact between different cell types and the ECM. Lower contact energy (J) signifies higher adhesivity between the interacting components \[cite: 9\]. The volume and surface constraints ensure that cells maintain their biological integrity by penalizing deviations from their target volume (Vt) and target surface area (St) using Lagrange multipliers (lambda\_v and lambda\_s) \[cite: 12, 13\].

## **Monte Carlo Step (MCS) Logic**

The simulation dynamics proceed through successive Monte Carlo Steps. In each MCS, the following logic is executed:

* Pixel Selection: The system randomly selects a lattice site (pixel) and an adjacent neighbor \[cite: 14\].  
* Energy Calculation: The change in effective energy (Delta H) that would result from copying the index of the source pixel to the target pixel is calculated \[cite: 1\].  
* Acceptance Criteria: If Delta H is less than or equal to 0, the update is accepted automatically. If Delta H is positive, the update is accepted with a probability defined by the Boltzmann function: P \= e^(-Delta H / T), where T represents the effective membrane fluctuation of the cells \[cite: 1, 14\].  
* Time Scaling: Based on experimental calibrations, 1000 MCS corresponds to approximately 24 to 36 hours of real-time, with 1 MCS effectively representing 86.4 seconds \[cite: 15\].

# **Model Agents and Environment Specification**

The research utilizes a heterogeneous environment where distinct cell agents interact with a structural and degradable ECM.

## **Agent-Based Components**

The simulation comprises two primary cancer cell types and recruited immune cells:

* Cancer1 (Epithelial-like): These cells exhibit high cell-cell adhesion and low cell-ECM adhesion. In the simulation, they tend to form stable, cohesive spheroids that invade the matrix as a collective unit \[cite: 1, 2\].  
* Cancer2 (Mesenchymal-like): These cells demonstrate low cell-cell adhesion and high cell-ECM adhesion, mimicking the motile, dispersed phenotype associated with advanced metastasis \[cite: 1, 2\].  
* Immune Cells (CD8+ T cells): Generated at the model's periphery, these agents move via chemotaxis towards the tumor mass. They are programmed with a specific "killing probability" to eliminate tumor cells upon contact \[cite: 1, 2, 7\].  
* The Extracellular Matrix: The matrix is modeled as a multicomponent structure consisting of collagen and laminin. Laminin is susceptible to proteolytic degradation, transitioning into a lysed state (l\_lysed) when exposed to a high ratio of MMPs to TIMPs \[cite: 1, 2\].

## **Modeling Chemical Fields**

The chemical environment is managed via the DiffusionSolverFE steppable in CC3D, facilitating the following fields:

* MMP and TIMP Dynamics: Cancer cells secrete MMPs and TIMPs upon contact with laminin. The matrix is only degraded if the local concentration ratio of MMP:TIMP exceeds 2.0 \[cite: 1\].  
* Growth Factor (GF): Secreted by the ECM during cellular interaction or degradation. The TargetVolume of cancer cells is set as a function of the local GF concentration, allowing for nutrient-dependent growth \[cite: 1\].  
* Chemoattractant: Tumor cells secrete this signal to recruit immune cells from the periphery, creating a dynamic competition between tumor growth and immune-mediated destruction \[cite: 1, 2\].

# **Implementation and Parameterization**

The simulation parameters were derived from experimental literature, including the works of Kumar S. et al. (2016) and Prasanna et al. (2024), to ensure the model captures biologically realistic invasion phenotypes \[cite: 1, 10, 16, 17\].

## **Adhesion Energy Matrix**

The contact energies (J) define the preferential interactions between the different agents. Lower values represent higher physical adhesion \[cite: 13\].

| Agent Type 1 | Agent Type 2 | Contact Energy (J) |
| :---- | :---- | :---- |
| Medium | Medium | 0 |
| Medium | Cell (Cancer) | 15 |
| Medium | ECM Fiber | 0 |
| Cell | Cell | 5 |
| Cell | ECM Fiber | 10 |
| ECM Fiber | ECM Fiber | 1 |

## **Cellular and Structural Constraints**

The mechanical properties of the cells and matrix fibers are defined by their target volumes and the strength of their volume/surface constraints (lambda) \[cite: 13\].

| Cell Type | Target Volume (pixels) | Lambda Volume | Target Surface | Lambda Surface |
| :---- | :---- | :---- | :---- | :---- |
| Cancer Cell | 100 | 5.0 | 35 | 2.0 |
| ECM Fiber | 15 | 100.0 | 20 | 50.0 |
| Medium | N/A | 0 | N/A | 0 |

## **Diffusion and Reaction Parameters**

The diffusion constant of the MMP field was the primary variable for sensitivity analysis in this study \[cite: 13\].

| Field / Property | Parameter Name | Numerical Value |
| :---- | :---- | :---- |
| MMP Diffusion Constant | D\_mmp | 0.005 \- 0.05 |
| MMP Decay Constant | delta\_mmp | 0.005 |
| Secretion Rate | lambda\_sec | 0.01 \- 0.1 s^-1 |
| Degradation Threshold | MMP/TIMP Ratio | \> 2.0 |
| Neighbor Order | NeighborOrder | 1 \- 2 |

# **Result Analysis and Key Findings**

The research team performed a systematic analysis of the simulation outputs, quantifying invasion through total cell volume and cell count dynamics over time \[cite: 1\].

## **Impact of MMP Diffusion Rates**

The diffusion constant (D) of MMPs fundamentally alters the morphology of tumor invasion and the regularity of the ECM degradation front.

* Low Diffusion (D \= 0.005): In this regime, proteolytic activity is restricted to the immediate vicinity of the cell membrane. This results in irregular, localized invasion paths. Because the inhibitor (TIMP) is also localized, the regulation of degradation is inconsistent, leading to "jagged" boundaries where individual cells may break away prematurely \[cite: 2\].  
* Intermediate Diffusion (D \= 0.01 \- 0.02): This range produces the most robust and "compact" collective invasion. The MMP signal diffuses far enough to create a smooth path for the tumor mass, while remaining concentrated enough for TIMPs to maintain an effective inhibitory boundary. This prevents erratic "leaks" in the degradation front \[cite: 2\].  
* High Diffusion (D \= 0.05): At high rates, the MMP signal becomes excessively diluted. While a larger area of the matrix is softened, the local concentration often falls below the threshold required for efficient fiber lysis. This leads to erratic and excessive invasion only when tumor densities are high enough to overcome the dilution effect, making inhibitor control largely ineffective \[cite: 1, 2\].

## **Effects of Tumor Density and Heterogeneity**

The simulation results suggest that population density is a major factor in determining the cohesion of the invasion front. Higher initial densities allow for a collective "proteolytic cloud" that degrades the ECM more uniformly than scattered individual cells \[cite: 2\].

Furthermore, the model highlights the specific vulnerabilities of epithelial-like cells. Cancer1 (epithelial-like) cells generally exhibit higher invasion potential due to their collective mass, but they are significantly more sensitive to high MMP diffusion rates than Cancer2 (mesenchymal-like) cells. The loss of a concentrated proteolytic signal disrupts the cohesive front of Cancer1 cells more severely, whereas Cancer2 cells can continue to navigate through partially degraded matrices using their high cell-ECM adhesion \[cite: 1, 2\].

## **ECM Architecture and T-Cell Exclusion**

A major insight from the model is the relationship between matrix remodeling and immune exclusion. Dense collagen regions or areas with low MMP diffusion create structural barriers that immune cells cannot easily penetrate. Even in the presence of strong chemoattractants, T-cells were often trapped at the periphery of the tumor mass, unable to exert their cytotoxic effects on the internal tumor core. This confirms the hypothesis that ECM remodeling by the tumor acts as a "physical shield" against immune surveillance \[cite: 4, 7\].

# **Discussion and Biological Implications**

The integration of agent-based modeling with reaction-diffusion systems provides a powerful lens through which to view the complexity of the TME. The results demonstrate that the effectiveness of metastasis is not solely a function of enzyme production but is heavily dependent on the spatial transport of those enzymes and the physical resistance of the matrix \[cite: 8, 9\].

The observation that intermediate diffusion leads to more regulated, compact invasion has significant therapeutic implications. It suggests that drugs targeting the transport of MMPs, or those that alter the stoichiometry of the MMP:TIMP complex, might be more effective than broad-spectrum inhibitors that simply reduce total enzyme counts \[cite: 1, 3\]. Furthermore, the role of MMP8 as an anti-metastatic factor highlights the potential for "matrix normalization" strategies, where the environment is manipulated to favor adhesion and structural stability rather than degradation \[cite: 1, 4\].

The findings regarding immune exclusion suggest that overcoming the physical barrier of the ECM is a prerequisite for the success of many immunotherapies. By simulating the "shielding" effect of the matrix, this model provides a platform for testing combination therapies that pair checkpoint inhibitors with matrix-degrading agents or adhesion-modulators \[cite: 4, 7\].

# **Getting Started and Implementation**

This project is implemented entirely in Python within the CompuCell3D environment. To replicate or extend this simulation, the following requirements and structure should be observed.

## **Prerequisites**

* CompuCell3D (Standard installation, compatible with Python 3.x) \[cite: 2\].  
* Basic understanding of CC3D project structure, including the .cc3d project file, the Python Steppables, and the XML configuration \[cite: 18, 19\].

## **Project Structure**

The repository is organized following the officially supported CC3D project structure to ensure portability and modularity \[cite: 20, 21\].

* `Simulation.py`: The main entry point that initializes the simulation objects and registers the steppables.  
* `Steppables.py`: Contains the custom Python logic for MMP/TIMP secretion, ECM degradation rules, immune cell recruitment, and the `MitosisSteppable` for tumor proliferation \[cite: 1, 18\].  
* `Simulation.xml`: Defines the lattice dimensions, Potts parameters (Temperature, NeighborOrder), cell types, and initial conditions \[cite: 13, 18\].

## **Running the Simulation**

1. Launch the CompuCell3D Player or Twedit++.  
2. Open the `.cc3d` project file from the cloned repository.  
3. Adjust parameters such as `MMP DiffusionConstant` in the XML or the `killing_probability` in the Steppables file to experiment with different microenvironmental conditions \[cite: 2\].  
4. Monitor real-time visualization of cell sorting, chemical gradients, and matrix degradation within the CC3D Player \[cite: 14\].

# **Conclusion**

This research underscores the critical role of cell-type-specific proteolytic dynamics in shaping the invasive potential of a tumor. By utilizing a 100% Python-based agent-based model, the team successfully demonstrated that the spatial regulation of MMPs and TIMPs—modulated by diffusion rates and tumor heterogeneity—determines whether a tumor remains a cohesive mass or transforms into a dispersed, metastatic threat \[cite: 1, 2\]. The insights gained regarding immune exclusion and the optimal "intermediate" diffusion regime for invasion provide a foundation for future computational and experimental investigations into matrix-targeted cancer therapies \[cite: 3, 4, 8\].

# **Sources**

1. [Final Report\_IISc PHCCO](https://drive.google.com/open?id=1DKoTAAkPPWMgAhN0YPewulfe3sZAKf2E0ALTxAW6QkE)  
2. [report](https://drive.google.com/open?id=1eEOVu5H9g1QaUNGZJr6nDRykQ2a0YBKs2XOCcqhQbXM)  
3. [The role of MMPs in metastasis and tumorigenesis. ECM remodeling... \- ResearchGate](https://www.researchgate.net/figure/The-role-of-MMPs-in-metastasis-and-tumorigenesis-ECM-remodeling-through-MMPs-secretion_fig4_384261431)  
4. [Extracellular matrix remodeling in tumor progression and immune escape: from mechanisms to treatments \- PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10007858/)  
5. [Matrix Metalloproteinases (MMPs) in the SASP: Remodeling the Tumor Microenvironment](https://www.reddotbiotech.com/articles/elisa-kits/mmps-in-senescence-sasp-markers-2150.html)  
6. [Matrix Metalloproteinases Shape the Tumor Microenvironment in Cancer Progression \- PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8745566/)  
7. [PHCCO Project Doc](https://drive.google.com/open?id=1LhfrklrIGLKRq4BvAdOM4J2mhOylggNPKpIxURLTEHU)  
8. [An Interplay Between Reaction-Diffusion and Cell-Matrix Adhesion Regulates Multiscale Invasion in Early Breast Carcinomatosis \- PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700745/)  
9. [Interactive dynamics of matrix adhesion and reaction-diffusion predict diverse multiscale strategies of cancer cell invasion | bioRxiv](https://www.biorxiv.org/content/10.1101/2020.04.14.041632.full)  
10. [Formation of motile cell clusters in heterogeneous model tumors: the role of cell-cell alignment \- arXiv](https://arxiv.org/html/2406.14196v2)  
11. [Cellular Potts Modeling of Tumor Growth, Tumor Invasion, and Tumor Evolution \- Frontiers](https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2013.00087/full)  
12. [Developing a CompuCell3D (CC3D) Simulation](https://compucell3d.org/BinDoc/cc3d_binaries/Manuals/PASI_compucell3d_quickstartguide_2.0.pdf)  
13. [CancerInvasion.xml](https://drive.google.com/open?id=11A4YswhcBuN6kZ6SR3Q6Rzk_nBDTdwoz)  
14. [Introduction to CompuCell3D](https://compucell3d.org/BinDoc/cc3d_binaries/Presentations/Introduction_To_CompuCell/CompuCell_intro_2011.pdf)  
15. [Agent-based modeling reveals impacts of cell adhesion and matrix remodeling on cancer collective cell migration phenotypes | bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.23.630172v1.full-text)  
16. [MedChat\_POC\_Technical\_Documentation\_final](https://drive.google.com/open?id=1NhOZIaw1psrx0Tttx0VLgevE5kp2p5sN07G6QCZoApE)  
17. [A hybrid computational model of cancer spheroid growth with ribose-induced collagen stiffening \- PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12014586/)  
18. [Create Your First CompuCell3D Project — CC3D Reference Manual 4.9.0 documentation](https://compucell3dreferencemanual.readthedocs.io/en/latest/how_to_use_python_in_cc3d.html)  
19. [CompuCell3D Python Scripting manual Version 3.6.0 Maciej H. Swat, Julio Belmonte, Benjamin L. Zaitlen](https://compucell3d.org/BinDoc/cc3d_binaries/Manuals/PythonScriptingManual_v.3.6.0.pdf)  
20. [CompuCell3DReferenceManual/docs/cc3d\_python.rst at master \- GitHub](https://github.com/CompuCell3D/CompuCell3DReferenceManual/blob/master/docs/cc3d_python.rst)  
21. [scripting inside CompuCell3D](https://compucell3d.org/BinDoc/cc3d_binaries/Presentations/Introduction_To_CompuCell/SupplementaryMaterials/PythonScriptingInCompuCell_2011.pdf)

