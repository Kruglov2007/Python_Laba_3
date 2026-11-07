import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
class InvalidConfigError(Exception):
    """Исключение для некорректных параметров конфигурации генератора."""
class DataExportError(Exception):
    """Исключение при невозможности сохранить итоговый CSV-файл."""

def validate_args(years: int, stores: int, out_path: str) :
    """Проверяет корректность аргументов командной строки."""
    if years <= 0 or years > 20:
        raise InvalidConfigError(f"Параметр --years должен быть от 1 до 20 (получено: {years}).")
    if stores < 5:
        raise InvalidConfigError(f"По ТЗ требуется не менее 5 магазинов (получено: {stores}).")
    if not out_path or not out_path.strip():
        raise InvalidConfigError("Путь выходного файла (--out) не может быть пустым.")
    return Path(out_path)

def build_stores(num_stores: int, rng: np.random.Generator) :
    """Формирует справочник магазинов и городов с базовыми коэффициентами трафика."""
    cities = ["Москва", "Санкт-Петербург", "Казань", "Екатеринбург", "Новосибирск", "Минск"]
    store_ids = [f"STORE_{i:02d}" for i in range(1, num_stores + 1)]
    assigned_cities = [cities[i % len(cities)] for i in range(num_stores)]
    store_multipliers = rng.uniform(0.75, 1.35, size=num_stores)
    return pd.DataFrame(
        {
            "store_id": store_ids,
            "city": assigned_cities,
            "store_mult": store_multipliers,
        }
    )

def build_catalog() :
    """Формирует каталог из 3 категорий и 9 товаров с индивидуальными трендами и сезонностью."""
    items = [
        # category, product, base_price, base_cost, base_qty, annual_trend, season_amp, season_phase
        ("Электроника", "Наушники TWS", 4500.0, 2700.0, 12, 0.25, 0.20, -1.5),
        ("Электроника", "Пауэрбанк 20000mAh", 3200.0, 1800.0, 15, 0.15, 0.15, -1.0),
        ("Электроника", "Умные часы", 8900.0, 5600.0, 7, 0.30, 0.30, -1.8),
        ("Одежда", "Футболка базовая", 1500.0, 650.0, 30, 0.05, 0.45, 1.5),
        ("Одежда", "Куртка демисезонная", 7500.0, 4100.0, 10, -0.05, 0.60, -2.5),
        ("Одежда", "Кроссовки городские", 6200.0, 3400.0, 14, 0.10, 0.40, 1.2),
        ("Дом и кухня", "Кофеварка капельная", 5400.0, 3100.0, 9, 0.12, 0.25, -1.5),
        ("Дом и кухня", "Набор сковород", 4100.0, 2200.0, 11, -0.10, 0.15, -1.2),
        ("Дом и кухня", "Термокружка 0.5л", 1800.0, 800.0, 22, 0.08, 0.35, -2.0),
    ]
    return pd.DataFrame(
        items,
        columns=[
            "category",
            "product",
            "base_price",
            "base_cost",
            "base_qty",
            "annual_trend",
            "season_amp",
            "season_phase",
        ],
    )

def generate_sales_data(seed: int, years: int, num_stores: int) :
    """Генерирует воспроизводимый датасет посуточных продаж с трендами, сезонностью, выбросами и пропусками."""
    rng = np.random.default_rng(seed=seed)

    start_date = pd.Timestamp("2023-01-01")
    end_date = start_date + pd.DateOffset(years=years) - pd.Timedelta(days=1)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    stores_df = build_stores(num_stores, rng)
    catalog_df = build_catalog()

    # Декартово произведение: даты × магазины × товары
    grid = (
        pd.DataFrame({"date": dates})
        .merge(stores_df, how="cross")
        .merge(catalog_df, how="cross")
    )

    n_rows = len(grid)
    day_index = (grid["date"] - start_date).dt.days.to_numpy()
    day_of_year = grid["date"].dt.dayofyear.to_numpy()
    day_of_week = grid["date"].dt.dayofweek.to_numpy()

    # 1. Индивидуальный линейный тренд по товарам
    trend_factor = 1.0 + grid["annual_trend"].to_numpy() * (day_index / 365.0)
    trend_factor = np.clip(trend_factor, 0.3, None)

    # 2. Недельная сезонность (пт-вс повышенный спрос) и годовая сезонность
    weekly_mult = np.where(day_of_week >= 4, 1.28, 0.90)
    yearly_mult = 1.0 + grid["season_amp"].to_numpy() * np.sin(
        2.0 * np.pi * day_of_year / 365.25 + grid["season_phase"].to_numpy()
    )

    # 3. Акции (promo): ~15% наблюдений, снижают цену и увеличивают объём продаж
    promo = rng.binomial(1, 0.15, size=n_rows)
    discount = np.where(promo == 1, rng.uniform(0.15, 0.25, size=n_rows), 0.0)
    promo_qty_boost = np.where(promo == 1, rng.uniform(1.5, 2.1, size=n_rows), 1.0)

    # 4. Случайный шум и расчёт базовых значений qty и price
    noise = rng.normal(1.0, 0.12, size=n_rows)
    expected_qty = (
        grid["base_qty"].to_numpy()
        * grid["store_mult"].to_numpy()
        * trend_factor
        * weekly_mult
        * yearly_mult
        * promo_qty_boost
        * noise
    )
    qty = np.maximum(1, np.round(expected_qty)).astype(int)

    price_noise = rng.normal(1.0, 0.02, size=n_rows)
    price = np.round(grid["base_price"].to_numpy() * (1.0 - discount) * price_noise, 2)
    cost = grid["base_cost"].to_numpy()

    # 5. Выбросы / аномалии (1.5% строк — резкий всплеск оптового спроса)
    outlier_mask = rng.random(n_rows) < 0.015
    qty = np.where(outlier_mask, qty * rng.integers(4, 9, size=n_rows), qty)

    # 6. Способы оплаты
    payment_methods = rng.choice(
        ["карта", "онлайн", "наличные"],
        size=n_rows,
        p=[0.55, 0.30, 0.15],
    )

    result_df = pd.DataFrame(
        {
            "date": grid["date"].dt.strftime("%Y-%m-%d"),
            "store_id": grid["store_id"],
            "city": grid["city"],
            "category": grid["category"],
            "product": grid["product"],
            "qty": qty,
            "price": price,
            "cost": cost,
            "promo": promo,
            "payment_method": payment_methods,
        }
    )

    # 7. Пропуски (по ~0.8% в price и payment_method, итого > 0.5%)
    price_na_mask = rng.random(n_rows) < 0.008
    pay_na_mask = rng.random(n_rows) < 0.008
    result_df.loc[price_na_mask, "price"] = np.nan
    result_df.loc[pay_na_mask, "payment_method"] = np.nan

    return result_df

def save_csv(df: pd.DataFrame, out_path: Path) :
    """Сохраняет DataFrame в CSV-файл с обработкой ошибок файловой системы."""
    try:
        if out_path.exists() and out_path.is_dir():
            raise DataExportError(f"Указанный путь '{out_path}' является директорией, а не файлом.")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False, encoding="utf-8")
    except OSError as exc:
        raise DataExportError(f"Ошибка записи файла '{out_path}': {exc}") from exc


def parse_cli_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="CLI-генератор синтетических посуточных данных о продажах сети магазинов."
    )
    parser.add_argument("--seed", type=int, default=42, help="Зерно генератора случайных чисел (по умолчанию: 42)")
    parser.add_argument("--years", type=int, default=3, help="Количество лет для генерации (по умолчанию: 3)")
    parser.add_argument("--stores", type=int, default=5, help="Количество магазинов, минимум 5 (по умолчанию: 5)")
    default_out = Path(__file__).resolve().parent / "data" / "sales.csv"
    parser.add_argument(
        "--out",
        type=str,
        default=str(default_out),
        help="Путь для сохранения итогового CSV-файла",
    )
    return parser.parse_args()


def main() :
    """Точка входа CLI-скрипта."""
    args = parse_cli_args()
    try:
        out_path = validate_args(years=args.years, stores=args.stores, out_path=args.out)
        df = generate_sales_data(seed=args.seed, years=args.years, num_stores=args.stores)
        save_csv(df, out_path)
        print(f"[Успех] Сгенерировано {len(df)} записей. Файл сохранён: {out_path}")
        return 0
    except (InvalidConfigError, DataExportError) as exc:
        print(f"[Ошибка] {exc}", file=sys.stderr)
        return 1
if __name__ == "__main__":
    sys.exit(main())