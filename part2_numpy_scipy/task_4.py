import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import dblquad, quad
def main():
    val_1d, _ = quad(lambda x: x * np.sin(x), 0, np.pi)
    exact_1d = np.pi
    err_1d = abs(val_1d - exact_1d)
    print("=== 1. Определённый интеграл (quad) ===")
    print(f"Численное значение:     {val_1d:.10f}")
    print(f"Аналитическое значение: {exact_1d:.10f}")
    print(f"Абсолютная погрешность: {err_1d:.2e}\n")

    val_2d, _ = dblquad(lambda y, x: x + y, 0, 1, lambda x: 0, lambda x: x)
    exact_2d = 0.5
    err_2d = abs(val_2d - exact_2d)
    print("=== 2. Двойной интеграл (dblquad) ===")
    print(f"Численное значение:     {val_2d:.10f}")
    print(f"Аналитическое значение: {exact_2d:.10f}")
    print(f"Абсолютная погрешность: {err_2d:.2e}\n")
    rng = np.random.default_rng(seed=42)
    n_values = np.array([10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6])

    def estimate_mc(n: int) :
        x = rng.uniform(0.0, 1.0, size=int(n))
        y = rng.uniform(0.0, 1.0, size=int(n))
        values = np.where(y <= x, x + y, 0.0)
        est = float(np.mean(values))
        return est, abs(est - exact_2d)

    mc_estimates, mc_errors = np.vectorize(estimate_mc)(n_values)

    print("=== 3. Метод Монте-Карло ===")
    summary = np.column_stack((n_values, mc_estimates, mc_errors))
    print(f"N\t  Оценка\t Погрешность\n{summary}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(n_values, mc_errors, marker="o", linewidth=2, color="teal", label="Погрешность Монте-Карло")
    ref_line = mc_errors[0] * np.sqrt(n_values[0] / n_values)
    ax.loglog(n_values, ref_line, linestyle="--", color="gray", label=r"Теоретический наклон $O(N^{-1/2})$")
    ax.set_title("Сходимость метода Монте-Карло для двойного интеграла", fontsize=13)
    ax.set_xlabel("Количество точек $N$ (лог. шкала)", fontsize=11)
    ax.set_ylabel("Абсолютная погрешность (лог. шкала)", fontsize=11)
    ax.grid(True, which="both", linestyle=":", alpha=0.7)
    ax.legend()

    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    main()