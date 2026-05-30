import pandas as pd

# Загружаем датасет московской недвижимости
df = pd.read_csv("moscow_housing_study.csv", delimiter=",")

print("--------Общая информация--------")
df.info()

print(f"\nРазмерность датасета: {df.shape}")

print("\n--- Первые 5 строк таблицы ---")
print(df.head())

print("\n--- Список признаков ---")
print(df.columns.tolist())

print("\n--- Последние 5 строк таблицы ---")
print(df.tail())

print("\n--- Описательные статистики (числовые) ---")
print(df.describe())

print("\n--- Описательные статистики (категориальные) ---")
print(df.describe(include='object'))
