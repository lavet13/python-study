import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",")

# Работаем с ценами — они имеют выбросы
df_price = df.copy()

# Вычислим границу для отображения заранее — одинаковая для всех трёх графиков
display_max = df_price["price_rub"].quantile(0.98)  # показываем 98% данных


def plot_price_hist(data, title, filename, left, right, display_max):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(data["price_rub"] / 1e6, bins=60, color="steelblue", edgecolor="none")
    # Вертикальные линии — границы фильтрации
    ax.axvline(
        right / 1e6,
        color="red",
        linewidth=1.5,
        linestyle="--",
        label=f"Граница: {right / 1e6:.1f} млн",
    )
    ax.set_xlabel("price_rub (млн руб.)")
    ax.set_ylabel("Количество квартир")
    ax.set_xlim(0, display_max / 1e6)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=100, bbox_inches="tight")
    plt.close()


# ── 2. Правило трёх сигм ─────────────────────────────────────────────────────
m = df_price["price_rub"].mean()
s = df_price["price_rub"].std()
left_1 = m - 3 * s
right_1 = m + 3 * s

print(f"\nСпособ 1 (3σ) — диапазон: [{left_1:,.0f}; {right_1:,.0f}]")

# ── plot_07: до фильтрации ────────────────────────────────────────────────────
plot_price_hist(
    df_price,
    "Распределение цен (до фильтрации)",
    "plot_07_boxplot_before.png",
    left_1,
    right_1,
    display_max,
)

df_clean1 = df_price[
    (df_price["price_rub"] >= left_1) & (df_price["price_rub"] <= right_1)
]

# ── plot_08: после 3σ ─────────────────────────────────────────────────────────
plot_price_hist(
    df_clean1,
    "Распределение цен (после правила 3σ)",
    "plot_08_boxplot_3sigma.png",
    left_1,
    right_1,
    display_max,
)

# ── 3. Метод IQR ─────────────────────────────────────────────────────────────
Q1 = df_price["price_rub"].quantile(0.25)
Q3 = df_price["price_rub"].quantile(0.75)
IQR = Q3 - Q1
left_2 = Q1 - 1.5 * IQR
right_2 = Q3 + 1.5 * IQR

print(f"Способ 2 (IQR) — диапазон: [{left_2:,.0f}; {right_2:,.0f}]")

df_clean2 = df_price[
    (df_price["price_rub"] >= left_2) & (df_price["price_rub"] <= right_2)
]

# ── plot_09: после IQR ────────────────────────────────────────────────────────
plot_price_hist(
    df_clean2,
    "Распределение цен (после метода IQR)",
    "plot_09_boxplot_iqr.png",
    left_2,
    right_2,
    display_max,
)

print(f"\nОсталось после 3σ: {len(df_clean1)} строк")
print(f"Осталось после IQR: {len(df_clean2)} строк")
