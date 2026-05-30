import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("../../moscow_housing_study.csv", delimiter=",").dropna()

X = df[["full_area", "metro_distance_km", "price_rub"]].values
y = df["price_segment"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

clf = SGDClassifier(random_state=42, max_iter=1000)
clf.fit(X_train_s, y_train)

y_pred = clf.predict(X_test_s)
print(f"Точность SGDClassifier: {accuracy_score(y_test, y_pred):.2%}")
print("Матрица ошибок:")
print(confusion_matrix(y_test, y_pred))
