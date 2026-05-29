import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, precision_recall_fscore_support, confusion_matrix

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# ── 1. Решающее дерево для задачи регрессии ───────────────────────────────────
# Деревья применимы не только к классификации, но и к регрессии.
# Фильтруем нулевой capitalgain — нас интересуют только инвесторы.
df_reg = df[df["capitalgain"] > 0].copy()

# Признаки: hoursperweek и education-num (числовые, как в workbook).
# Рост (height) в нашем датасете отсутствует — используем education-num.
X_reg = df_reg[["hoursperweek", "education-num"]].values
y_reg = df_reg["capitalgain"].values

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# Дерево без ограничения глубины
tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(X_train_r, y_train_r)
y_pred_r = tree_reg.predict(X_test_r)
mae_reg = mean_absolute_error(y_test_r, y_pred_r)
print(f"--- Дерево регрессии (без ограничения) ---")
print(f"Глубина: {tree_reg.get_depth()}")
print(f"MAE: {mae_reg:.4f}")

# Дерево с max_depth=10 — как в учебнике, уменьшает ошибку
tree_reg10 = DecisionTreeRegressor(max_depth=10, random_state=42)
tree_reg10.fit(X_train_r, y_train_r)
y_pred_r10 = tree_reg10.predict(X_test_r)
mae_reg10 = mean_absolute_error(y_test_r, y_pred_r10)
print(f"\n--- Дерево регрессии (max_depth=10) ---")
print(f"MAE: {mae_reg10:.4f}")
print(f"Улучшение MAE: {mae_reg - mae_reg10:.4f}")

# ── 2. Случайный лес (Random Forest — бэггинг) ────────────────────────────────
# Бэггинг: обучающая выборка делится на части, каждая часть обучает
# отдельное дерево, результаты усредняются. Не требует нормирования.
features_clf = ["capitalgain", "hoursperweek", "education-num", "age"]
X_clf = df[features_clf].values
y_clf = df["sex"].values

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(random_state=42)
rf.fit(X_train_c, y_train_c)
y_pred_rf = rf.predict(X_test_c)

acc_rf = accuracy_score(y_test_c, y_pred_rf)
cm_rf  = confusion_matrix(y_test_c, y_pred_rf)
prec_rf, rec_rf, f1_rf, sup_rf = precision_recall_fscore_support(y_test_c, y_pred_rf)

print(f"\n--- Случайный лес (RandomForest) ---")
print(f"Точность (accuracy): {acc_rf:.2%}")
print("Матрица ошибок:")
print(cm_rf)
print("Метрики по классам:")
for i, cls in enumerate(rf.classes_):
    print(f"  {cls}: precision={prec_rf[i]:.3f}, recall={rec_rf[i]:.3f}, f1={f1_rf[i]:.3f}")

# ── 3. Градиентный бустинг ────────────────────────────────────────────────────
# Бустинг: деревья строятся последовательно, каждое следующее
# минимизирует ошибку предыдущего ансамбля. Тоже не требует нормирования.
gb = GradientBoostingClassifier(random_state=42)
gb.fit(X_train_c, y_train_c)
y_pred_gb = gb.predict(X_test_c)

acc_gb = accuracy_score(y_test_c, y_pred_gb)
cm_gb  = confusion_matrix(y_test_c, y_pred_gb)
prec_gb, rec_gb, f1_gb, sup_gb = precision_recall_fscore_support(y_test_c, y_pred_gb)

print(f"\n--- Градиентный бустинг (GradientBoosting) ---")
print(f"Точность (accuracy): {acc_gb:.2%}")
print("Матрица ошибок:")
print(cm_gb)
print("Метрики по классам:")
for i, cls in enumerate(gb.classes_):
    print(f"  {cls}: precision={prec_gb[i]:.3f}, recall={rec_gb[i]:.3f}, f1={f1_gb[i]:.3f}")
