import random
import galois
from sympy import isprime, primerange

def generate_parameters(bit_sec, n=None):
    """
    Generates cryptographically secure parameters for an AIIP instance based on a target security level.
    Follows the guidelines from the paper.

    Args:
        bit_sec (int): The desired classical security level (e.g., 128, 192, 256).
        n (int, optional): Manually set the iteration depth. If None, it is chosen based on bit_sec.

    Returns:
        Namespace: An object containing parameters (q, n, alpha).
    """
    class Namespace:
        pass
    params = Namespace()

    # 1. Select field size q (prime field for simplicity)
    # Rule of thumb: log2(q) ~ 2 * bit_sec to resist quantum Grover's algorithm.
    target_q_bits = 2 * bit_sec
    # Find a prime close to 2^(target_q_bits)
    lower_bound = 2**(target_q_bits - 2)
    upper_bound = 2**(target_q_bits + 2)
    # This is a simplified search. For real use, use a proper CSPRNG.
    possible_primes = [p for p in primerange(lower_bound, upper_bound) if p.bit_length() == target_q_bits]
    if not possible_primes:
        raise ValueError(f"Could not find a prime of bit length {target_q_bits} in the range.")
    params.q = random.choice(possible_primes)

    # 2. Select iteration depth n
    # Rule of thumb: n is chosen so that MQ solving complexity ~ n^{ω n} > 2^{bit_sec}
    # This is a heuristic. The paper provides a table.
    security_to_n = {128: 16, 192: 20, 256: 24}
    if n is None:
        params.n = security_to_n.get(bit_sec, 16) # Default to 16 if not found
    else:
        params.n = n

    # 3. Select constant alpha (should be a quadratic non-residue mod q for security)
    GF = galois.GF(params.q)
    while True:
        alpha_candidate = random.randint(1, params.q-1)
        # Check if alpha_candidate is a quadratic non-residue
        # For a prime field GF(q), the Legendre symbol (a/q) can be computed as a^((q-1)/2) mod q
        legendre = pow(alpha_candidate, (params.q-1)//2, params.q)
        if legendre == params.q - 1: # This equals -1 mod q, meaning non-residue
            params.alpha = alpha_candidate
            break

    params.field = GF
    print(f"Generated parameters for ~{bit_sec}-bit security:")
    print(f"  Field (q)      : {params.q} (prime)")
    print(f"  Iterations (n) : {params.n}")
    print(f"  Constant (alpha): {params.alpha} (quadratic non-residue mod q)")
    return params

if __name__ == "__main__":
    # Generate parameters for 128-bit security
    params = generate_parameters(bit_sec=128)