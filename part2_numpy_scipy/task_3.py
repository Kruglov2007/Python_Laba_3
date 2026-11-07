import numpy as np
def main():
    A = np.array(
        [
            [4.0, -1.5, 2.0, 0.5],
            [1.0, 5.0, -2.0, 1.2],
            [-2.0, 1.0, 6.0, -1.0],
            [0.5, 2.0, -1.0, 7.0],
        ],
        dtype=float,
    )
    B = np.array([[11.05], [-6.82], [11.5], [-0.5]], dtype=float)
    det_A = np.linalg.det(A)
    cond_A = np.linalg.cond(A)
    print(f"Определитель матрицы det(A) = {det_A:.4f}")
    if np.isclose(det_A, 0.0):
        print("Ошибка: определитель равен нулю, система не имеет единственного решения.")
        return
    print(f"Число обусловленности cond(A) = {cond_A:.4f}\n")
    A_inv = np.linalg.inv(A)
    X_inv = A_inv @ B

    X_solve = np.linalg.solve(A, B)
    diff_norm = np.linalg.norm(X_inv - X_solve)
    residual_norm = np.linalg.norm(A @ X_solve - B)
    print(f"Норма разности решений ||X_inv - X_solve||: {diff_norm:.2e}")
    print(f"Проверка подстановкой ||A·X - B||:   {residual_norm:.2e}\n")
    solution_rounded = np.round(X_solve.ravel(), 1)
    print(f"Вектор решения X: {solution_rounded}")

if __name__ == "__main__":
    main()