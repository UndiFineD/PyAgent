# AI for Science

Applying Deep Learning to solve fundamental problems in biology, physics, and chemistry.

## 1. Protein Folding (AlphaFold)

*   **Problem**: Predicting the 3D structure of a protein based solely on its 1D amino acid sequence. This determines how the protein functions (and how drugs interact with it).
*   **Solution**: AlphaFold uses an "Evoformer" (Evolutionary Transformer) to process Multiple Sequence Alignments (MSA) and predict the spatial coordinates of atoms.
*   **Impact**: Solved a 50-year-old grand challenge in biology.

## 2. Material Discovery (GNoME)

*   **Problem**: Finding new stable crystals for batteries, solar panels, and chips.
*   **Solution**: Graph Neural Networks (GNNs) predict the stability of millions of theoretical crystal structures.
*   **Impact**: Discovered 2.2 million new crystals (equivalent to 800 years of human research).

## 3. Physics-Informed Neural Networks (PINNs)

*   **Concept**: Embedding physical laws (Partial Differential Equations like Navier-Stokes) directly into the Loss Function of the neural network.
*   **Benefit**: The model doesn't just fit the data; it obeys the laws of physics (e.g., conservation of energy/mass).
*   **Use Case**: Simulating fluid dynamics, weather forecasting, and heat transfer faster than traditional solvers.
