import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# Те же признаки и та же полная выборка, что и в kNN —
# для корректного сравнения методов условия должны совпадать.
df3 = df[["capitalgain", "hoursperweek", "sex"]].copy()

X = df3[["capitalgain", "hoursperweek"]].values
y = df3["sex"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Нормирование обязательно для SGDClassifier: алгоритм основан на
# градиентном спуске, который чувствителен к масштабу признаков.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ── SGDClassifier (линейный классификатор) ────────────────────────────────────
# Ищет разделяющую гиперплоскость (прямую в 2D), которая отделяет
# мужчин от женщин. random_state фиксирует начальные веса.
clf = SGDClassifier(random_state=42)
clf.fit(X_train_scaled, y_train)

y_pred = clf.predict(X_test_scaled)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print(f"--- Линейный классификатор (SGDClassifier) ---")
print(f"Точность (accuracy): {acc:.2%}")
print("Матрица ошибок:")
print(cm)

# ── Метрики precision и recall ────────────────────────────────────────────────
# precision (точность класса) — доля верных среди предсказанных данного класса.
# recall   (полнота класса)   — доля верных среди всех реальных данного класса.
# ВАЖНО: порядок аргументов — сначала реальные метки, потом предсказанные!
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred)

print("\n--- Метрики по классам ---")
classes = clf.classes_
for i, cls in enumerate(classes):
    print(
        f"  {cls}: precision={precision[i]:.3f}, recall={recall[i]:.3f}, "
        f"f1={f1[i]:.3f}, support={support[i]}"
    )
