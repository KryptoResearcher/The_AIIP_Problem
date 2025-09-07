
#### File 1: aiip.py

import numpy as np
import galois

class AIIP:
    """
    A class to represent and work with the Affine Iterated Inversion Problem (AIIP).
    Core functionality: Iterate a polynomial f, n times, and generate the corresponding MQ system.
    """

    def __init__(self, f, n, q):
        """
        Initialize an AIIP context.

        Args:
            f (function): A polynomial function, e.g., lambda x: x**2 + alpha.
            n (int): The number of iterations.
            q (int): The prime power defining the finite field GF(q).
        """
        self.f = f
        self.n = n
        self.q = q
        self.GF = galois.GF(q) # Create the Galois field object

    def iterate(self, x):
        """
        Compute f^{(n)}(x), the n-th iterate of f applied to x.

        Args:
            x (int): The input element in GF(q).

        Returns:
            int: The result of the iteration in GF(q).
        """
        current = self.GF(x)
        for _ in range(self.n):
            current = self.f(current)
        return int(current)

    def to_mq_system(self, y_target):
        """
        Generates the Multivariate Quadratic (MQ) system representation of the AIIP instance.
        This implements the reduction from the paper.

        The system has n+1 variable vectors (x_0, x_1, ..., x_n), each of size k (for GF(q) = GF(p^k)).
        The equations enforce x_{i} = f(x_{i-1}) and x_n = y_target.

        Args:
            y_target (int): The target value y for which to solve f^{(n)}(x) = y.

        Returns:
            MQSystem: An object containing the list of quadratic equations.
        """
        # This is a placeholder structure. A full implementation would:
        # 1. Decompose GF(q) into a vector space over GF(p) (k=1 if q is prime).
        # 2. For each iteration i, express the equation x_i = f(x_{i-1}) as k quadratic equations.
        # 3. Flatten all variable vectors into a single list of N = k*(n+1) variables over GF(p).
        # 4. Return a list of polynomial equations of degree <= 2.

        # For the sake of this example, we return a simple object.
        # A real implementation would be more complex and use the galois library's arithmetic.
        class MQSystem:
            def __init__(self, equations, num_vars, field):
                self.equations = equations
                self.num_vars = num_vars
                self.field = field

        # Placeholder: Simulate generating a system of size ~O(n)
        num_vars_approx = self.n * 2  # Simplified approximation
        # In reality, num_vars = k * (n+1)
        dummy_equation = "x0^2 + x1 + ... = 0"

        return MQSystem(
            equations=[dummy_equation] * (self.n * 3), # Placeholder number of equations
            num_vars=num_vars_approx,
            field=self.GF
        )

if __name__ == "__main__":
    # Example usage
    alpha = 5
    n = 4
    q = 2**17 # 131072
    f = lambda x: x**2 + alpha

    aiip_instance = AIIP(f, n, q)

    # Let's find the image of a point
    secret_x = 123
    result_y = aiip_instance.iterate(secret_x)
    print(f"f^{n}({secret_x}) = {result_y} in GF({q})")

    # Generate the MQ system for the problem: find x such that f^{n}(x) = result_y
    mq_sys = aiip_instance.to_mq_system(result_y)
    print(f"Generated an MQ system with {mq_sys.num_vars} variables and {len(mq_sys.equations)} equations.")