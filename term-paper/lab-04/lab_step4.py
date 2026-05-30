import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# One-Hot Encoding
df_ohe = pd.get_dummies(df, columns=["region", "renovation", "building_type"], drop_first=True)

print("--- Пример One-Hot Encoding ---")
print(df_ohe.columns.tolist()[:15])  # первые 15 столбцов

# Предсказание price_segment с OHE-признаками
feature_cols = [col for col in df_ohe.columns if col not in
                ['id', 'timestamp', 'price_rub', 'price_segment']]

X = df_ohe[feature_cols].values
y = df_ohe["price_segment"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

tree = DecisionTreeClassifier(max_depth=6, random_state=42)
tree.fit(X_train, y_train)

y_pred = tree.predict(X_test)

print(f"\nТочность с One-Hot Encoding: {accuracy_score(y_test, y_pred):.2%}")
print("Матрица ошибок:")
print(confusion_matrix(y_test, y_pred))
