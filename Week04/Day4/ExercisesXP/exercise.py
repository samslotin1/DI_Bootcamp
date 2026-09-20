# Exercise 1

# Data Analysis Overview

# Introduction
#Data analysis is something we hear about a lot today, especially with how much data is being created every second. From apps we use to businesses making decisions, data is everywhere. Because of this, understanding how to analyze data has become really important. This essay explains what data analysis is, why it matters, and where it’s used in real life.

# What is Data Analysis?
#Data analysis is basically the process of taking raw data and making sense of it. It involves collecting data, organizing it, and looking for patterns or trends that can help answer questions or solve problems.

#Instead of just having a bunch of numbers or information, data analysis helps turn that information into something useful. For example, a company might look at customer data to understand what people like or don’t like about a product.

# Why is Data Analysis Important?
#Data analysis is important because it helps people make better decisions. Instead of guessing, businesses and organizations can rely on actual data to guide them. This usually leads to more accurate and effective results.

#In today’s world, companies use data to understand customers, improve products, and stay competitive. Without data analysis, a lot of decisions would be based on assumptions, which can be risky.

#It also helps uncover patterns that might not be obvious at first. This can lead to new ideas, improvements, or even completely new strategies.

# Applications of Data Analysis

# Healthcare
#In healthcare, data analysis is used to improve patient care. Doctors and hospitals analyze patient data to better understand diseases and choose the best treatments. It can also help predict outbreaks or identify high-risk patients early.

# Finance
#In finance, data analysis is used to detect fraud and manage risk. Banks and financial institutions analyze transactions to spot unusual behavior. This helps protect people’s money and prevent financial crimes.

# Retail and Marketing
#Retail companies use data analysis to understand what customers want. For example, they track what people buy and use that information to recommend products or create better marketing campaigns. This is why online stores often suggest items that match your interests.

# Conclusion
#Overall, data analysis is a key part of how decisions are made today. It helps turn raw information into useful insights that can improve outcomes in many areas. Whether it’s healthcare, finance, or retail, data analysis plays a major role in making systems more efficient and effective.


# Exercise 2


# This dataset has 690 rows and 16 columns about credit card applications.
# It includes personal details (like age and gender) and financial info (like income and debt).
# The data is clean with no missing values.
# The main column is “Approved,” which shows whether an application was accepted (1) or rejected (0), and the data is fairly balanced



# The average depression rate is about 3.5%, with most values between 3% and 4%
# The low standard deviation (0.66) indicates that depression
# rates are relatively consistent across countries and years, without large fluctuations.



#This dataset includes 945 entries on how much Americans sleep, with details like year, age group, and type of day.
# It is clean and can be used to analyze sleep patterns across different groups and time periods.

# Exercise 3

# Dataset 1: Credit Card Approval
# The dataset contains both quantitative and qualitative variables. Quantitative variables include Age, Debt, YearsEmployed, CreditScore, and Income because they represent measurable numeric values. Qualitative variables include Gender, Married, BankCustomer, Industry, Ethnicity, PriorDefault, Employed, DriversLicense, Citizen, ZipCode, and Approved, as they represent categories or labels, even when stored as numbers.

# Dataset 2: Mental Health
# This dataset mainly consists of quantitative variables, such as Schizophrenia (%), Bipolar disorder (%), Eating disorders (%), Anxiety disorders (%), Drug use disorders (%), Depression (%), and Alcohol use disorders (%), as they represent measurable percentages. The column Year is also quantitative since it represents time. The columns Entity and Code are qualitative because they represent country names and labels.

# Dataset 3: Sleep
# The dataset contains both quantitative and qualitative variables. Quantitative variables include Avg hrs per day sleeping, Standard Error, and Year, as they represent measurable numeric values. Qualitative variables include Period, Type of Days, Age Group, Activity, and Sex, as they describe categories or groups. The index column is not meaningful for analysis and can be ignored.

# Exercise 4


# The columns sepal_length, sepal_width, petal_length, and petal_width are quantitative because they are numeric measurements. The column species is qualitative because it represents categories of flowers rather than numeric values.

# Exercise 5


# The columns Year and Avg hrs per day sleeping are useful for analyzing trends over time. The columns Age Group, Sex, and Avg hrs per day sleeping can be used to compare sleep patterns across different groups. Type of Days allows comparison between weekdays and weekends, and Standard Error indicates how reliable the data is.

# Exercise 6

# Structured
# Unstructured
# Unstructured
# Structured
# Unstructured

# Exercise 7

# Blog posts can be turned into structured data using text analysis to pull out things like topics or locations. Audio recordings can be converted to text using speech-to-text, then analyzed. Handwritten notes can be turned into text using OCR. Video tutorials can be processed by converting speech to text and extracting key steps.

# Exercise 8

import pandas as pd

df = pd.read_csv("train.csv")

print(df.head())

# Exercise 9



import pandas as pd

df = pd.DataFrame({
    "Name": ["Sam", "John", "Doe"],
    "Age": [12, 13, 14],
    "City": ["Savannah", "Atlanta", "Seattle"]
})

df.to_excel("data.xlsx", index=False)

df.to_json("data.json")

# Exercise 10

import pandas as pd

df = pd.read_json("https://jsonplaceholder.typicode.com/posts")

df.head()
df.info()
