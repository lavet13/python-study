import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# LabelEncoder
coder = LabelEncoder()

# Кодируем категориальные признаки
cat_cols = ["region", "renovation", "building_type", "price_segment"]
df_encoded = df.copy()

for col in cat_cols:
    df_encoded[col] = coder.fit_transform(df_encoded[col].astype(str))

print("--- Пример кодирования region ---")
print(df[["region"]].head())
print(df_encoded[["region"]].head())

# Предсказание price_segment по физическим характеристикам
X_cat = df_encoded[["full_area", "metro_distance_km", "floor", "region"]].values
y_cat = df_encoded["price_segment"].values

X_train, X_test, y_train, y_test = train_test_split(
    X_cat, y_cat, test_size=0.2, random_state=42
)

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)

print(f"\nТочность предсказания ценового сегмента: {accuracy_score(y_test, tree.predict(X_test)):.2%}")

# Feature Importance
rf_imp = RandomForestClassifier(random_state=42)
rf_imp.fit(X_cat, y_cat)

importances = pd.Series(rf_imp.feature_importances_,
                       index=["full_area", "metro_distance_km", "floor", "region"])
print("\n--- Важность признаков ---")
print(importances.sort_values(ascending=False))
