# Theoretical Background: The AIIP Problem

This document summarizes the core theoretical concepts behind the Affine Iterated Inversion Problem (AIIP). For complete details and proofs, please refer to the full paper: [eprint.iacr.org/2025/1590](https://eprint.iacr.org/2025/1590).

## 1. Problem Definition

Let `f` be a polynomial over a finite field `GF(q)` of degree `d >= 2` (e.g., the quadratic map `f(x) = x² + α`). Let `f^{(n)}` denote the `n`-fold composition of `f` with itself.

The **AIIP** is defined as follows:
- **Given:** The function `f`, an iteration parameter `n`, and a target element `y ∈ GF(q)`.
- **Find:** An element `x ∈ GF(q)` such that `f^{(n)}(x) = y`.

## 2. Why is it Hard?

The hardness of AIIP stems from two independent, well-studied computational problems.

### 2.1. Reduction to the MQ Problem

**Theorem (Informal):** The AIIP is polynomial-time reducible to solving a system of multivariate quadratic (MQ) equations.

**How?** The computation `f^{(n)}(x)` can be "unrolled" by introducing intermediate variables `x₀, x₁, ..., xₙ` where:
- `x₀ = x`
- `x₁ = f(x₀)`
- `x₂ = f(x₁)`
- `...`
- `xₙ = f(xₙ₋₁) = y`

Each step `xᵢ = f(xᵢ₋₁)` can be expressed as a set of `k` quadratic equations over the prime subfield `GF(p)` (where `q = pᵏ`). The resulting system has `O(n)` variables and equations. Solving random MQ systems is NP-Hard, and the specific structure induced by iteration appears heuristically to be hard.

### 2.2. Connection to Hyperelliptic Curve DLP

**Theorem (Informal):** For the quadratic map `f(x)=x²+α`, solving an AIIP instance `(f, n, y)` is intimately connected to computing discrete logarithms in the Jacobian of a specific hyperelliptic curve.

**How?** The curve is defined by the equation:
`C_{n,y}: v² = F_n(u) - y`
where `F_n(u) = f^{(n)}(u)` is the iterated polynomial. This curve has genus `g = 2ⁿ⁻¹ - 1`, which grows exponentially with `n`. The Discrete Logarithm Problem (DLP) in high-genus Jacobians is believed to be hard, even for quantum computers.

## 3. Security Analysis & Parameter Selection

Security rests on ensuring that all known attacks are computationally infeasible.

| Attack Vector | Defense | Parameter Guidance |
| :--- | :--- | :--- |
| **Brute Force** | Large field size `q` | `log₂(q) >= 2λ` to resist Grover's quantum search (`O(√q)`). |
| **Algebraic (Gröbner Basis)** | High iteration depth `n` | The MQ system's solving complexity is `~n^{ωn}`, so choose `n` such that `n^{ωn} > 2^λ`. |
| **Hyperelliptic Index Calculus** | Exponentially large genus `g` | The genus `g = 2ⁿ⁻¹ - 1` is massive for crypto `n`, making index calculus attacks (`~O(q^{2-2/g})`) infeasible. |

**Recommended Parameters:**
| Security Level (λ) | Field Size `log₂(q)` | Iterations `n` | Curve Genus `g` |
| :--- | :--- | :--- | :--- |
| 128-bit | 256 | 16 | 2¹⁵ - 1 = 32767 |
| 192-bit | 384 | 20 | 2¹⁹ - 1 = 524287 |
| 256-bit | 512 | 24 | 2²³ - 1 = 8388607 |

## 4. Conclusion

The AIIP problem enjoys a **dual hardness foundation**:
1.  **Combinatorial/Algebraic Hardness:** Based on the NP-hardness of the MQ problem.
2.  **Number-Theoretic Hardness:** Based on the conjectured hardness of DLP in high-genus hyperelliptic curves.

This makes it a robust and promising candidate for building post-quantum cryptographic primitives.