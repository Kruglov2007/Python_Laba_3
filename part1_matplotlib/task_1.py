import matplotlib.pyplot as plt
import numpy as np
def main():
    x_deg = np.arange(-360, 361, 1)
    x_rad = np.deg2rad(x_deg)
    #p(x) = e^(sin x) + ln(sin²(0.5x) + 1) · cos x
    p=np.exp(np.sin(x_rad))+ np.log(np.sin(0.5*x_rad)**2+1)*np.cos(x_rad)
    #q(x) = −ln((sin x − cos x)² + 2) + 8
    q=-np.log((np.sin(x_rad)-np.cos(x_rad))**2+2)+8

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

    ax1.plot(x_deg,p, label=r"$p(x) = e^{\sin x} + \ln(\sin^2(0.5x) + 1) \cdot \cos x$", color="crimson", linewidth=2)
    ax1.set_title("График функции $p(x)$", fontsize=14)
    ax1.set_ylabel("Значения $p(x)$", fontsize=12)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=10)

    ax2.plot(x_deg, q, label=r"$q(x) = -\ln((\sin x - \cos x)^2 + 2) + 8$", color="royalblue", linewidth=2)
    ax2.set_title("График функции $q(x)$", fontsize=14)
    ax2.set_ylabel("Значения $q(x)$", fontsize=12)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=10)

    ticks_range = np.arange(-360, 361, 90)
    plt.xticks(ticks_range)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()