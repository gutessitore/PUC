import time
import timeit
from functools import wraps

import numpy
import numpy as np
from numba import njit, prange, set_num_threads

set_num_threads(4)


def timeme(function):
    """
    Decorator to measure and print the execution time of a function.

    This decorator wraps the provided function and measures its execution time
    using the time.perf_counter() function. Upon completion, it prints the
    function name and the elapsed time in seconds with 4 decimal places.

    Args:
    function (Callable): The function to be timed.

    Returns:
    Callable: The wrapped function with added timing functionality.

    Example:
    >>>
    >>> @timeme
    >>> def example_function():
    >>>    # Some code here
    >>>
    >>> example_function()  # Will print the execution time upon completion.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"{function.__name__} levou {elapsed_time:.4f} segundos para executar.")
        return result

    return wrapper


@timeme
def matrix_multiply_np(matriz1, matriz2):
    return numpy.dot(matriz1, matriz2)


@timeme
def sequential_matrix_multiply(matrix_A, matrix_B):
    rows_A = matrix_A.shape[0]
    cols_A = matrix_A.shape[1]
    rows_B = matrix_B.shape[0]
    cols_B = matrix_B.shape[1]

    if cols_A != rows_B:
        raise ValueError("O número de colunas da matriz A deve ser igual ao número de linhas da matriz B.")

    result_matrix = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for row_idx in range(rows_A):
        for col_idx in range(cols_B):
            for shared_dim in range(cols_A):
                result_matrix[row_idx][col_idx] += matrix_A[row_idx][shared_dim] * matrix_B[shared_dim][col_idx]

    return result_matrix


@timeme
@njit(parallel=True)
def parallel_matrix_multiply(matrix_A, matrix_B):
    rows_A = matrix_A.shape[0]
    cols_A = matrix_A.shape[1]
    rows_B = matrix_B.shape[0]
    cols_B = matrix_B.shape[1]

    if cols_A != rows_B:
        raise ValueError("O número de colunas da matriz A deve ser igual ao número de linhas da matriz B.")

    result_matrix = np.zeros((rows_A, cols_B))

    for row_idx in prange(rows_A):
        for col_idx in range(cols_B):
            for shared_dim in range(cols_A):
                result_matrix[row_idx, col_idx] += matrix_A[row_idx, shared_dim] * matrix_B[shared_dim, col_idx]

    return result_matrix


def compare_matrix_multiplication(matrix_A, matrix_B):
    result_np = matrix_multiply_np(matrix_A, matrix_B)
    result_parallel = parallel_matrix_multiply(matrix_A, matrix_B)
    result_manual = sequential_matrix_multiply(matrix_A, matrix_B)

    assert np.array_equal(result_manual, result_np) and np.array_equal(result_manual, result_parallel)


# testando np vs implementação manual
matriz1 = np.array([[1, 2, 3], [4, 5, 6]])
matriz2 = np.array([[1, 2], [3, 4], [5, 6]])

print(f"Testando com matrizes de tamanho {matriz1.shape} e {matriz2.shape}")
compare_matrix_multiplication(matriz1, matriz2)

# Testando com matrizes maiores com valores aleatórios
n = 500

matriz1 = np.random.randint(0, 100, size=(n, n))
matriz2 = np.random.randint(0, 100, size=(n, n))

print(f"\nTestando com matrizes de tamanho {matriz1.shape} e {matriz2.shape}")
compare_matrix_multiplication(matriz1, matriz2)

# Testando com número de threads diferentes
for num_of_threads in [1, 2, 4, 8, 9, 20]:
    set_num_threads(num_of_threads)
    print(f"\nTestando com {num_of_threads} threads")
    parallel_matrix_multiply(matriz1, matriz2)


# Medindo o tempo de execução da solução sequencial
def run_sequential():
    sequential_matrix_multiply(matrix_A, matrix_B)

sequential_time = timeit.timeit(run_sequential, number=10) / 10

# Medindo o tempo de execução da solução paralela
def run_parallel():
    parallel_matrix_multiply(matrix_A, matrix_B)

parallel_time = timeit.timeit(run_parallel, number=10) / 10

speedup = sequential_time / parallel_time
print(f"Speedup: {speedup:.2f}")