import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# Для дерева решений берём больше признаков, как в учебнике.
# Деревья не требуют нормирования — они работают с пороговыми значениями,
# а не с расстояниями, поэтому масштаб признаков не важен.
features = ["capitalgain", "hoursperweek", "education-num", "age"]
df4 = df[features + ["sex"]].copy()

X = df4[features].values
y = df4["sex"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Визуализация парных диаграмм (как в учебнике перед обучением) ─────────────
sns.pairplot(df4.sample(2000, random_state=42), hue="sex", vars=features)
plt.savefig("plot_13_pairplot_tree_features.png", dpi=100, bbox_inches="tight")
plt.close()

# ── Дерево без ограничения глубины ────────────────────────────────────────────
# Без max_depth дерево растёт до полного разделения обучающих данных.
# Это часто приводит к переобучению: модель «выучивает» шум.
tree_full = DecisionTreeClassifier(random_state=42)
tree_full.fit(X_train, y_train)

y_pred_full = tree_full.predict(X_test)
acc_full = accuracy_score(y_test, y_pred_full)
cm_full = confusion_matrix(y_test, y_pred_full)
print(f"--- Дерево без ограничения глубины ---")
print(f"Глубина дерева: {tree_full.get_depth()}")
print(f"Точность (accuracy): {acc_full:.2%}")
print("Матрица ошибок:")
print(cm_full)

# Текстовый вывод дерева (первые уровни)
print("\n--- Структура дерева (первые 3 уровня) ---")
print(export_text(tree_full, feature_names=features, max_depth=3))

# ── Дерево с max_depth=3 ──────────────────────────────────────────────────────
# Ограничение глубины — это регуляризация: модель задаёт меньше вопросов,
# обобщает лучше и реже переобучается.
tree3 = DecisionTreeClassifier(max_depth=3, random_state=42)
tree3.fit(X_train, y_train)

y_pred3 = tree3.predict(X_test)
acc3 = accuracy_score(y_test, y_pred3)
cm3 = confusion_matrix(y_test, y_pred3)
print(f"\n--- Дерево с max_depth=3 ---")
print(f"Точность (accuracy): {acc3:.2%}")
print("Матрица ошибок:")
print(cm3)

print("\n--- Структура дерева (max_depth=3) ---")
print(export_text(tree3, feature_names=features))

# ── Метрики precision и recall для дерева глубиной 3 ─────────────────────────
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred3)
classes = tree3.classes_
print("\n--- Метрики по классам (max_depth=3) ---")
for i, cls in enumerate(classes):
    print(
        f"  {cls}: precision={precision[i]:.3f}, recall={recall[i]:.3f}, "
        f"f1={f1[i]:.3f}, support={support[i]}"
    )
