import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# ── 1. Гистограмма распределения числового признака ──────────────────────────
# displot() строит гистограмму и/или кривую плотности распределения.
# По оси X — значение признака, по оси Y — количество записей с этим значением.
sns.displot(df["education-num"])
plt.title("Распределение продолжительности образования")
plt.savefig("./plot_01_displot_education.png", dpi=100, bbox_inches="tight")
plt.close()

# Добавим параметр kind='kde' — вместо столбцов получим кривую плотности.
# KDE (Kernel Density Estimate) сглаживает гистограмму в непрерывную кривую.
sns.displot(df["education-num"], kind="kde")
plt.title("Функция плотности распределения education-num")
plt.savefig("./plot_02_kde_education.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 2. Точечная диаграмма (scatterplot) ───────────────────────────────────────
# Фильтруем строки с нулевым capitalgain — эти люди не инвестировали,
# поэтому включать их в анализ зависимости дохода от часов работы
# не имеет смысла: они искажают облако точек.
df_nonzero = df[df["capitalgain"] > 0]

# hue='sex' окрашивает точки по значению признака «пол»:
# мужчины и женщины отображаются разными цветами.
sns.scatterplot(data=df_nonzero, x="hoursperweek", y="capitalgain", hue="sex")
plt.title("Зависимость capitalgain от hoursperweek")
plt.savefig("./plot_03_scatter_hours_gain.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 3. Столбчатая диаграмма для категориального признака (countplot) ─────────
# countplot() строит столбцы по количеству строк для каждого значения признака.
sns.countplot(data=df, x="sex")
plt.title("Распределение по полу")
plt.savefig("./plot_04_countplot_sex.png", dpi=100, bbox_inches="tight")
plt.close()

# Параметр hue разбивает каждый столбец по дополнительному признаку.
# Так можно увидеть распределение семейного статуса внутри каждой группы.
sns.countplot(data=df, x="sex", hue="marital-status")
plt.title("Распределение по полу и семейному статусу")
plt.xticks(rotation=15)
plt.savefig("./plot_05_countplot_sex_marital.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 4. Парные точечные диаграммы (pairplot) ───────────────────────────────────
# pairplot() строит матрицу диаграмм: на пересечении каждой пары признаков —
# scatterplot. На главной диагонали — распределение признака (KDE или hist).
# Матрица симметрична: верхний треугольник зеркален нижнему.
df_pair = df[["education-num", "capitalgain", "hoursperweek", "sex"]]
sns.pairplot(df_pair, hue="sex")
plt.savefig("./plot_06_pairplot.png", dpi=100, bbox_inches="tight")
plt.close()

print("Все графики сохранены.")
