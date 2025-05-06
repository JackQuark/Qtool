# _summary_
# ==================================================
import numpy as np
# ==================================================

__all__ = ['integrate', 'fdd_3pt_forward', 'fdd_3pt_backward', 'fdd_2pt_central',
           'gradient', 'divergence', 'curl']

def integrate(f, a, b, n=1000):
    """Integrate f(x) from a to b by `np.trapz`."""
    x = np.linspace(a, b, n+1)
    y = f(x)
    return np.trapz(y, x)

# ==================================================
# Finite Difference from data (fdd)
def fdd_3pt_forward(Y, h, axis=0):
    """finite difference from data, 3 points forward"""
    if Y.shape[axis] < 3: raise ValueError("Y must have at least 3 elements")
    if axis == 0:
        return (-3*Y[:-2] + 4*Y[1:-1] - Y[2:]) / (2*h)
    else:
        idxer1, idxer2, idxer3 = [slice(None)] * Y.ndim, [slice(None)] * Y.ndim, [slice(None)] * Y.ndim
        idxer1[axis] = slice(None, -2)
        idxer2[axis] = slice(1, -1)
        idxer3[axis] = slice(2, None)
        return (-3*Y[tuple(idxer1)] + 4*Y[tuple(idxer2)] - Y[tuple(idxer3)]) / (2*h)

def fdd_3pt_backward(Y, h, axis=0):
    """finite difference from data, 3 points backward"""
    if Y.shape[axis] < 3: raise ValueError("Y must have at least 3 elements")
    if axis == 0:
        return (3*Y[2:] - 4*Y[1:-1] + Y[:-2]) / (2*h)
    else:
        idxer1, idxer2, idxer3 = [slice(None)] * Y.ndim, [slice(None)] * Y.ndim, [slice(None)] * Y.ndim
        idxer1[axis] = slice(2, None)
        idxer2[axis] = slice(1, -1)
        idxer3[axis] = slice(None, -2)
        return (3*Y[tuple(idxer1)] - 4*Y[tuple(idxer2)] + Y[tuple(idxer3)]) / (2*h)
    
def fdd_2pt_central(Y, h, axis=0):
    """finite difference from data, 2 points central"""
    if Y.shape[axis] < 3: raise ValueError("Y must have at least 3 elements")
    if axis == 0:
        return (Y[2:] - Y[:-2]) / (2*h)
    else:
        idxer1, idxer2 = [slice(None)] * Y.ndim, [slice(None)] * Y.ndim
        idxer1[axis] = slice(2, None)
        idxer2[axis] = slice(None, -2)
        return (Y[tuple(idxer1)] - Y[tuple(idxer2)]) / (2*h)

# ==================================================
# Vector Calculus
def _args_check_VectorCalculus(*arrs, h=None):
    """**private function**\n
    for `gradient`, `divergence`, `curl`\n
    """
    if len(arrs) != (Ndim := arrs[0].ndim):
        raise ValueError(f"len(arrs) ({len(arrs)}) must be equal to the ndim of the arrays ({Ndim})")
    if len(set(map(np.ndim, arrs))) != 1:
        raise ValueError("All arrays must have the same ndim")
    if h is None: # interval check
        h = (1,) * Ndim
    elif isinstance(h, (int, float)):
        h = (h,) * Ndim
    elif len(h) != Ndim:
        raise ValueError("len(h) must be equal to the ndim of the array")
    return Ndim

def gradient(*arrs: np.ndarray, h: float | tuple[float] = None) -> list[np.ndarray]:
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
    Ndim = _args_check_VectorCalculus(*arrs, h=h)
    
    res = [np.zeros_like(arr) for arr in arrs]
    idxer = [slice(None)] * Ndim
    for i, arr in enumerate(arrs): # compute gradient of each dim
        idxer[i] = slice(1, -1)
        res[i][tuple(idxer)] = fdd_2pt_central(arr, h[i], axis=i)
        idxer[i] = slice(None, 1)
        res[i][tuple(idxer)] = fdd_3pt_forward(arr.take(range(0, 3), axis=i), h[i], axis=i)
        idxer[i] = slice(-1, None)
        res[i][tuple(idxer)] = fdd_3pt_backward(arr.take(range(-3, 0), axis=i), h[i], axis=i)
        idxer[i] = slice(None) # reset index
    return res

def divergence(*arrs: np.ndarray, h: float | tuple[float] = None) -> np.ndarray:
    """divergence of n-d arrays using finite difference\n
    using 3 pts forward and backward and 2 pts central\n 
    truncation error: `O(h^2)`\n
    Args:
        arrs (*np.ndarray): n-d arrays
        h (float | tuple[float], optional): interval size, default is 1 for all dimensions
    Returns:
        res (np.ndarray): divergence of n-d arrays with same shape as any arr in arrs
    See Also
    ---
        `gradient` (used to calc. the partial derivatives)
    """    
    return sum(gradient(*arrs, h=h))

def curl(*arrs: np.ndarray, h: float | tuple[float] = None) -> list[np.ndarray]:
    """curl of 2 or 3-d arrays using finite difference\n
    truncation error: `O(h^2)`\n
    Args:
        arrs (*np.ndarray): n-d arrays
        h (float | tuple[float], optional): interval size, default is 1 for all dimensions
    Returns:
        res (list[np.ndarray]): curl of n-d arrays with same shape as any arr in arrs
    See Also
    ---
        `gradient` (used to calc. the partial derivatives)
    """
    Ndim = _args_check_VectorCalculus(*arrs, h=h)
    
    if Ndim == 2:
        dFy_dx, dFx_dy = gradient(arrs[0], arrs[1], h=h)
        return dFy_dx - dFx_dy
    elif Ndim == 3:
        grad_left = gradient(arrs[1], arrs[2], arrs[0], h=h)
        grad_right = gradient(arrs[2], arrs[0], arrs[1], h=h)
        return [grad_left[1] - grad_right[2], grad_right[2] - grad_left[0], grad_left[0] - grad_right[1]]
    else:
        raise ValueError("curl is only for 2 or 3-d arrays")

# ==================================================

def main():
    import matplotlib.pyplot as plt
        
    x = y = z = np.linspace(-2, 2, 101)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    Fx = np.cos(X + 2*Y)
    Fy = np.sin(X - 2*Y)
    Fz = Z * X
    
    analytic_divF = lambda x, y, z: -np.sin(x + 2*y) - 2*np.cos(x - 2*y) + x

    gradF = gradient(Fx, Fy, Fz, h=x[1]-x[0])
    divF  = sum(gradF)
    curlF = curl(Fx, Fy, Fz, h=x[1]-x[0])
    mid_z = divF.shape[2] // 2
    plt.figure(figsize=(4, 3))

    plt.contourf(X[..., mid_z], Y[..., mid_z], curlF[2][..., mid_z], cmap='coolwarm', levels=10)
    plt.colorbar(label='Divergence')
    plt.contour(X[..., mid_z], Y[..., mid_z], analytic_divF(X[..., mid_z], Y[..., mid_z], Z[..., mid_z]), 
                levels=10, colors='k', linewidths=0.5).clabel()
    
    _skip = slice(None, None, 5)
    plt.quiver(X[_skip, _skip, mid_z], Y[_skip, _skip, mid_z], Fx[_skip, _skip, mid_z], Fy[_skip, _skip, mid_z], 
               color='k')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.tight_layout()
    plt.show()

# ==================================================

if __name__ == '__main__':
    from time import perf_counter
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))