import pandas as pd

df = pd.read_csv("moscow_housing_study.csv", delimiter=",")

# Новый признак: отношение жилой площади к общей
df["living_ratio"] = df["living_area"] / df["full_area"]

print("--- Первые 5 строк с living_ratio ---")
print(df[["full_area", "living_area", "living_ratio"]].head())

# Корреляции
corr_matrix = df.corr(numeric_only=True)
print("\n--- Матрица корреляций ---")
print(corr_matrix[["price_rub"]].sort_values("price_rub", ascending=False))

# Группировки
print("\n--- Средняя цена по району ---")
print(df.groupby("region")["price_rub"].mean())

print("\n--- Средняя цена по типу ремонта ---")
print(df.groupby("renovation")["price_rub"].mean())
