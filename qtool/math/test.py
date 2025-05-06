import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 建立三維格點
x = y = z = np.linspace(-1, 1, 10)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# 定義向量場 F(x, y, z) = (xy, yz, zx)
Fx = X * Y
Fy = Y * Z
Fz = Z * X

# 你自己的 divergence 函數
def divergence(Fx, Fy, Fz, h):
    dFx_dx = (Fx[2:, 1:-1, 1:-1] - Fx[:-2, 1:-1, 1:-1]) / (2 * h)
    dFy_dy = (Fy[1:-1, 2:, 1:-1] - Fy[1:-1, :-2, 1:-1]) / (2 * h)
    dFz_dz = (Fz[1:-1, 1:-1, 2:] - Fz[1:-1, 1:-1, :-2]) / (2 * h)
    return dFx_dx + dFy_dy + dFz_dz

h = x[1] - x[0]
divF = divergence(Fx, Fy, Fz, h)

# 用某一個 z 切面可視化 divergence（例如 z = 5）
mid_z = divF.shape[2] // 2
plt.figure(figsize=(6, 5))
plt.title("Divergence of vector field at z-slice")
plt.contourf(X[1:-1, 1:-1, mid_z], Y[1:-1, 1:-1, mid_z], divF[:, :, mid_z], cmap='coolwarm')
plt.colorbar(label='Divergence')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
plt.show()
