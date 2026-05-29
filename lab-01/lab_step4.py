import pandas as pd

df = pd.read_csv("learn_dataset.csv", delimiter=",")

# ── 1. Добавление нового признака: отношение прироста капитала к потерям ──────
# Иллюстрирует тот же принцип, что и ИМТ в учебнике: вычисление нового
# признака на основе двух существующих через арифметическую операцию.
# +1 в знаменателе — защита от деления на ноль (у большинства людей
# capitalloss = 0, деление на ноль дало бы inf или ошибку).
df["capital_ratio"] = df["capitalgain"] / (df["capitalloss"] + 1)

print("--- Первые 5 строк с новым признаком capital_ratio ---")
print(df[["capitalgain", "capitalloss", "capital_ratio"]].head())

# ── 2. Корреляционная матрица ─────────────────────────────────────────────────
# corr() вычисляет коэффициенты корреляции Пирсона между всеми числовыми столбцами.
# Значение от -1 до 1:
#   близко к  1 → сильная прямая связь (оба растут вместе)
#   близко к -1 → сильная обратная связь (один растёт, другой падает)
#   близко к  0 → связь отсутствует
# На главной диагонали всегда 1.0 — признак коррелирует сам с собой.
corr_matrix = df.corr(numeric_only=True)
print("\n--- Матрица корреляций ---")
print(corr_matrix)

# Выборочное извлечение конкретных пар признаков из матрицы.
corr_gain_ratio = corr_matrix.loc["capitalgain", "capital_ratio"]
print(f"\nКорреляция между capitalgain и capital_ratio: {corr_gain_ratio:.3f}")

corr_hours_gain = corr_matrix.loc["hoursperweek", "capitalgain"]
print(f"Корреляция между hoursperweek и capitalgain: {corr_hours_gain:.3f}")

corr_edu_hours = corr_matrix.loc["education-num", "hoursperweek"]
print(f"Корреляция между education-num и hoursperweek: {corr_edu_hours:.3f}")

# ── 3. Группировка ───────────────────────────────────────────────────────────
# groupby(признак) разбивает датасет на группы по уникальным значениям признака.
# После группировки применяем агрегирующую функцию: mean(), min(), max() и т.д.

# Группировка по одному признаку: средние education-num и hoursperweek по расе.
group_race = df.groupby("race")[["education-num", "hoursperweek"]].mean()
print("\n--- Среднее education-num и hoursperweek по расе ---")
print(group_race)

# Группировка по двум признакам: сначала по полу, внутри — по расе.
# Результат имеет двухуровневый индекс (MultiIndex).
group_sex_race = df.groupby(["sex", "race"])[["education-num", "hoursperweek"]].mean()
print("\n--- Среднее education-num и hoursperweek по полу и расе ---")
print(group_sex_race)
