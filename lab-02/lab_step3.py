import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# Работаем только с ненулевыми значениями capitalgain —
# нули означают отсутствие инвестиций, а не аномалии.
df_fem = df[(df["sex"] == "Female") & (df["capitalgain"] > 0)].copy()
print(f"Женщин с ненулевым capitalgain: {len(df_fem)}")

# ── 1. Диаграмма «ящик с усами» (boxplot) ────────────────────────────────────
# Прямоугольник («ящик») охватывает 50% значений: от 25-й до 75-й процентили.
# Линия внутри ящика — медиана.
# «Усы» — допустимый разброс (обычно 1.5 * IQR за пределами ящика).
# Точки за усами — аномалии (выбросы).
sns.boxplot(data=df_fem, y="capitalgain")
plt.title("Ящик с усами: capitalgain (женщины)")
plt.savefig("plot_07_boxplot_before.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 2. Способ 1: правило трёх сигм (mean ± 3*std) ────────────────────────────
# Если m — среднее, s — среднеквадратичное отклонение, то значения
# за пределами [m - 3s; m + 3s] считаются аномальными.
m = df_fem["capitalgain"].mean()
s = df_fem["capitalgain"].std()
left_1  = m - 3 * s
right_1 = m + 3 * s
print(f"\nСпособ 1 — допустимый диапазон: [{left_1:.1f}; {right_1:.1f}]")

df_clean1 = df_fem[(df_fem["capitalgain"] >= left_1) & (df_fem["capitalgain"] <= right_1)]
print(f"Осталось строк после фильтрации: {len(df_clean1)}")

sns.boxplot(data=df_clean1, y="capitalgain")
plt.title("После удаления по правилу 3σ")
plt.savefig("plot_08_boxplot_3sigma.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 3. Способ 2: метод межквартильного размаха (IQR) ─────────────────────────
# a — 25-я процентиль (квантиль 0.25), b — 75-я процентиль (квантиль 0.75).
# Допустимый диапазон: [a - 1.5*(b-a); b + 1.5*(b-a)].
# Этот метод устойчивее к несимметричным распределениям, чем правило 3σ.
a = df_fem["capitalgain"].quantile(0.25)
b = df_fem["capitalgain"].quantile(0.75)
left_2  = a - 1.5 * (b - a)
right_2 = b + 1.5 * (b - a)
print(f"\nСпособ 2 — 25-я процентиль: {a:.1f}, 75-я процентиль: {b:.1f}")
print(f"Допустимый диапазон: [{left_2:.1f}; {right_2:.1f}]")

df_clean2 = df_fem[(df_fem["capitalgain"] >= left_2) & (df_fem["capitalgain"] <= right_2)]
print(f"Осталось строк после фильтрации: {len(df_clean2)}")

sns.boxplot(data=df_clean2, y="capitalgain")
plt.title("После удаления по методу IQR")
plt.savefig("plot_09_boxplot_iqr.png", dpi=100, bbox_inches="tight")
plt.close()

print("\nГрафики сохранены.")
