import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# 1. Распределение общей площади
sns.displot(df["full_area"], bins=30)
plt.title("Распределение общей площади квартир")
plt.savefig("./plot_01_displot_full_area.png", dpi=100, bbox_inches="tight")
plt.close()

sns.displot(df["full_area"], kind="kde")
plt.title("Функция плотности распределения full_area")
plt.savefig("./plot_02_kde_full_area.png", dpi=100, bbox_inches="tight")
plt.close()

# 2. Зависимость цены от площади
sns.scatterplot(data=df, x="full_area", y="price_rub", hue="region", alpha=0.6)
plt.title("Зависимость цены от общей площади")
plt.savefig("./plot_03_scatter_area_price.png", dpi=100, bbox_inches="tight")
plt.close()

# 3. Распределение по району и типу ремонта
sns.countplot(data=df, x="region")
plt.title("Распределение квартир по районам")
plt.savefig("./plot_04_countplot_region.png", dpi=100, bbox_inches="tight")
plt.close()

sns.countplot(data=df, x="region", hue="renovation")
plt.title("Распределение по району и ремонту")
plt.xticks(rotation=15)
plt.savefig("./plot_05_countplot_region_renovation.png", dpi=100, bbox_inches="tight")
plt.close()

# 4. Pairplot ключевых признаков
df_pair = df[["full_area", "living_area", "kitchen_area", "price_rub", "region"]]
sns.pairplot(df_pair, hue="region", corner=True)
plt.savefig("./plot_06_pairplot.png", dpi=100, bbox_inches="tight")
plt.close()

print("Все графики сохранены.")
