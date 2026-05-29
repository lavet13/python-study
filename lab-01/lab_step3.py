import pandas as pd

df = pd.read_csv("learn_dataset.csv", delimiter=",")

# sort_values() сортирует датасет по одному или нескольким столбцам.
# Передаём by и ascending как списки — это устраняет предупреждение
# статического анализатора и делает код единообразным.
# ascending=[False] — убывающий порядок (от большего к меньшему)
# ascending=[True]  — возрастающий порядок (от меньшего к большему)

# 1. Сортировка по одному признаку — убывающая.
sorted_desc = df[["age", "education", "education-num"]].sort_values(
    by=["education-num"], ascending=[False]
)
print("--- Сортировка по education-num (убывающая) ---")
print(sorted_desc.head())

# 2. Сортировка по одному признаку — возрастающая.
sorted_asc = df[["age", "education", "education-num"]].sort_values(
    by=["education-num"], ascending=[True]
)
print("\n--- Сортировка по education-num (возрастающая) ---")
print(sorted_asc.head())

# 3. Сортировка по двум признакам одновременно.
# Порядок в by= и ascending= совпадает позиционно:
# первый элемент ascending применяется к первому ключу, и т.д.
sorted_multi = df[["age", "education", "education-num"]].sort_values(
    by=["age", "education-num"], ascending=[False, True]
)
print("\n--- Сортировка по возрасту (убыв.) и education-num (возр.) ---")
print(sorted_multi.head())

# 4. iloc[] — выбор строк и столбцов по целочисленному порядковому номеру.
# iloc[0]      — первая строка (нумерация с нуля!)
# iloc[2]      — третья строка (индекс 2 = третье место)
# iloc[2, 0]   — третья строка, первый столбец (только одно значение)
oldest = df.sort_values(by=["age"], ascending=[False]).iloc[0]
print("\n--- Человек с максимальным возрастом ---")
print(oldest)

third_oldest = df.sort_values(by=["age"], ascending=[False]).iloc[2]
print("\n--- Человек на третьем месте по возрасту ---")
print(third_oldest)

third_age_value = df.sort_values(by=["age"], ascending=[False]).iloc[2, 0]
print(f"\n--- Только значение возраста (третье место): {third_age_value} ---")
