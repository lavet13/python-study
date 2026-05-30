# ВВЕДЕНИЕ

## Цель работы

Целью данной курсовой работы является демонстрация полного цикла
анализа данных и машинного обучения на реальном датасете рынка
недвижимости Москвы: от загрузки и первичного осмотра данных до
построения и сравнения моделей машинного обучения.

## Описание датасета

Для анализа использован синтетический датасет `moscow_housing_study.csv`,
содержащий 2 000 записей о квартирах московского региона за период
с января 2024 по май 2026 года. Датасет включает 13 признаков:

- **Числовые:** `full_area`, `living_area`, `kitchen_area`, `floor`,
  `num_rooms`, `metro_distance_km`, `price_rub`
- **Категориальные:** `region`, `renovation`, `building_type`,
  `price_segment`
- **Временной:** `timestamp`

Целевые признаки: `price_rub` (задача регрессии — предсказание цены)
и `price_segment` (задача классификации — Budget / Standard / Premium).

## Обоснование выбора датасета

Датасет рынка недвижимости охватывает все темы курса: числовые и
категориальные признаки, пропущенные значения, аномалии, временную
компоненту, чёткий целевой признак для регрессии и классификации,
богатую корреляционную структуру. Регион, тип ремонта, расстояние
до метро и площадь формируют многофакторную задачу, демонстрирующую
преимущества ансамблевых методов.

---

# 2. ПРЕДВАРИТЕЛЬНЫЙ АНАЛИЗ ДАННЫХ

## 2.1 Загрузка и первичный осмотр данных

```python
df = pd.read_csv("moscow_housing_study.csv", delimiter=",")
df.info()
print(df.shape)
print(df.head())
```

```
<class 'pandas.DataFrame'>
RangeIndex: 2000 entries, 0 to 1999
Data columns (total 13 columns):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   id                 2000 non-null   int64
 1   timestamp          2000 non-null   str
 2   full_area          2000 non-null   float64
 3   living_area        1786 non-null   float64
 4   kitchen_area       1848 non-null   float64
 5   floor              2000 non-null   int64
 6   num_rooms          2000 non-null   int64
 7   metro_distance_km  1906 non-null   float64
 8   region             2000 non-null   str
 9   renovation         1506 non-null   str
10   building_type      2000 non-null   str
11   price_rub          2000 non-null   float64
12   price_segment      2000 non-null   str
dtypes: float64(5), int64(3), str(5)
memory usage: 203.3 KB

Размерность датасета: (2000, 13)

   id            timestamp  full_area  living_area  ...  price_rub price_segment
0   1  2024-11-22 14:01:09       75.3         41.1  ...  14380000.0      Standard
1   2  2025-04-16 20:19:58       61.7          NaN  ...  16910000.0       Premium
2   3  2024-06-27 05:29:49       79.0         42.4  ...  14040000.0      Standard
3   4  2024-04-11 14:59:23      105.9         60.9  ...   9320000.0        Budget
4   5  2024-03-23 03:53:05       60.0         26.9  ...   9830000.0        Budget
```

Датасет содержит **2 000 строк** и **13 признаков**. Уже из `info()`
видны пропуски: `living_area` — 214, `kitchen_area` — 152,
`metro_distance_km` — 94, `renovation` — 494. Целевой признак
`price_segment` содержит три класса: Budget, Standard, Premium.

## 2.2 Описательные статистики

```python
print(df.describe())
print(df.describe(include='object'))
```

```
         full_area  living_area  kitchen_area        floor  metro_distance_km     price_rub
count  2000.000000  1786.000000   1848.000000  2000.000000        1906.000000  2.000000e+03
mean     69.410500    41.865398     10.292587    13.242500           2.512881  1.504903e+07
std      22.586468    15.200216      4.056187     7.158094           2.414435  8.872781e+06
min      28.500000    14.300000      0.000000     1.000000           0.100000  3.130000e+06
25%      53.500000    31.225000      7.500000     7.000000           0.749750  9.707500e+06
50%      65.300000    38.950000      9.600000    14.000000           1.822000  1.349500e+07
75%      79.925000    49.400000     12.225000    19.000000           3.493000  1.834750e+07
max     245.700000   147.400000     32.500000    25.000000          20.038000  1.825200e+08

        timestamp  region renovation building_type price_segment
count        2000    2000       1506          2000          2000
unique       2000       3          3             3             3
top           ...  Moscow   Cosmetic         Panel        Budget
freq            1    1111        899           814           669
```

Средняя цена квартиры — **15,05 млн руб.**, медиана — 13,50 млн.
Разрыв и максимум 182,5 млн руб. указывают на правостороннюю
асимметрию и наличие выбросов. Большинство квартир — в Москве
(1 111 из 2 000), преобладающий ремонт — Cosmetic (899).

## 2.3 Фильтрация и селекция строк

```python
premium = df[df["price_segment"] == "Premium"]
large_moscow = df[(df["full_area"] > 80) & (df["region"] == "Moscow")]
subset = df.loc[df["metro_distance_km"] < 1, ["full_area", "price_rub", "price_segment"]]
```

```
Квартир премиум-класса: 668
Больших квартир в Москве (>80 м²): 285
Квартир в пешей доступности от метро (<1 км): 619
    full_area   price_rub price_segment
4        60.0   9830000.0        Budget
8        55.9   7510000.0        Budget
9        76.4  11600000.0      Standard
```

Квартиры у метро (619 записей) охватывают все три сегмента —
расстояние до метро влияет на цену, но не является единственным
фактором.

## 2.4 Сортировка и iloc

```python
sorted_price = df[["full_area", "price_rub", "region"]].sort_values(
    by="price_rub", ascending=False
)
most_expensive = df.sort_values(by="price_rub", ascending=False).iloc[0]
```

```
--- Самые дорогие квартиры ---
      full_area    price_rub      region
1333      104.7  182520000.0  New_Moscow
439        63.3  175110000.0      Moscow
209       245.7   78010000.0      Moscow

--- Самые маленькие квартиры ---
      full_area  price_rub         region
262        28.5  3130000.0  Moscow_Oblast

--- Самая дорогая квартира ---
region              New_Moscow
renovation                Euro
building_type           Monolith
price_rub            182520000.0
price_segment            Premium
Name: 1333, dtype: object
```

Самая дорогая квартира (182,5 млн руб.) находится в New_Moscow,
площадь 104,7 м² — нестандартный результат, указывающий на
искусственный выброс, заданный при генерации датасета.

## 2.5 Добавление нового признака и корреляционный анализ

```python
df["living_ratio"] = df["living_area"] / df["full_area"]
corr_matrix = df.corr(numeric_only=True)
print(corr_matrix[["price_rub"]].sort_values("price_rub", ascending=False))
```

```
--- Первые 5 строк с living_ratio ---
   full_area  living_area  living_ratio
0       75.3         41.1      0.545817
1       61.7          NaN           NaN
2       79.0         42.4      0.536709

--- Матрица корреляций (с price_rub) ---
                   price_rub
price_rub           1.000000
full_area           0.548686
living_area         0.494679
kitchen_area        0.449637
num_rooms           0.424275
floor               0.071358
id                 -0.005579
living_ratio       -0.008016
metro_distance_km  -0.102334
```

Наиболее сильная корреляция с ценой — у `full_area` (r = 0.549).
`metro_distance_km` имеет слабую отрицательную корреляцию (r = −0.102):
чем ближе к метро, тем дороже квартира.

## 2.6 Группировка и агрегация

```python
print(df.groupby("region")["price_rub"].mean())
print(df.groupby("renovation")["price_rub"].mean())
```

```
--- Средняя цена по району ---
Moscow           17 902 440 руб.
Moscow_Oblast     9 956 263 руб.
New_Moscow       13 436 590 руб.

--- Средняя цена по типу ремонта ---
Cosmetic    14 332 860 руб.
Designer    20 158 760 руб.
Euro        17 288 340 руб.
```

Квартиры в Москве в среднем в 1,8 раза дороже, чем в Подмосковье.
Ремонт Designer увеличивает среднюю цену на 40% по сравнению с Cosmetic.

---

# 3. ВИЗУАЛИЗАЦИЯ И ОЧИСТКА ДАННЫХ

## 3.1 Визуализация распределений и зависимостей

```python
sns.displot(df["full_area"], bins=30)
```

![Распределение общей площади](lab-02/plot_01_displot_full_area.png)

![Функция плотности full_area](lab-02/plot_02_kde_full_area.png)

Распределение `full_area` правосторонне асимметрично: пик 55–70 м²,
длинный хвост до 245 м² отражает элитные квартиры.

```python
sns.scatterplot(data=df, x="full_area", y="price_rub", hue="region", alpha=0.6)
```

![Зависимость цены от площади](lab-02/plot_03_scatter_area_price.png)

Московские квартиры (синие) систематически дороже при той же площади,
чем квартиры в Подмосковье (оранжевые).

```python
sns.countplot(data=df, x="region")
sns.countplot(data=df, x="region", hue="renovation")
```

![Распределение квартир по районам](lab-02/plot_04_countplot_region.png)

![Распределение по району и ремонту](lab-02/plot_05_countplot_region_renovation.png)

Во всех районах преобладает ремонт Cosmetic; доля Designer-ремонта
пропорционально схожа во всех регионах.

```python
df_pair = df[["full_area", "living_area", "kitchen_area", "price_rub", "region"]]
sns.pairplot(df_pair, hue="region", corner=True)
```

![Матрица парных диаграмм](lab-02/plot_06_pairplot.png)

Матрица показывает чёткую линейную зависимость между `full_area`,
`living_area` и `kitchen_area`. Московские квартиры имеют более широкий
ценовой диапазон.

## 3.2 Обработка пропущенных значений

```python
print(df.isnull().sum())
df_dropped = df_with_na.dropna()
```

```
living_area          214
kitchen_area         152
metro_distance_km     94
renovation           494

После dropna(): осталось строк: 1175 из 2000
```

Удаление строк уничтожает 41,25% датасета — недопустимо. Применяется
заполнение медианой для числовых признаков:

```python
for col in ["living_area", "kitchen_area", "metro_distance_km"]:
    median_val = df_filled[col].median()
    df_filled[col] = df_filled[col].fillna(median_val)
```

```
  living_area: пропуски заполнены медианой (38.95)
  kitchen_area: пропуски заполнены медианой (9.60)
  metro_distance_km: пропуски заполнены медианой (1.82)
После заполнения: пропусков осталось: 494
```

Пропуски в `renovation` (494 записи) соответствуют квартирам без
указанного ремонта и обрабатываются отдельно при кодировании.

## 3.3 Выявление и устранение аномалий

```python
sns.boxplot(data=df_price, y="price_rub")
```

![Ящик с усами: price_rub до фильтрации](lab-02/plot_07_boxplot_before.png)

Отчётливо видны выбросы выше 50 млн руб., включая два экстремальных
значения (175 и 182 млн руб.).

```python
m, s = df_price["price_rub"].mean(), df_price["price_rub"].std()
left_1, right_1 = m - 3 * s, m + 3 * s
```

```
Способ 1 (3σ) — диапазон: [-11 569 313; 41 667 373]
Осталось после 3σ: 1986 строк (удалено 14)
```

![После удаления по правилу 3σ](lab-02/plot_08_boxplot_3sigma.png)

```python
Q1 = df_price["price_rub"].quantile(0.25)
Q3 = df_price["price_rub"].quantile(0.75)
left_2, right_2 = Q1 - 1.5*(Q3-Q1), Q3 + 1.5*(Q3-Q1)
```

```
Способ 2 (IQR) — диапазон: [-3 252 500; 31 307 500]
Осталось после IQR: 1938 строк (удалено 62)
```

![После удаления по методу IQR](lab-02/plot_09_boxplot_iqr.png)

IQR-метод строже (62 удалённых строки против 14), поскольку
распределение асимметрично. После IQR-фильтрации экстремальные
выбросы устранены.

## 3.4 Кластеризация

```python
features = ["full_area", "metro_distance_km", "price_rub"]
X_scaled = scaler.fit_transform(df_clust[features])
model = KMeans(n_clusters=3, random_state=42, n_init=10)
df_clust["cluster"] = model.fit_predict(X_scaled)
```

```
--- Размер кластеров ---
cluster 0:  1142 объекта
cluster 1:   422 объекта
cluster 2:   342 объекта
```

![Реальные районы и кластеры KMeans](lab-02/plot_10_clustering.png)

KMeans разделил объекты по ценовому уровню: кластер 0 — типичные
квартиры, кластер 1 и 2 — крупные или дорогие объекты. Районная
принадлежность не совпадает с кластерами — алгоритм разделяет
по цене и площади, а не по географии.

---

# 4. МАШИННОЕ ОБУЧЕНИЕ: РЕГРЕССИЯ И КЛАССИФИКАЦИЯ

## 4.1 Постановка задачи

Определены две задачи: **регрессия** (`price_rub`) и **классификация**
(`price_segment`). Для всех моделей: разбиение 80/20, `random_state=42`.

## 4.2 Линейная регрессия

```python
X_simple = df1[["full_area"]].values
y = df1["price_rub"].values
model = LinearRegression()
model.fit(X_train, y_train)
```

```
Уравнение: price_rub ≈ 215 484 * full_area + 36 205
MAE: 3 962 161 руб.
```

![Зависимость цены от площади](lab-03/plot_11_scatter_regression.png)

Коэффициент 215 484 руб./м² соответствует рыночной стоимости московского
жилья. MAE ≈ 3,96 млн руб. — модель ошибается на ≈26% от медианной цены.

## 4.3 Метод k ближайших соседей (kNN)

```python
X = df[["full_area", "metro_distance_km", "price_rub"]].values
y = df["price_segment"].values
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X_train_scaled, y_train)
```

```
Точность KNN (n=7): 90.64%
```

![Ошибки KNN (n=7)](lab-03/plot_12_knn_errors.png)

KNN достигает точности 90.64%. Редкие ошибки (оранжевые точки)
концентрируются в пограничных зонах между сегментами.

## 4.4 Линейный классификатор (SGDClassifier)

```python
clf = SGDClassifier(random_state=42, max_iter=1000)
clf.fit(X_train_s, y_train)
```

```
Точность SGDClassifier: 97.45%
Матрица ошибок:
[[65  0  1]
 [ 0 86  0]
 [ 0  5 78]]
```

SGDClassifier показал **97.45%** — лучший результат среди всех методов
классификации. Ценовые сегменты линейно разделяются в пространстве
признаков, что обеспечивает высокую точность линейного классификатора.

## 4.5 Решающие деревья

```python
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)
```

```
Точность (max_depth=5): 51.06%

Структура дерева (первые уровни):
|--- full_area <= 72.30
|   |--- full_area <= 54.85
|   |   |--- metro_distance_km <= 1.35
```

![Матрица парных диаграмм (признаки дерева)](lab-03/plot_13_pairplot_tree_features.png)

Дерево без `price_rub` в признаках (только `full_area`, `living_area`,
`metro_distance_km`, `floor`) показало 51.06%. Физические характеристики
сами по себе недостаточны для чёткого разделения сегментов.

---

# 5. ПРОДВИНУТЫЕ МЕТОДЫ МАШИННОГО ОБУЧЕНИЯ

## 5.1 Дерево регрессии

```python
tree_reg = DecisionTreeRegressor(random_state=42)          # глубина 26
tree_reg_limited = DecisionTreeRegressor(max_depth=8, random_state=42)
```

```
--- Без ограничения ---
Глубина: 26  |  MAE: 6 225 806 руб.

--- max_depth=8 ---
MAE: 5 044 218 руб.  (улучшение 19%)
```

Ограничение глубины снижает переобучение и улучшает MAE на 19%.
Тем не менее оба дерева уступают простой линейной регрессии — из-за
нестабильности на малых выборках с выбросами.

## 5.2 Ансамблевые методы. Вероятностные предсказания

```python
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
proba = rf.predict_proba(X_test)
```

```
Классы: ['Budget' 'Premium' 'Standard']

Первые 5 вероятностей:
[[0.22 0.40 0.38]
 [0.01 0.71 0.28]
 [0.04 0.60 0.36]
 [0.46 0.05 0.49]
 [0.08 0.56 0.36]]

--- Первые 8 строк с вероятностями ---
  real_segment  prob_Budget  prob_Standard  prob_Premium
0     Standard         0.22           0.40          0.38
1      Premium         0.01           0.71          0.28
3       Budget         0.46           0.05          0.49
```

`predict_proba()` возвращает вероятности принадлежности к каждому
классу. Строка 3 (`Budget`) иллюстрирует пограничный случай: 46%
на Budget, 49% на Standard — квартира находится на границе сегментов.

## 5.3 Кодирование категориальных признаков. Важность признаков

**LabelEncoder:**

```python
for col in ["region", "renovation", "building_type", "price_segment"]:
    df_encoded[col] = coder.fit_transform(df_encoded[col].astype(str))
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
```

```
--- Пример кодирования region ---
Moscow        →  0
Moscow_Oblast →  1

Точность предсказания ценового сегмента: 65.00%

--- Важность признаков ---
full_area            0.447891
metro_distance_km    0.229299
region               0.175919
floor                0.146891
```

`full_area` — доминирующий признак (44.8%). Расстояние до метро —
второй по важности (22.9%), район — третий (17.6%).

**One-Hot Encoding:**

```python
df_ohe = pd.get_dummies(df, columns=["region", "renovation", "building_type"],
                        drop_first=True)
tree = DecisionTreeClassifier(max_depth=6, random_state=42)
```

```
--- Новые столбцы после get_dummies ---
['region_Moscow_Oblast', 'region_New_Moscow', 'renovation_Designer',
 'renovation_Euro', 'building_type_Monolith']

Точность с One-Hot Encoding: 74.00%
Матрица ошибок:
[[104   1  28]
 [  5 102  24]
 [ 24  22  90]]
```

OHE улучшает точность с 65% до **74%** по сравнению с LabelEncoder,
устраняя ложный числовой порядок между категориями.

---

# 6. ЗАКЛЮЧЕНИЕ

## Сравнение методов

| Метод | Задача | Метрика | Результат |
|---|---|---|---|
| Линейная регрессия (full_area) | Регрессия цены | MAE | 3 962 161 руб. |
| Дерево регрессии (глубина 26) | Регрессия цены | MAE | 6 225 806 руб. |
| Дерево регрессии (max_depth=8) | Регрессия цены | MAE | 5 044 218 руб. |
| KNN (n=7) | Классификация сегмента | Accuracy | 90.64% |
| SGDClassifier | Классификация сегмента | Accuracy | 97.45% |
| Дерево (max_depth=5, без price_rub) | Классификация сегмента | Accuracy | 51.06% |
| Дерево (max_depth=6, OHE) | Классификация сегмента | Accuracy | 74.00% |

## Выводы

**Регрессия:** простая линейная модель по одному признаку (MAE 3,96 млн)
оказалась точнее дерева с четырьмя признаками — из-за нестабильности
деревьев на асимметричных данных с выбросами.

**Классификация:** SGDClassifier (97.45%) превзошёл все методы —
ценовые сегменты линейно разделяются в пространстве признаков при
наличии `price_rub`. Дерево без цены (51.06%) показало ограниченность
физических характеристик для сегментации.

**Кодирование:** OHE (+9 п.п. к точности) превосходит LabelEncoder
для номинальных признаков. Важность признаков: площадь (44.8%),
расстояние до метро (22.9%), район (17.6%).

## Практическая значимость

Разработанные модели позволяют оценить стоимость квартиры по площади
(MAE ≈ 4 млн руб.) и с высокой точностью определить ценовой сегмент
(97.45% при наличии цены, 74% без неё). Ключевые факторы
ценообразования: общая площадь, расстояние до метро и район.

## Список использованных источников

1. McKinney, W. Python for Data Analysis. O'Reilly Media, 2022.
2. Pedregosa, F. et al. Scikit-learn: Machine Learning in Python.
   JMLR, 12, 2825–2830, 2011.
3. Waskom, M. Seaborn: statistical data visualization.
   JOSS, 6(60), 3021, 2021.
4. Géron, A. Hands-On Machine Learning with Scikit-Learn, Keras,
   and TensorFlow. O'Reilly Media, 2022.
