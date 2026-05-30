import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",").dropna()

# Pairplot для важных признаков
sns.pairplot(df.sample(800, random_state=42),
             vars=["full_area", "living_area", "metro_distance_km", "price_rub"],
             hue="price_segment")
plt.savefig("plot_13_pairplot_tree_features.png", dpi=100, bbox_inches="tight")
plt.close()

# Дерево решений
features = ["full_area", "living_area", "metro_distance_km", "floor"]
X = df[features].values
y = df["price_segment"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)

print(f"Точность (max_depth=5): {accuracy_score(y_test, tree.predict(X_test)):.2%}")
print("\nСтруктура дерева (первые уровни):")
print(export_text(tree, feature_names=features, max_depth=3))
