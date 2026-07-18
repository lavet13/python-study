import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# ── 1. LabelEncoder: замена категориальных признаков на числовые ──────────────
# Алгоритмы ML работают только с числами. LabelEncoder присваивает
# каждому уникальному строковому значению целое число (0, 1, 2, ...).
# Порядок кодирования — алфавитный.
coder = LabelEncoder()

# Кодируем один признак — 'race':
df["race_encoded"] = coder.fit_transform(df["race"])
print("--- Маппинг race → число ---")
for i, cls in enumerate(coder.classes_):
    print(f"  {i}: {cls}")
print(df[["race", "race_encoded"]].head())

# Кодирование нескольких признаков в цикле:
cat_cols = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
    "class",
]
df_encoded = df.copy()
for col in cat_cols:
    df_encoded[col] = coder.fit_transform(df_encoded[col].astype(str))

print("\n--- Датасет после кодирования (первые 3 строки) ---")
print(df_encoded.head(3))

# ── 2. Предсказание пола по двум категориальным признакам ────────────────────
# marital-status и relationship — до кодирования категориальные,
# теперь числовые. Проверяем, можно ли по ним предсказать пол.
X_cat = df_encoded[["marital-status", "relationship"]].values
y_cat = df_encoded["sex"].values

X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
    X_cat, y_cat, test_size=0.2, random_state=42
)

tree_cat = DecisionTreeClassifier(max_depth=3, random_state=42)
tree_cat.fit(X_train_cat, y_train_cat)
y_pred_cat = tree_cat.predict(X_test_cat)

print(f"\n--- Предсказание пола по marital-status + relationship ---")
print(f"Точность: {accuracy_score(y_test_cat, y_pred_cat):.2%}")
print("Матрица ошибок:")
print(confusion_matrix(y_test_cat, y_pred_cat))

# ── 3. Селекция признаков (feature importance) ────────────────────────────────
# Случайный лес вычисляет важность каждого признака — насколько сильно
# он снижает неопределённость при построении деревьев.
# Значения нормированы: сумма по всем признакам = 1.0.
from sklearn.ensemble import RandomForestClassifier

# Перекодируем всё заново от исходного датасета (чистого).
df2 = pd.read_csv("../learn_dataset.csv", delimiter=",")
for col in cat_cols:
    df2[col] = coder.fit_transform(df2[col].astype(str))

# Оцениваем важность признаков для предсказания 'education'.
mas = [
    "age",
    "workclass",
    "fnlwgt",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capitalgain",
    "capitalloss",
    "hoursperweek",
    "native-country",
]

X_sel = df2[mas].values
y_sel = df2["education"].values

rf_sel = RandomForestClassifier(random_state=42, n_estimators=100)
rf_sel.fit(X_sel, y_sel)

# feature_importances_ — массив той же длины, что и список признаков.
importances = rf_sel.feature_importances_
importance_df = pd.DataFrame({"feature": mas, "importance": importances}).sort_values(
    "importance", ascending=False
)

print("\n--- Важность признаков для предсказания 'education' ---")
print(importance_df.to_string(index=False))
