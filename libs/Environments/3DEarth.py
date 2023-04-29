import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 좌표를 생성하기 위한 각도 범위 설정
phi = np.linspace(0, np.pi, 100)
theta = np.linspace(0, 2 * np.pi, 100)

# 각도를 좌표로 변환
phi, theta = np.meshgrid(phi, theta)

# 구의 반지름 설정 (예: 반지름 1)
radius = 1

# 구의 좌표를 계산
x = radius * np.sin(phi) * np.cos(theta)
y = radius * np.sin(phi) * np.sin(theta)
z = radius * np.cos(phi)

# 그래프 그리기
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, color='b', alpha=1.0)  # 투명도를 조절하려면 alpha 값을 변경하세요.

# 축 레이블 설정
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 그래프 보여주기
plt.show()
