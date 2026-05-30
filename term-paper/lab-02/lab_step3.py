import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# Работаем с ценами — они имеют выбросы
df_price = df.copy()

# 1. Boxplot до очистки
sns.boxplot(data=df_price, y="price_rub")
plt.title("Ящик с усами: price_rub (до фильтрации)")
plt.savefig("plot_07_boxplot_before.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 2. Правило трёх сигм ─────────────────────────────────────────────────────
m = df_price["price_rub"].mean()
s = df_price["price_rub"].std()
left_1 = m - 3 * s
right_1 = m + 3 * s

print(f"\nСпособ 1 (3σ) — диапазон: [{left_1:,.0f}; {right_1:,.0f}]")

df_clean1 = df_price[(df_price["price_rub"] >= left_1) & (df_price["price_rub"] <= right_1)]

sns.boxplot(data=df_clean1, y="price_rub")
plt.title("После удаления по правилу 3σ")
plt.savefig("plot_08_boxplot_3sigma.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 3. Метод IQR ─────────────────────────────────────────────────────────────
Q1 = df_price["price_rub"].quantile(0.25)
Q3 = df_price["price_rub"].quantile(0.75)
IQR = Q3 - Q1
left_2 = Q1 - 1.5 * IQR
right_2 = Q3 + 1.5 * IQR

print(f"Способ 2 (IQR) — диапазон: [{left_2:,.0f}; {right_2:,.0f}]")

df_clean2 = df_price[(df_price["price_rub"] >= left_2) & (df_price["price_rub"] <= right_2)]

sns.boxplot(data=df_clean2, y="price_rub")
plt.title("После удаления по методу IQR")
plt.savefig("plot_09_boxplot_iqr.png", dpi=100, bbox_inches="tight")
plt.close()

print(f"\nОсталось после 3σ: {len(df_clean1)} строк")
print(f"Осталось после IQR: {len(df_clean2)} строк")
