#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline


# In[2]:


#Add your file path here
stock_path = os.path.join("Resources","FB_daily_stock_yahoo.csv")
employee_reviews_path = os.path.join("Resources","employee_reviews.csv")
int_rate_path = os.path.join("Resources","FEDFUNDS.csv")


# ## Facebook Stock Data 

# In[3]:


stock = pd.read_csv(stock_path)
stock.head()


# In[4]:


#Get the average stock price per month
stock["YYYY-MM"] = [x[:7] for x in stock["Date"]]
stock_grouped = stock.groupby("YYYY-MM")
stock_monthly = pd.DataFrame(stock_grouped["Close"].mean())
stock_monthly["Year Month"] = pd.to_datetime(stock_monthly.index)
stock_monthly.head()

#stock closing price vs employment rate
#reading employment csv
employment="employmentrates.csv"
employment_rate = pd.read_csv(employment)
#cleaning employment csv file
employment_rate=employment_rate.loc[employment_rate['SUBJECT']=='LREM64TT']
employment_rate["Time"] = pd.to_datetime(employment_rate["Time"])
employment=employment_rate.rename(columns={"Time":"Year Month","Value":"Employment Rate" })
employment.head(40)
#merge employment and stock data
combined_data=pd.merge(employment,stock_monthly,on='Year Month', how='inner')
combined_data.head()
#create employment and stock dataset
employment_and_stock=combined_data[['Year Month','Employment Rate','Close']]
employment_and_stock.head(27)
# plotting scatter plot
plt.figure(figsize=(10,8))
plt.scatter(employment_and_stock["Employment Rate"], employment_and_stock["Close"], color='b', alpha=0.5)
plt.grid()
plt.xlabel('Employment Rate')
plt.ylabel('Facebook Avg Monthly Close Price')
plt.title('Facebook Stock Price vs Employment Rate')
plt.plot(np.unique(employment_and_stock["Employment Rate"]), np.poly1d(np.polyfit(employment_and_stock["Employment Rate"],employment_and_stock["Close"] , 1))(np.unique(employment_and_stock["Employment Rate"])), color = "red")
plt.show()
#scatter plot with labels
plt.figure(figsize=(10,8))
plt.scatter(employment_and_stock["Employment Rate"], employment_and_stock["Close"], color='b', alpha=0.5)
plt.grid()
plt.xlabel('Employment Rate')
plt.ylabel('Facebook Avg Monthly Close Price')
plt.title('Facebook Stock Price vs Employment Rate')

for label, x, y in zip(employment_and_stock["Year Month"], employment_and_stock["Employment Rate"], employment_and_stock["Close"]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
plt.show()
'''
#####################################################
Effective Federal Funds Rate (Interest Rate) Analysis 
#####################################################
'''
#The effective federal funds rate is the interest rate banks charge each other for overnight loans to meet their reserve requirements. 
#Also known as the federal funds rate, the effective federal funds rate is set by the Federal Open Market Committee, or FOMC. 
#The effective federal funds rate is the most influential interest rate in the nation’s economy. 
# It affects employment, growth and inflation.
effr = pd.read_csv(int_rate_path)
effr["YYYY-MM"] = [x[:7] for x in effr["Date"]]
effr_grouped = effr.groupby("YYYY-MM").min()
effr_grouped.head()

#Merge DataFrames
merge_table = pd.merge(stock_monthly, effr_grouped, left_index = True, right_index = True, how="inner")
merge_table

# Obtain coordinates to plot graph
stock = merge_table[["Date", "Close","Federal Funds Rate"]]
stock.head()

#Scatterplot showing Interest Rate and Closing stock price for all monthly data points in two year period
x = stock["Federal Funds Rate"]
y = stock ["Close"]
plt.scatter(x, y, linewidth=1, marker="o", facecolors="blue", edgecolors="black", s=x_axis, alpha=0.75)
plt.title('Note : Affect of Interest Rate on Facebook Stock Price')
plt.xlabel('Effective Federal Funds Rate(Interest Rate)')
plt.ylabel('Facebook Stock Price(Closing)')
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color = "red")

#Scatterplot showing Interest Rate and Closing stock price minus the last three months of 2018 data
x_3 = stock.iloc[:-3,2]
y_3 = stock.iloc[:-3,1]
plt.scatter(x_3, y_3, linewidth=1, marker="o", facecolors="blue", edgecolors="black", s=x_axis, alpha=0.75)
plt.title('Note : Affect of Interest Rate on Facebook Stock Price')
plt.xlabel('Effective Federal Funds Rate(Interest Rate)')
plt.ylabel('Facebook Stock Price(Closing)')
plt.plot(np.unique(x_3), np.poly1d(np.polyfit(x_3, y_3, 1))(np.unique(x_3)), color = "red")

'''
##############################################
End of Interest Rate Analysis
##############################################
'''