import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, confusion_matrix

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# ── 1. Дерево регрессии для предсказания цены ───────────────────────────────
df_reg = df.dropna(subset=["living_area", "metro_distance_km"]).copy()

X_reg = df_reg[["full_area", "living_area", "metro_distance_km", "floor"]].values
y_reg = df_reg["price_rub"].values

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# Полное дерево
tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(X_train_r, y_train_r)
y_pred_r = tree_reg.predict(X_test_r)
mae = mean_absolute_error(y_test_r, y_pred_r)

print("--- Дерево регрессии (без ограничения) ---")
print(f"Глубина дерева: {tree_reg.get_depth()}")
print(f"MAE: {mae:,.0f} руб.")

# Ограниченное дерево
tree_reg_limited = DecisionTreeRegressor(max_depth=8, random_state=42)
tree_reg_limited.fit(X_train_r, y_train_r)
y_pred_l = tree_reg_limited.predict(X_test_r)
mae_l = mean_absolute_error(y_test_r, y_pred_l)

print(f"\n--- Дерево регрессии (max_depth=8) ---")
print(f"MAE: {mae_l:,.0f} руб.")
