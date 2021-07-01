import numpy as np

ITERATION_LIMIT = 1000


A = np.array([[10., 1, 2., 1],
              [-1., 11., 7, 3.],
              [2., 7, 10., -1.],
              [0., 3, -1., 8.]])
# initialize the RHS vector
b = np.array([6.0, 25.0, -11.0, 15.0])

print("система рівннянь:")
for i in range(A.shape[0]):
    row = ["{0:3g}*x{1}".format(A[i, j], j + 1) for j in range(A.shape[1])]
    print("[{0}] = [{1:3g}]".format(" + ".join(row), b[i]))

x = np.zeros_like(b)
for it_count in range(1, ITERATION_LIMIT):
    x_new = np.zeros_like(x)
    print("Iteration {0}: {1}".format(it_count, x))
    for i in range(A.shape[0]):
        s1 = np.dot(A[i, :i], x_new[:i])
        s2 = np.dot(A[i, i + 1 :], x[i + 1 :])
        x_new[i] = (b[i] - s1 - s2) / A[i, i]
    if np.allclose(x, x_new, rtol=1e-8):
        break
    x = x_new

print("Відповідь: {0}".format(x))
error = np.dot(A, x) - b
print("Помилкаа: {0}".format(error))
