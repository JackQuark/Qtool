from numpy import ndarray
from typing import Tuple, List

def gradient(*arrs: ndarray, h: Tuple[float, ...] = ...) -> List[ndarray]: 
    """gradient of n-d arrays using finite difference\n
    using 3 pts forward and backward and 2 pts central\n 
    truncation error: `O(h^2)`\n
    Args:
        arrs (*np.ndarray): n-d arrays
        h (float | tuple[float], optional): interval size, default is 1 for all dimensions
    Returns:
        res (list[np.ndarray]): divergence of n-d arrays with same shape as any arr in arrs
    Example:
        ```python
        x = y = z = np.linspace(-1, 1, 100)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        Fx = X * Y
        Fy = Y * Z
        Fz = Z * X
        gradF = gradient(Fx, Fy, Fz, h=x[1]-x[0])
        ```
    """
    ...