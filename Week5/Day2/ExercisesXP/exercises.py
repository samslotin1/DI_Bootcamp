# Exercise 2

from scipy import stats
import numpy as np
data = [12, 15, 13, 12, 18, 20, 22, 21]

np.mean(data)
np.median(data)
np.var(data)
np.std(data)

print(np.mean(data))
print(np.median(data))
print(np.var(data))
print(np.std(data))

# Exercise 3

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

mean = 50
std = 10
x = np.linspace(20, 80, 100)

y = norm.pdf(x, mean, std)

plt.plot(x, y)
plt.show()

# Exercise 4

import numpy as np
from scipy import stats

data1 = np.random.normal(50, 10, 100)
data2 = np.random.normal(60, 10, 100)

result = stats.ttest_ind(data1, data2)
print(result)

# Exercise 5

import numpy as np
from scipy import stats

house_sizes = [50, 70, 80, 100, 120,]
house_prices =  [150000, 200000, 210000, 250000, 280000,]

slope, intercept, r_value, p_value, std_err = stats.linregress(house_sizes, house_prices)

print(slope)
print(intercept)

predicted_price = slope * 90 + intercept
print(predicted_price)

# Exercise 6

from scipy import stats

fertilizer_1 = [5, 6, 7, 6, 5]
fertilizer_2 = [7, 8, 7, 9, 8]
fertilizer_3 = [4, 5, 4, 3, 4]

result = stats.f_oneway(fertilizer_1, fertilizer_2, fertilizer_3)
print(result)

# Exercise 7

from scipy import stats

probability = stats.binom.pmf(5, 10, 0.5)
print(probability)

# Exercise 8

import pandas as pd
from scipy import stats

income = [35000, 40000, 50000, 60000, 70000]
age = [23, 25, 30, 35, 40]

data = pd.DataFrame({'age': age, 'income': income})

pearson = stats.pearsonr(data['age'], data['income'])
print(pearson)

spearman = stats.spearmanr(data['age'], data['income'])
print(spearman)
