# Affine Iterated Inversion Problem (AIIP) - Cryptographic Implementation

This repository provides a Python reference implementation and cryptanalysis tools for the **Affine Iterated Inversion Problem (AIIP)**, a new candidate hard problem for post-quantum cryptography introduced in the paper:

> **"The AIIP Problem: Toward a Post-Quantum Hardness Assumption from Affine Iterated Inversion over Finite Fields"**
> *Preprint: https://eprint.iacr.org/2025/1590*

The AIIP problem involves inverting an iterated polynomial map over a finite field, i.e., for a polynomial `f`, iteration count `n`, and target `y`, find `x` such that `f^{(n)}(x) = y`. This work establishes hardness reductions to both the Multivariate Quadratic (MQ) problem and the Hyperelliptic Curve Discrete Logarithm Problem (HCDLP).

## Repository Structure
The_AIIP_Problem/
├── src/ # Core Python source code
│ ├── aiip.py # AIIP iteration and MQ system generation
│ ├── parameters.py # Parameter generation and validation
│ └── cryptanalysis.py # Brute-force and algebraic attack scripts
├── examples/ # Pre-computed example instances
│ ├── small_n/ # Examples for small n (n=3,4,5) for testing
│ └── security_levels/ # Parameters for 128, 192, 256-bit security
├── notebooks/ # Jupyter notebooks for tutorial and analysis
│ ├── tutorial.ipynb # Step-by-step guide to using the library
│ └── analysis.ipynb # Cryptanalysis of small-scale instances
├── docs/ # Supplementary documentation
│ ├── README.md # This file
│ └── THEORY.md # Detailed theoretical background
└── requirements.txt # Python dependencies


## Features

- **Efficient Iteration:** Compute `f^{(n)}(x)` for polynomials over large finite fields.
- **MQ Reduction:** Generate the system of multivariate quadratic equations equivalent to solving an AIIP instance, as per the polynomial-time reduction in the paper.
- **Parameter Generation:** Generate cryptographically secure parameters (field size `q`, iteration depth `n`, constant `α`) for target security levels.
- **Cryptanalysis Tools:** Scripts for brute-force inversion and interface with Gröbner basis solvers (e.g., SageMath) for the generated MQ systems.
- **Educational Examples:** Jupyter notebooks and small-scale examples to understand the problem structure and the growth in complexity.

## Installation & Dependencies

1.  **Clone the repository:**
   
    git clone https://github.com/your-username/aiip-crypto.git
    cd aiip-crypto
    

2.  **Install required Python packages:**
    
    pip install -r requirements.txt
    
    *Core dependencies:* `numpy`, `galois`, `sage` (for advanced cryptanalysis, recommended to install separately via SageMath).

## Quick Start

```python
from src.aiip import AIIP
from src.parameters import generate_parameters

# 1. Generate parameters for a small test instance
params = generate_parameters(bit_sec=32, n=4)
f = lambda x: x**2 + params.alpha
aiip_solver = AIIP(f, params.n, params.q)

# 2. Choose a random starting point x and compute the final target y
x_true = 123456  # Secret input
y_target = aiip_solver.iterate(x_true) # f^{(n)}(x_true)

# 3. Create an AIIP instance: Given (f, n, y_target), find x.
print(f"AIIP Instance: Find x such that f^{(params.n)}(x) = {y_target}")

# 4. Generate the MQ system for this instance (for analysis or solving)
mq_system = aiip_solver.to_mq_system(y_target)
print(f"Generated a system of {len(mq_system.equations)} quadratic equations.")

For a detailed walkthrough, see the notebooks/tutorial.ipynb Jupyter notebook.
Usage Examples

    examples/small_n/: Contains AIIP instances with n=3,4,5 and their corresponding MQ systems. Use these to test your solving algorithms.

    examples/security_levels/: Contains recommended parameters for 128, 192, and 256-bit security levels, as proposed in the paper. The MQ systems for these are too large to solve but can be generated for structural analysis.

Cryptanalysis

The src/cryptanalysis.py module provides tools to assess the hardness of AIIP instances:

    Brute-force attack: Tests the naive inversion method. Infeasible for q > 2^40.

    Algebraic attack: Exports MQ systems to SageMath format for Gröbner basis analysis (e.g., using F4/F5 algorithms). The complexity is super-exponential in n, demonstrating the problem's hardness.

Run a simple analysis:
python -m src.cryptanalysis --n 4 --q 65537
Theory & Supporting Documentation

The docs/THEORY.md file provides a summary of the core theoretical concepts from the paper:

    Definition of the AIIP problem.

    Overview of the reduction to the MQ problem.

    Overview of the connection to HCDLP.

    Security analysis and parameter selection rationale.
    Contributing

This is a research reference implementation. Contributions, bug reports, and suggestions are welcome, especially regarding:

    Efficiency improvements for large iterations.

    New cryptanalysis techniques.

    Additional documentation and examples.

Please open an issue or submit a pull request.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Citation

If you use this code or the AIIP problem in your academic work, please cite our preprint:
@article{aiip2025,
    title = {The AIIP Problem: Toward a Post-Quantum Hardness Assumption from Affine Iterated Inversion over Finite Fields},
    author = {Minka Mi Nguidjoi, Thierry Emmanuel},
    year = {2025},
    url = {https://eprint.iacr.org/2025/1590},
    note = {Cryptology ePrint Archive, Paper 2025/1590}
}

