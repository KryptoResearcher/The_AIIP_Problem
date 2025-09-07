import time
from .aiip import AIIP
from .parameters import generate_parameters

def brute_force_attack(aiip_instance, y_target):
    """
    Attempts to solve the AIIP instance by iterating over all possible x in GF(q).
    Only feasible for very small fields.

    Args:
        aiip_instance (AIIP): An initialized AIIP object.
        y_target (int): The target value to find the preimage for.

    Returns:
        int: The solution x if found, else None.
    """
    print(f"Starting brute-force attack on AIIP instance (q={aiip_instance.q}, n={aiip_instance.n})...")
    start_time = time.time()
    for x_candidate in range(aiip_instance.q):
        if aiip_instance.iterate(x_candidate) == y_target:
            end_time = time.time()
            print(f"Solution found: x = {x_candidate}")
            print(f"Time elapsed: {end_time - start_time:.2f} seconds.")
            return x_candidate
    end_time = time.time()
    print(f"No solution found. Time elapsed: {end_time - start_time:.2f} seconds.")
    return None

def time_iteration(aiip_instance, num_samples=100):
    """
    Benchmarks the average time to compute a single iteration.
    Useful for estimating the cost of brute-force attacks.

    Args:
        aiip_instance (AIIP): An initialized AIIP object.
        num_samples (int): Number of samples to average over.
    """
    print(f"Benchmarking iteration for n={aiip_instance.n}, q={aiip_instance.q}...")
    total_time = 0.0
    for _ in range(num_samples):
        x = int(galois.GF(aiip_instance.q).Random())
        start_time = time.perf_counter()
        aiip_instance.iterate(x)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
    avg_time = total_time / num_samples
    print(f"Average time per full iteration ({aiip_instance.n} evaluates): {avg_time:.6f} seconds")
    print(f"Estimated brute-force time for entire field: {avg_time * aiip_instance.q / 3600:.2f} hours")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run cryptanalysis on a small AIIP instance.')
    parser.add_argument('--n', type=int, default=4, help='Number of iterations')
    parser.add_argument('--q', type=int, default=2**10, help='Field size (prime)')
    args = parser.parse_args()

    # Generate a random instance
    params = generate_parameters(bit_sec=32, n=args.n) # Low security for testing
    params.q = args.q # Override with user-provided q
    f = lambda x: x**2 + params.alpha
    aiip_instance = AIIP(f, params.n, params.q)

    # Create a problem instance
    secret_x = 42
    y_target = aiip_instance.iterate(secret_x)
    print(f"Secret x is: {secret_x}")
    print(f"Target y is: {y_target}")

    # Time the iteration
    time_iteration(aiip_instance, num_samples=10)

    # Try to brute force it (only for very small q!)
    if args.q <= 2**14: # ~16,384 elements max for a quick test
        found_x = brute_force_attack(aiip_instance, y_target)
        if found_x == secret_x:
            print("Brute force attack successful!")
        else:
            print("Brute force attack failed or found a collision.")
    else:
        print(f"Field size q={args.q} is too large for a brute-force demo.")