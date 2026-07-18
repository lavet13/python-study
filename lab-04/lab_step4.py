import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# ── Проблема LabelEncoder ─────────────────────────────────────────────────────
# LabelEncoder кодирует Female=0, Male=1. Но тогда модель может
# «думать», что Female < Male в числовом смысле, что некорректно.
# One-hot encoding решает это: каждое значение → отдельный бинарный столбец.

# ── 1. get_dummies(): базовый пример ─────────────────────────────────────────
df_demo = df[["sex", "hoursperweek"]].copy()
df_ohe = pd.get_dummies(df_demo)
print("--- Результат get_dummies (первые 5 строк) ---")
print(df_ohe.head())
print(f"\nСтолбцы: {df_ohe.columns.tolist()}")

# ── 2. drop_first=True: удаление избыточного столбца ─────────────────────────
# Если Sex_Male=1, то Sex_Female гарантированно = 0, второй столбец лишний.
# drop_first убирает первый столбец каждой категориальной переменной.
df_ohe2 = pd.get_dummies(df_demo, drop_first=True)
print("\n--- После drop_first=True ---")
print(df_ohe2.head())
print(f"\nСтолбцы: {df_ohe2.columns.tolist()}")

# ── 3. Предсказание Sex_Male с помощью решающего дерева ──────────────────────
# Теперь целевой признак — бинарный столбец 'sex_Male' (True/False),
# а не строка 'Male'/'Female'.
df_full = df[["hoursperweek", "education-num", "age", "capitalgain", "sex"]].copy()
df_full = pd.get_dummies(df_full, columns=["sex"], drop_first=True)

# get_dummies создаёт булев столбец; преобразуем в int для ясности.
target_col = "sex_Male"
df_full[target_col] = df_full[target_col].astype(int)

print(f"\n--- Целевой признак после get_dummies: '{target_col}' ---")
print(df_full[[target_col]].value_counts())

feature_cols = ["hoursperweek", "education-num", "age", "capitalgain"]
X = df_full[feature_cols].values
y = df_full[target_col].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)

print(f"\n--- Предсказание '{target_col}' (дерево, max_depth=3) ---")
print(f"Точность: {accuracy_score(y_test, y_pred):.2%}")
print("Матрица ошибок:")
print(confusion_matrix(y_test, y_pred))
