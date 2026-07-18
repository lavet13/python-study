import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

features = ["capitalgain", "hoursperweek", "education-num", "age"]
X = df[features].values
y = df["sex"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)

# ── predict_proba() вместо predict() ─────────────────────────────────────────
# predict() возвращает конкретный класс: 'Male' или 'Female'.
# predict_proba() возвращает вероятности принадлежности к каждому классу.
# Сумма вероятностей в каждой строке всегда равна 1.0.
# Порядок классов можно проверить через rf.classes_.
result = rf.predict_proba(X_test)
print(f"Классы модели: {rf.classes_}")
print(f"\nПервые 5 строк predict_proba:")
print(result[:5])
print("(столбец 0 = Female, столбец 1 = Male)")

# Добавляем вероятности в датасет как отдельные столбцы.
# Индексы 0 и 1 соответствуют классам в rf.classes_ (Female=0, Male=1).
df_test = pd.DataFrame(X_test, columns=features)
df_test["sex_real"] = y_test
df_test["prob_Female"] = result[:, 0]
df_test["prob_Male"] = result[:, 1]

print("\n--- Первые 10 строк с вероятностями ---")
print(df_test[["sex_real", "prob_Female", "prob_Male"]].head(10))

# Проверка: там где реальный пол Male, prob_Male должна быть выше.
male_rows = df_test[df_test["sex_real"] == "Male"]
print(f"\nСреднее prob_Male у реальных мужчин:   {male_rows['prob_Male'].mean():.3f}")
female_rows = df_test[df_test["sex_real"] == "Female"]
print(f"Среднее prob_Male у реальных женщин: {female_rows['prob_Male'].mean():.3f}")
