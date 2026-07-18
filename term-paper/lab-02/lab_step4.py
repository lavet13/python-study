import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# Подготовка данных для кластеризации
features = ["full_area", "metro_distance_km", "price_rub"]
df_clust = df[features + ["region"]].dropna().copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clust[features])

# KMeans
model = KMeans(n_clusters=3, random_state=42, n_init=10)
df_clust["cluster"] = model.fit_predict(X_scaled)

print("--- Размер кластеров ---")
print(df_clust["cluster"].value_counts())

# Визуализация
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.scatterplot(data=df_clust, x="full_area", y="price_rub", hue="region", ax=axes[0])
axes[0].set_title("Реальные районы")

sns.scatterplot(
    data=df_clust,
    x="full_area",
    y="price_rub",
    hue="cluster",
    palette="tab10",
    ax=axes[1],
)
axes[1].set_title("Кластеры KMeans")

plt.savefig("plot_10_clustering.png", dpi=100, bbox_inches="tight")
plt.close()

print("Кластеризация завершена. График сохранён.")
