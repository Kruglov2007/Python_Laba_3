import matplotlib.pyplot as plt
import numpy as np
def main():
    x=np.arange(-8, 8.01, 0.01)
    #y(x) = 4 / (x² − 4)
    y=4/(x**2-4)
    threshold = 0.05
    y = np.where(np.abs(x - 2) < threshold, np.nan, y)
    y = np.where(np.abs(x + 2) < threshold, np.nan, y)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, label=r"$y(x) = \frac{4}{x^2 - 4}$", linewidth=2.5)
    ax.axvline(x=-2, color="gray", linestyle="--", linewidth=1.5, label="Вертикальные асимптоты ($x = \pm 2$)")
    ax.axvline(x=2, color="gray", linestyle="--", linewidth=1.5)
    ax.set_title("График функции с разрывами в точках $x = \pm 2$", fontsize=14)
    ax.set_xlabel("Ось X", fontsize=12)
    ax.set_ylabel("Ось Y", fontsize=12)
    ax.set_ylim(-10, 10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", fontsize=12)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()


