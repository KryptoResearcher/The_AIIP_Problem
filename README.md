# Small-n AIIP Examples

This directory contains concrete, solvable AIIP instances with small iteration parameters (`n = 3, 4, 5`). These are intended for testing and validation of the reduction algorithms and solving techniques.

## File Format

Each example is stored in a JSON file with the following structure:
```json
{
    "parameters": {
        "q": 65537,
        "n": 4,
        "alpha": 12345
    },
    "challenge": {
        "y_target": 9876
    },
    "solution": {
        "x_seed": 42
    },
    "mq_system_info": {
        "num_variables": 32,
        "num_equations": 28,
        "generation_time_sec": 0.15
    }
}