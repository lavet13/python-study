import pandas as pd

df = pd.read_csv("moscow_housing_study.csv", delimiter=",")

# 1. Фильтрация по цене
premium = df[df["price_segment"] == "Premium"]
print(f"Квартир премиум-класса: {len(premium)}")

# 2. Фильтрация по нескольким условиям
large_moscow = df[(df["full_area"] > 80) & (df["region"] == "Moscow")]
print(f"\nБольших квартир в Москве: {len(large_moscow)}")

# 3. Выбор конкретных столбцов
subset = df.loc[
    df["metro_distance_km"] < 1, ["full_area", "price_rub", "price_segment"]
]
print(f"\nКвартир в пешей доступности от метро: {len(subset)}")
print(subset.head())
