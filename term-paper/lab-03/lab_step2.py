import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",").dropna()

X = df[["full_area", "metro_distance_km", "price_rub"]].values
y = df["price_segment"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# KNN с 7 соседями
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

print(f"Точность KNN (n=7): {accuracy_score(y_test, y_pred):.2%}")

# Визуализация ошибок
df_vis = pd.DataFrame(X_test, columns=["full_area", "metro_distance_km", "price_rub"])
df_vis["true"] = y_test
df_vis["pred"] = y_pred
df_vis["error"] = 0
df_vis.loc[df_vis["true"] != df_vis["pred"], "error"] = 1

sns.scatterplot(
    data=df_vis, x="full_area", y="price_rub", hue="error", palette="coolwarm"
)
plt.title("Ошибки KNN (n=7): 0=верно, 1=ошибка")
plt.savefig("plot_12_knn_errors.png", dpi=100, bbox_inches="tight")
plt.close()
