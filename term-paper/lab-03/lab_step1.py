import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# Фильтруем данные
df1 = df.dropna(subset=["living_area", "metro_distance_km"]).copy()

# Визуализация
sns.scatterplot(data=df1, x="full_area", y="price_rub", alpha=0.5)
plt.title("Зависимость цены от общей площади")
plt.savefig("plot_11_scatter_regression.png", dpi=100, bbox_inches="tight")
plt.close()

# Простая регрессия
X_simple = df1[["full_area"]].values
y = df1["price_rub"].values

X_train, X_test, y_train, y_test = train_test_split(
    X_simple, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print(
    f"Уравнение: price_rub ≈ {model.coef_[0]:.0f} * full_area + {model.intercept_:.0f}"
)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE: {mae:,.0f} руб.")
