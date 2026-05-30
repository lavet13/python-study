import pandas as pd

df = pd.read_csv("moscow_housing_study.csv", delimiter=",")

# Сортировки
sorted_price = df[["full_area", "price_rub", "region"]].sort_values(
    by="price_rub", ascending=False
)
print("--- Самые дорогие квартиры ---")
print(sorted_price.head())

sorted_area = df[["full_area", "price_rub", "region"]].sort_values(
    by="full_area", ascending=True
)
print("\n--- Самые маленькие квартиры ---")
print(sorted_area.head())

# iloc
most_expensive = df.sort_values(by="price_rub", ascending=False).iloc[0]
print("\n--- Самая дорогая квартира ---")
print(most_expensive)
