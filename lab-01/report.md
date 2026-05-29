**Цель работы:** Изучение основных возможностей библиотеки Pandas для загрузки, первичного осмотра, фильтрации, сортировки, добавления новых признаков, корреляционного анализа и группировки табличных данных.

**Задание:**

1. Загрузить датасет `learn_dataset.csv` и провести первичный анализ структуры данных.
2. Изучить типы признаков, вычислить описательные статистики.
3. Выполнить операции фильтрации и селекции строк с использованием логических выражений.
4. Отсортировать данные по одному и нескольким признакам; применить метод `iloc`.
5. Рассчитать новый признак — отношение капитального прироста к потерям.
6. Проанализировать корреляцию между признаками.
7. Выполнить группировку и агрегацию данных.

**Ход выполнения:**

### 1. Загрузка и первичный осмотр данных

Для загрузки данных использована функция `pd.read_csv()` библиотеки
Pandas с указанием разделителя запятой.

```python
df = pd.read_csv("learn_dataset.csv", delimiter=",")
df.info()
print(df.shape)
print(df.head())
```

```
<class 'pandas.DataFrame'>
RangeIndex: 48842 entries, 0 to 48841
Data columns (total 15 columns):
 #   Column          Non-Null Count  Dtype
---  ------          --------------  -----
 0   age             48842 non-null  int64
 1   workclass       48842 non-null  str
 2   fnlwgt          48842 non-null  int64
 3   education       48842 non-null  str
 4   education-num   48842 non-null  int64
 5   marital-status  48842 non-null  str
 6   occupation      48842 non-null  str
 7   relationship    48842 non-null  str
 8   race            48842 non-null  str
 9   sex             48842 non-null  str
 10  capitalgain     48842 non-null  int64
 11  capitalloss     48842 non-null  int64
 12  hoursperweek    48842 non-null  int64
 13  native-country  48842 non-null  str
 14  class           48842 non-null  str
dtypes: int64(6), str(9)
memory usage: 5.6 MB

Размерность датасета: (48842, 15)

   age         workclass  fnlwgt  education  education-num  ...  class
0    2         State-gov   77516  Bachelors             13  ...  <=50K
1    3  Self-emp-not-inc   83311  Bachelors             13  ...  <=50K
2    2           Private  215646    HS-grad              9  ...  <=50K
3    3           Private  234721       11th              7  ...  <=50K
4    1           Private  338409  Bachelors             13  ...  <=50K
```

Датасет содержит **48 842 строки** и **15 столбцов**.
Типы данных: числовые (`int64`) — `age`, `fnlwgt`, `education-num`,
`capitalgain`, `capitalloss`, `hoursperweek`; категориальные (`str`) —
`workclass`, `education`, `marital-status`, `occupation`, `relationship`,
`race`, `sex`, `native-country`, `class`.

Все столбцы содержат 48 842 непустых значения — явных пропусков нет.
Однако визуальный осмотр выявил значение `?` в столбцах `workclass`,
`occupation` и `native-country` — вероятно, так закодированы
отсутствующие данные. Это потребует обработки в Lab 2.
Целевой признак `class` принимает два значения: `<=50K` и `>50K`.

### 2. Описательные статистики

```python
print(df.describe())
print(df.describe(include='str'))
```

```
                age        fnlwgt  education-num   capitalgain  hoursperweek
count  48842.000000  4.884200e+04   48842.000000  48842.000000  48842.000000
mean       1.771078  1.896641e+05      10.078089      0.200319      1.950698
std        1.295378  1.056040e+05       2.570973      0.746182      0.897038
min        0.000000  1.228500e+04       1.000000      0.000000      0.000000
25%        1.000000  1.175505e+05       9.000000      0.000000      2.000000
50%        2.000000  1.781445e+05      10.000000      0.000000      2.000000
75%        3.000000  2.376420e+05      12.000000      0.000000      2.000000
max        4.000000  1.490400e+06      16.000000      4.000000      4.000000

       workclass education      marital-status  ...    sex  class
count      48842     48842               48842  ...  48842  48842
unique         9        16                   7  ...      2      2
top      Private   HS-grad  Married-civ-spouse  ...   Male  <=50K
freq       33906     15784               22379  ...  32650  37155
```

Признаки `age` и `hoursperweek` закодированы в диапазоны 0–4, а не
хранятся в исходном виде. Признаки `capitalgain` и `capitalloss`
сильно скошены вправо: медиана и 75-й перцентиль равны 0.
Целевой признак `class` несбалансирован: `<=50K` — 37 155 записей,
`>50K` — 11 687 (≈76% / 24%).

### 3. Фильтрация и селекция данных

```python
high_income = df[df['class'] == '>50K']
high_income_male = df[(df['class'] == '>50K') & (df['sex'] == 'Male')]
older_subset = df.loc[df['age'] > 2, ['age', 'education', 'class']]
```

```
Записей с высоким доходом: 11687
    age         workclass  fnlwgt     education  ...  class
7     3  Self-emp-not-inc  209642       HS-grad  ...   >50K
8     1           Private   45781       Masters  ...   >50K
9     2           Private  159449     Bachelors  ...   >50K

Мужчин с высоким доходом: 9918
    age         workclass  fnlwgt     education  ...  class
7     3  Self-emp-not-inc  209642       HS-grad  ...   >50K
9     2           Private  159449     Bachelors  ...   >50K

Записей с age > 2: 14544
    age  education  class
1     3  Bachelors  <=50K
3     3       11th  <=50K
6     3        9th  <=50K
```

Из 11 687 записей с доходом `>50K` мужчин — 9 918 (≈84,9%).
При двойной фильтрации условия заключаются в скобки и соединяются
оператором `&`. Метод `df.loc[условие, столбцы]` позволяет одновременно
фильтровать строки и выбирать нужные столбцы.

### 4. Сортировка и метод iloc

```python
sorted_desc = df[["age", "education", "education-num"]].sort_values(
    by=["education-num"], ascending=[False]
)
sorted_multi = df[["age", "education", "education-num"]].sort_values(
    by=["age", "education-num"], ascending=[False, True]
)
oldest = df.sort_values(by=["age"], ascending=[False]).iloc[0]
third_oldest = df.sort_values(by=["age"], ascending=[False]).iloc[2]
```

```
--- Сортировка по education-num (убывающая) ---
       age  education  education-num
41215    2  Doctorate             16
41093    4  Doctorate             16
24891    3  Doctorate             16

--- Сортировка по education-num (возрастающая) ---
       age  education  education-num
6433     1  Preschool              1
48525    4  Preschool              1
32035    2  Preschool              1

--- Человек с максимальным возрастом ---
age                                4
workclass               Self-emp-inc
education                  Bachelors
occupation           Exec-managerial
sex                             Male
class                          <=50K
Name: 14559, dtype: object

--- Человек на третьем месте по возрасту ---
age                           4
workclass             State-gov
education               HS-grad
occupation         Adm-clerical
sex                      Female
class                     <=50K
Name: 14567, dtype: object

--- Только значение возраста (третье место): 4 ---
```

Метод `sort_values()` принимает `by` и `ascending` как списки —
это обеспечивает единообразный синтаксис для одно- и многоключевой
сортировки. `iloc[0]` — первая строка после сортировки (нумерация
с нуля), `iloc[2, 0]` — значение из первого столбца третьей строки.

### 5. Добавление нового признака

```python
df["capital_ratio"] = df["capitalgain"] / (df["capitalloss"] + 1)
```

```
--- Первые 5 строк с новым признаком capital_ratio ---
   capitalgain  capitalloss  capital_ratio
0            1            0            1.0
1            0            0            0.0
2            0            0            0.0
3            0            0            0.0
4            0            0            0.0
```

`+1` в знаменателе — защита от деления на ноль: у большинства людей
`capitalloss = 0`, деление на ноль дало бы `inf`. Новый столбец
вычисляется векторизованно — Pandas применяет операцию ко всему
столбцу сразу, без явного цикла.

### 6. Корреляционный анализ

```python
corr_matrix = df.corr(numeric_only=True)
corr_gain_ratio = corr_matrix.loc["capitalgain", "capital_ratio"]
corr_hours_gain = corr_matrix.loc["hoursperweek", "capitalgain"]
corr_edu_hours  = corr_matrix.loc["education-num", "hoursperweek"]
```

```
                    age    fnlwgt  education-num  capitalgain  hoursperweek  capital_ratio
age            1.000000 -0.076674       0.034859     0.124929      0.115442       0.124929
fnlwgt        -0.076674  1.000000      -0.038761    -0.004681     -0.008893      -0.004681
education-num  0.034859 -0.038761       1.000000     0.160389      0.146786       0.160389
capitalgain    0.124929 -0.004681       0.160389     1.000000      0.099180       1.000000
hoursperweek   0.115442 -0.008893       0.146786     0.099180      1.000000       0.099180
capital_ratio  0.124929 -0.004681       0.160389     1.000000     -0.055408       1.000000

Корреляция между capitalgain и capital_ratio: 1.000
Корреляция между hoursperweek и capitalgain: 0.099
Корреляция между education-num и hoursperweek: 0.147
```

`capital_ratio` коррелирует с `capitalgain` идеально (1.000) —
у большинства строк `capitalloss = 0`, поэтому знаменатель формулы
константен и новый признак является точным линейным преобразованием
`capitalgain`. Связь `hoursperweek` и `capitalgain` (0.099) и
`education-num` и `hoursperweek` (0.147) слабая.

### 7. Группировка и агрегация

```python
group_race = df.groupby("race")[["education-num", "hoursperweek"]].mean()
group_sex_race = df.groupby(["sex", "race"])[
    ["education-num", "hoursperweek"]
].mean()
```

```
--- Среднее по расе ---
                    education-num  hoursperweek
race
Amer-Indian-Eskimo       9.387234      1.938298
Asian-Pac-Islander      10.998683      1.912442
Black                    9.491142      1.821772
Other                    8.839901      1.834975
White                   10.130262      1.967818

--- Среднее по полу и расе ---
                           education-num  hoursperweek
sex    race
Female Amer-Indian-Eskimo       9.686486      1.691892
       Asian-Pac-Islander      10.497099      1.740812
       Black                    9.591854      1.698440
Male   Amer-Indian-Eskimo       9.192982      2.098246
       Asian-Pac-Islander      11.257485      2.000998
       White                   10.133461      2.119158
```

`groupby()` разбивает датафрейм на группы по уникальным значениям
признака. При двойной группировке результат имеет двухуровневый
индекс (MultiIndex). Мужчины всех расовых групп работают больше часов,
чем женщины. Мужчины азиатского происхождения имеют наибольшее
среднее `education-num` (11.26) среди всех групп.

**Выводы:**

В ходе лабораторной работы освоены базовые операции с табличными
данными средствами библиотеки Pandas. Датасет содержит 48 842 записи
и 15 признаков смешанного типа. Целевой признак `class` несбалансирован
(≈76% / 24%); среди лиц с высоким доходом выявлено гендерное
неравенство (≈85% мужчин). Добавление расчётного признака
`capital_ratio` и корреляционный анализ подтвердили слабую линейную
связь между числовыми признаками (max r = 0.160). Группировка
по расовым и гендерным признакам показала устойчивое различие в
рабочих часах между мужчинами и женщинами во всех расовых группах.
