import pandas as pd

df = pd.read_csv("learn_dataset.csv", delimiter=",")

# 1. Отбор строк по одному условию — булево индексирование.
# df[условие] возвращает только строки, где условие True.
high_income = df[df["class"] == ">50K"]
print(f"Записей с высоким доходом: {len(high_income)}")
print(high_income.head())

# 2. Отбор по двум условиям одновременно.
# & — логическое И. Каждое условие ОБЯЗАТЕЛЬНО в скобках.
# Без скобок Python вычислит & раньше == и получит ошибку.
high_income_male = df[(df["class"] == ">50K") & (df["sex"] == "Male")]
print(f"\nМужчин с высоким доходом: {len(high_income_male)}")
print(high_income_male.head())

# 3. Отбор конкретных столбцов для отфильтрованных строк.
# df.loc[условие, [список столбцов]] — фильтр строк + выбор столбцов.
older_subset = df.loc[df["age"] > 2, ["age", "education", "class"]]
print(f"\nЗаписей с age > 2: {len(older_subset)}")
print(older_subset.head())
