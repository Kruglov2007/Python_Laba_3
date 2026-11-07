import numpy as np

def input_float_array(enter:str):
    while True:
        raw=input(enter).strip()
        if not raw:
            print("Ввод не может быть пустым!")
            continue
        try:
            arr=np.array(raw.split(), dtype=float)
            if np.any(arr<=0):
                print("Значения должны быть строго больше нуля")
                continue
            return arr
        except ValueError:
            print("Ошибка: введите корректные числа, разделённые пробелами.")
def input_int(enter:str, min_val: int, max_val: int):
    while True:
        raw=input(enter).strip()
        try:
            val=int(raw)
            if not(min_val<=val<=max_val):
                 print(f"Ошибка: число должно быть в диапазоне от {min_val} до {max_val}.")
                 continue
            return val
        except ValueError:
            print("Ошибка: введите целое число.")
def input_time(t:str,max_time:float):
    while True:
        raw=input(t).strip()
        try:
            val=float(raw)
            if val < 0:
                print("Ошибка: время не может быть отрицательным.")
                continue
            if val > max_time:
                print(f"Ошибка: время t ({val} ч) превышает общее время в пути ({max_time:.2f} ч).")
                continue
            return val
        except ValueError:
            print("Ошибка: введите числовое значение для времени.")


def main():
    while True:
        lengths = input_float_array("Длины:    ")
        speeds = input_float_array("Скорости: ")
        if lengths.size!=speeds.size:
            print(f"Ошибка: количество длин ({lengths.size}) не совпадает с количеством скоростей ({speeds.size}).\n")
            continue
        break


    n = lengths.size
    k = input_int(f"Введите начальный участок k (от 1 до {n}): ", 1, n)
    p = input_int(f"Введите конечный участок p (от {k} до {n}): ", k, n)

    sub_lengths = lengths[k - 1: p]
    sub_speeds = speeds[k - 1: p]
    sub_times = sub_lengths / sub_speeds
    total_length = np.sum(sub_lengths)
    total_time = np.sum(sub_times)
    mid_speed = total_length / total_time
    t = input_time(f"Введите время t в часах (от 0 до {total_time:.2f}): ", total_time)
    cum_times = np.cumsum(sub_times)
    if np.isclose(t, total_time):
        current_section = p
        dist_from_start = sub_lengths[-1]
    else:
        idx = int(np.searchsorted(cum_times, t, side="right"))
        current_section = k + idx
        prev_time = cum_times[idx - 1] if idx > 0 else 0.0
        dist_from_start = (t - prev_time) * sub_speeds[idx]

    print(f"S = {total_length:g} км, T = {total_time:.2f} ч, V = {mid_speed:.2f} км/ч")
    print(f"Через {t:g} ч автомобиль на участке {current_section}, в {dist_from_start:.1f} км от его начала")

if __name__ == '__main__':
    main()