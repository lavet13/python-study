import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("../learn_dataset.csv", delimiter=",")

# Фильтруем строки с нулевым capitalgain — эти люди не инвестировали,
# включать их в модель регрессии нет смысла (нулевая прибыль не зависит
# ни от каких признаков, она просто означает отсутствие инвестиций).
df1 = df[df["capitalgain"] > 0].copy()
print(f"Строк после фильтрации нулевой прибыли: {len(df1)}")

# ── 1. Визуализация зависимости ───────────────────────────────────────────────
sns.scatterplot(data=df1, x="hoursperweek", y="capitalgain")
plt.title("Зависимость capitalgain от hoursperweek")
plt.savefig("plot_11_scatter_regression.png", dpi=100, bbox_inches="tight")
plt.close()

# ── 2. Простая линейная регрессия (один признак) ──────────────────────────────
# Модель ищет коэффициенты k и b в уравнении: capitalgain = k * hoursperweek + b
#
# reshape(-1, 1) преобразует одномерный массив [x1, x2, ...] в двумерный
# [[x1], [x2], ...] — именно такой формат требует sklearn для признаков X.
# Для целевой переменной y одномерный массив допустим.
X_simple = df1["hoursperweek"].values.reshape(-1, 1)
y = df1["capitalgain"].values

# train_test_split делит данные на обучающую (80%) и тестовую (20%) выборки.
# random_state фиксирует разбиение для воспроизводимости.
X_train, X_test, y_train, y_test = train_test_split(
    X_simple, y, test_size=0.2, random_state=42
)

model_simple = LinearRegression()
model_simple.fit(X_train, y_train)

k = model_simple.coef_[0]
b = model_simple.intercept_
print(f"\n--- Простая регрессия ---")
print(f"Коэффициент k: {k:.4f}")
print(f"Свободный член b: {b:.4f}")
print(f"Уравнение: capitalgain = {k:.2f} * hoursperweek + {b:.2f}")

# Предсказание и оценка на тестовой выборке
y_pred_simple = model_simple.predict(X_test)
mae_simple = mean_absolute_error(y_test, y_pred_simple)
print(f"MAE на тестовой выборке: {mae_simple:.4f}")

# ── 3. Множественная регрессия (два признака) ─────────────────────────────────
# Теперь ищем: capitalgain = a * hoursperweek + b * education-num + c
# При нескольких признаках X уже является матрицей — reshape не нужен.
X_multi = df1[["hoursperweek", "education-num"]].values

X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(
    X_multi, y, test_size=0.2, random_state=42
)

model_multi = LinearRegression()
model_multi.fit(X_train_m, y_train_m)

a, b2 = model_multi.coef_
c = model_multi.intercept_
print(f"\n--- Множественная регрессия ---")
print(f"Коэффициенты: {model_multi.coef_}")
print(f"Свободный член: {c:.4f}")
print(
    f"Уравнение: capitalgain = {a:.2f}*hoursperweek + {b2:.2f}*education-num + {c:.2f}"
)

y_pred_multi = model_multi.predict(X_test_m)
mae_multi = mean_absolute_error(y_test_m, y_pred_multi)
print(f"MAE на тестовой выборке: {mae_multi:.4f}")

print(f"\nУлучшение MAE: {mae_simple - mae_multi:.4f}")
