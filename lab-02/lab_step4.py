import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# ── 1. Формируем датасет для кластеризации ────────────────────────────────────
# Берём два числовых признака: продолжительность образования и рабочие часы.
# Гипотеза: женщины в среднем учатся меньше и работают меньше часов,
# поэтому алгоритм должен суметь разделить выборку по полу.
print("--- Средние значения по полу ---")
print(df.groupby("sex")[["education-num", "hoursperweek"]].mean())

# Выделяем признаки в отдельный датасет и удаляем строки с пропусками,
# если они есть (dropna не влияет здесь, но это хорошая привычка).
df_clust = df[["education-num", "hoursperweek", "sex"]].dropna().copy()

# ── 2. Кластеризация методом KMeans ───────────────────────────────────────────
# n_clusters=2 — ищем два кластера (предполагаем два пола).
# random_state фиксирует начальные центроиды: результат воспроизводим.
model = KMeans(n_clusters=2, random_state=42, n_init=10)
model.fit(df_clust[["education-num", "hoursperweek"]])

# Сохраняем метки кластеров в новый столбец 'label'.
df_clust["label"] = model.labels_
print("\n--- Первые строки с меткой кластера ---")
print(df_clust.head(10))

# ── 3. Сравнение реального и предсказанного разбиения ────────────────────────
# Строим две точечные диаграммы рядом: одну по реальному полу, другую по label.
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.scatterplot(
    data=df_clust, x="hoursperweek", y="education-num", hue="sex", ax=axes[0], alpha=0.4
)
axes[0].set_title("Реальный пол")

sns.scatterplot(
    data=df_clust,
    x="hoursperweek",
    y="education-num",
    hue="label",
    ax=axes[1],
    alpha=0.4,
)
axes[1].set_title("Кластеры KMeans")

plt.savefig("plot_10_clustering.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 4. Количественная оценка точности (ручной подсчёт, как в учебнике) ────────
# Определяем, какая метка (0 или 1) соответствует мужчинам.
# Берём ту метку, которая чаще встречается у мужчин.
male_label = df_clust[df_clust["sex"] == "Male"]["label"].mode()[0]
female_label = 1 - male_label  # вторая метка — для женщин

total_male = (df_clust["sex"] == "Male").sum()
total_female = (df_clust["sex"] == "Female").sum()

# Мужчины, предсказанные верно (их метка совпадает с male_label).
correct_male = ((df_clust["sex"] == "Male") & (df_clust["label"] == male_label)).sum()
# Мужчины, предсказанные неверно.
wrong_male = ((df_clust["sex"] == "Male") & (df_clust["label"] == female_label)).sum()

# Женщины, предсказанные верно.
correct_female = (
    (df_clust["sex"] == "Female") & (df_clust["label"] == female_label)
).sum()
# Женщины, предсказанные неверно.
wrong_female = ((df_clust["sex"] == "Female") & (df_clust["label"] == male_label)).sum()

print(f"\nВсего мужчин: {total_male}")
print(f"  Верно предсказано: {correct_male}")
print(f"  Ошибочно (как женщины): {wrong_male}")

print(f"\nВсего женщин: {total_female}")
print(f"  Верно предсказано: {correct_female}")
print(f"  Ошибочно (как мужчины): {wrong_female}")

total_correct = correct_male + correct_female
print(f"\nВсего верных предсказаний: {total_correct} из {len(df_clust)}")
print(f"Точность: {total_correct / len(df_clust) * 100:.1f}%")
