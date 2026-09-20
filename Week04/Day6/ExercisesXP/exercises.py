# Exercise 1
import pandas as pd

df = pd.read_csv("train.csv")

print(df.head())

before = len(df)

duplicates = df.duplicated().sum()
print(f"Duplicated rows found: {duplicates}")

df_cleaned = df.drop_duplicates()

after = len(df_cleaned)

print(f"Rows before: {before}")
print(f"Rows after: {after}")
print(f"Rows removed: {before - after}")

# Exercise 2

print(df.head())

print(df.isnull().sum()[df.isnull().sum() > 0])

df['Age'] = df['Age'].fillna(df['Age'].median())

df.drop(columns=['Cabin'], inplace=True)


from sklearn.impute import SimpleImputer
import numpy as np

imputer = SimpleImputer(strategy='median')
df[['Age', 'Fare']] = imputer.fit_transform(df[['Age', 'Fare']])

cat_imputer = SimpleImputer(strategy='most_frequent')
df[['Embarked']] = cat_imputer.fit_transform(df[['Embarked']])

# Exercise 3

print(df.columns)
print(df[['SibSp', 'Parch']].head())

df["FamilySize"] = df['SibSp'] + df['Parch']

print(df[['SibSp', 'Parch', 'FamilySize']].head())

print(df['Name'].head())

df['Title'] = df['Name'].str.extract(r'([A-Za-z]+)\.')
print(df['Title'].value_counts())

title_counts = df['Title'].value_counts()
rare_titles = title_counts[title_counts < 8].index
print(rare_titles)

df['Title'] = df['Title'].replace(rare_titles,'Rare')
print(df['Title'].value_counts())
print(df.dtypes)

df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
print(df['Sex'].value_counts())

df = pd.get_dummies(df, columns=[ 'Embarked', 'Title'])
print(df.columns)

# Exercise 4

import matplotlib.pyplot as plt

df['Fare'].plot(kind='box')
plt.show()

df['Age'].plot(kind='box')
plt.show()

Q1 = df['Fare'].quantile(0.25)
Q3 = df['Fare'].quantile(0.75)
IQR = Q3 - Q1

print(f"Q1: {Q1}")
print(f"Q3: {Q3}")
print(f"IQR: {IQR}")

upper = Q3 + (1.5 * IQR)
lower = Q1 - (1.5 * IQR)

print(f"Upper limit: {upper}")
print(f"Lower limit: {lower}")

print((df['Fare'] > upper).sum())

print("Before:", df['Fare'].max())

cap = df['Fare'].quantile(0.98)
df['Fare'] = df['Fare'].clip(upper=cap)
print("After:", df['Fare'].max())

import numpy as np

df['Age_log'] = np.log1p(df['Age'])
print(df[['Age', 'Age_log']].head(10))

fig, axes = plt.subplots(1, 2)
df['Age'].plot(kind='box', ax=axes[0], title='Age Before')
df['Age_log'].plot(kind='box', ax=axes[1], title='Age After')
plt.show()

df = df[df['Age'] <= 65]

print("Rows before:", 891)
print("Rows after:", len(df))

# Exercise 5

from sklearn.preprocessing import StandardScaler, MinMaxScaler

age_scaler = StandardScaler()
fare_scaler = MinMaxScaler()

df['Age'] = age_scaler.fit_transform(df[['Age']])
df['Fare'] = fare_scaler.fit_transform(df[['Fare']])

print(df[['Age', 'Fare']].head())
print(df['Fare'].min(), df['Fare'].max())

# Exercise 6

df = df.drop(columns=['Name', 'Ticket'])
print(df.select_dtypes(include=['object', 'string']).columns)
print(df.head())

# Exercise 7

import pandas as pd

df = pd.read_csv('train.csv')

bins = [0, 12, 18, 60, 100]
labels = ['child', 'teen', 'adult', 'senior']

df['age_group'] = pd.cut(df['Age'], bins=bins, labels=labels)

df = pd.get_dummies(df, columns=['age_group'])

print(df.head())
