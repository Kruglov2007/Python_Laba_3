import numpy as np


def main():
    expenses=np.array([3200, 3100, 2600, 1900, 1500, 1300, 1250, 1400, 1800, 2300, 2900, 3500])
    winter_sum=expenses[[0,1,11]].sum()
    summer_sum=expenses[5:8].sum()
    if winter_sum>summer_sum:
        max_season="больше тратится зимой"
    if winter_sum < summer_sum:
        max_season="больше тратится летом"
    if winter_sum==summer_sum:
        max_season="Одинаковые расходы"
    max_val=np.max(expenses)
    max_months = np.where(expenses == max_val)[0] + 1
    months_str = ", ".join(map(str, max_months))
    print(f"Расходы: {' '.join(map(str, expenses))}")
    print(f"Зима: {winter_sum}, лето: {summer_sum} -> {max_season}")

    print(f"Максимум ({max_val}) в месяцах: {months_str}")


if __name__ == "__main__":
    main()