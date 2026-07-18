import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",").dropna()

features = ["full_area", "living_area", "kitchen_area", "metro_distance_km", "floor"]
X = df[features].values
y = df["price_segment"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# predict_proba
proba = rf.predict_proba(X_test)

print(f"Классы: {rf.classes_}")
print("\nПервые 5 вероятностей:")
print(proba[:5])

# Добавляем вероятности в DataFrame
df_test = pd.DataFrame(X_test, columns=features)
df_test["real_segment"] = y_test
df_test["prob_Budget"] = proba[:, 0]
df_test["prob_Standard"] = proba[:, 1]
df_test["prob_Premium"] = proba[:, 2]

print("\n--- Первые 8 строк с вероятностями ---")
print(df_test[["real_segment", "prob_Budget", "prob_Standard", "prob_Premium"]].head(8))
