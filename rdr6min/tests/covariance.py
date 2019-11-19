import numpy as np
import matplotlib.pyplot as plt


# Covariance
def cov(x, y):
    xbar, ybar = x.mean(), y.mean()
    return np.sum((x - xbar) * (y - ybar)) / (len(x) - 1)


# Covariance matrix
def cov_mat(X):
    return np.array([[cov(X[0], X[0]), cov(X[0], X[1])], \
                     [cov(X[1], X[0]), cov(X[1], X[1])]])


plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 8)

# Normal distributed x and y vector with mean 0 and standard deviation 1
x = np.random.normal(0, 1, 500)
y = np.random.normal(0, 1, 500)
X = np.vstack((x, y)).T

plt.scatter(X[:, 0], X[:, 1])
plt.title('Generated Data')
plt.axis('equal');

# Calculate covariance matrix
print(cov_mat(X.T))  # (or with np.cov(X.T))

# Center the matrix at the origin
X = X - np.mean(X, 0)

# Scaling matrix
sx, sy = 0.7, 3.4
Scale = np.array([[sx, 0], [0, sy]])

# Apply scaling matrix to X
Y = X.dot(Scale)

plt.scatter(Y[:, 0], Y[:, 1])
plt.title('Transformed Data')
plt.axis('equal')

# Calculate covariance matrix
print(cov_mat(Y.T))

# Scaling matrix
sx, sy = 0.7, 3.4
Scale = np.array([[sx, 0], [0, sy]])

# Rotation matrix
theta = 0.77 * np.pi
c, s = np.cos(theta), np.sin(theta)
Rot = np.array([[c, -s], [s, c]])

# Transformation matrix
T = Scale.dot(Rot)

# Apply transformation matrix to X
Y = X.dot(T)

plt.scatter(Y[:, 0], Y[:, 1])
plt.title('Transformed Data')
plt.axis('equal');
# Calculate covariance matrix
print(cov_mat(Y.T))
# 知道C是什么样的
C = cov_mat(Y.T)
# 可以对C进行奇异值分解，eVe是特征值，eVa是特征向量
eVe, eVa = np.linalg.eig(C)
print(eVe)
print(eVa)
plt.scatter(Y[:, 0], Y[:, 1])
# zip是把对应项放在一起，参见blog：https://blog.csdn.net/csdn15698845876/article/details/73411541
for e, v in zip(eVe, eVa.T):
    # 显示主轴
    plt.plot([0, 3 * np.sqrt(e) * v[0]], [0, 3 * np.sqrt(e) * v[1]], 'k-', lw=2)
plt.title('Transformed Data')
plt.axis('equal');


C = cov_mat(Y.T)

# Calculate eigenvalues
eVa, eVe = np.linalg.eig(C)

# Calculate transformation matrix from eigen decomposition
R, S = eVe, np.diag(np.sqrt(eVa))
T = R.dot(S).T

# Transform data with inverse transformation matrix T^-1
Z = Y.dot(np.linalg.inv(T))

plt.scatter(Z[:, 0], Z[:, 1])
plt.title('Uncorrelated Data')
plt.axis('equal');

# Covariance matrix of the uncorrelated data
cov_mat(Z.T)