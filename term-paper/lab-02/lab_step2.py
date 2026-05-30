import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# 1. Обнаружение пропусков
print("--- Количество пропусков по столбцам ---")
print(df.isnull().sum())

# Замена на NaN (если есть строковые маркеры, но в этом датасете уже NaN)
df_with_na = df.copy()

# 2. Удаление строк с пропусками
df_dropped = df_with_na.dropna()
print(f"\nПосле dropna(): осталось строк: {len(df_dropped)} из {len(df)}")

# 3. Заполнение медианой (лучше для числовых)
df_filled = df_with_na.copy()
for col in ["living_area", "kitchen_area", "metro_distance_km"]:
    median_val = df_filled[col].median()
    df_filled[col] = df_filled[col].fillna(median_val)
    print(f"  {col}: пропуски заполнены медианой ({median_val:.2f})")

print(f"\nПосле заполнения: пропусков осталось: {df_filled.isnull().sum().sum()}")
