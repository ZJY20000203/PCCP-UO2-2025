# PCCP-UO2-2025

## Contents: 
- 1-phonon
- 2-rdf
- 3-elastic_constans
- 4-cp&αL
- 5-kappa
- model.xyz
- nep.txt
- README

## Before you run:
Copy nep.txt and model.xyz into the target property folder before running.

## Notes:
1. The model.xyz in the root directory is an 8×8×8 supercell. It is not suitable for phonon and for thermal conductivity calculations using the NEMD method. For these calculations model.xyz files are already provided in the corresponding folders.
2. Each property folder includes a template run.in for calculating the corresponding property. Please adjust parameters such as temperature as needed.
