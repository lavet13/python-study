import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# Полный датасет (не фильтруем нули) — задача классификации пола,
# а не регрессия прибыли, поэтому все строки релевантны.
# Признаки: capitalgain и hoursperweek — два числовых столбца с
# наибольшим различием между мужчинами и женщинами.
df2 = df[["capitalgain", "hoursperweek", "sex"]].copy()

X = df2[["capitalgain", "hoursperweek"]].values
y = df2["sex"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Нормирование (StandardScaler) ─────────────────────────────────────────────
# capitalgain и hoursperweek имеют разные единицы измерения и разный масштаб.
# Без нормирования расстояние в пространстве признаков будет некорректным:
# один пункт hoursperweek не равен одному пункту capitalgain.
# StandardScaler приводит каждый признак к нулевому среднему и единичному
# стандартному отклонению: x_new = (x - mean) / std.
# ВАЖНО: scaler обучается только на train, а transform применяется к обоим.
# Если обучить scaler на всех данных — произойдёт утечка информации из теста.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("--- Данные после нормирования (первые 3 строки) ---")
print(X_train_scaled[:3])

# ── KNN с n_neighbors=1 ───────────────────────────────────────────────────────
knn1 = KNeighborsClassifier(n_neighbors=1)
knn1.fit(X_train_scaled, y_train)
y_pred1 = knn1.predict(X_test_scaled)

acc1 = accuracy_score(y_test, y_pred1)
cm1  = confusion_matrix(y_test, y_pred1)
print(f"\n--- KNN (n_neighbors=1) ---")
print(f"Точность (accuracy): {acc1:.2%}")
print("Матрица ошибок:")
print(cm1)

# ── KNN с n_neighbors=7 ───────────────────────────────────────────────────────
# Увеличение числа соседей сглаживает решение: вместо одного ближайшего
# соседа учитывается мнение семи — это снижает влияние шумовых точек.
knn7 = KNeighborsClassifier(n_neighbors=7)
knn7.fit(X_train_scaled, y_train)
y_pred7 = knn7.predict(X_test_scaled)

acc7 = accuracy_score(y_test, y_pred7)
cm7  = confusion_matrix(y_test, y_pred7)
print(f"\n--- KNN (n_neighbors=7) ---")
print(f"Точность (accuracy): {acc7:.2%}")
print("Матрица ошибок:")
print(cm7)

# ── Визуализация ошибок ───────────────────────────────────────────────────────
# Code = 0 → верно предсказан; 1 → мужчина предсказан как женщина;
# 2 → женщина предсказана как мужчина.
df_test_vis = pd.DataFrame(X_test, columns=["capitalgain", "hoursperweek"])
df_test_vis["sex"]       = y_test
df_test_vis["predicted"] = y_pred7
df_test_vis["Code"] = 0
df_test_vis.loc[(df_test_vis["sex"] == "Male")   & (df_test_vis["predicted"] == "Female"), "Code"] = 1
df_test_vis.loc[(df_test_vis["sex"] == "Female") & (df_test_vis["predicted"] == "Male"),   "Code"] = 2

sns.scatterplot(data=df_test_vis, x="hoursperweek", y="capitalgain", hue="Code", palette="tab10")
plt.title("Ошибки KNN (n=7): 0=верно, 1=M→F, 2=F→M")
plt.savefig("plot_12_knn_errors.png", dpi=100, bbox_inches="tight")
plt.close()

print("\nГрафик сохранён.")
