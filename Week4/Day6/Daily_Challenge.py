import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv('datascience_salaries.csv')

result = df.groupby('experience_level')['salary'].agg(['mean', 'median'])
print(result)

df['salary_normalized'] = (df['salary'] - df['salary'].min()) / (df['salary'].max() - df['salary'].min())

df = pd.get_dummies(df, columns=['job_title', 'job_type', 'experience_level', 'location', 'salary_currency'])

numeric_df = df.select_dtypes(include=[float, bool, int])

scaler = StandardScaler()
scaled_df = scaler.fit_transform(numeric_df)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_df)
print(pca_result)
