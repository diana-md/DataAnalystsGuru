#!/usr/bin/env python
# coding: utf-8

# In[137]:


import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[138]:


#file to load
#Add your file path here
#_daily_stock_yahoo
stock_path = os.path.join("Resources","FB_daily_stock_yahoo.csv")
int_rate_path = os.path.join("Resources","FEDFUNDS.csv")


# In[207]:


stock = pd.read_csv(stock_path)
stock.head()


# In[193]:


#The effective federal funds rate is the interest rate banks charge each other for overnight loans to meet their reserve requirements. 
#Also known as the federal funds rate, the effective federal funds rate is set by the Federal Open Market Committee, or FOMC. 
#The effective federal funds rate is the most influential interest rate in the nation’s economy. It affects employment, growth and inflation.
effr = pd.read_csv(int_rate_path)
effr["YYYY-MM"] = [x[:7] for x in effr["Date"]]
effr_grouped = effr.groupby("YYYY-MM").min()
effr_grouped.head()


# In[192]:


#Get the average stock price per month
stock["YYYY-MM"] = [x[:7] for x in stock["Date"]]
stock_grouped = stock.groupby("YYYY-MM")
stock_monthly = pd.DataFrame(stock_grouped["Close"].mean())
# stock_monthly["Year Month"] = pd.to_datetime(stock_monthly.index)
stock_monthly.head()


# In[195]:


merge_table = pd.merge(stock_monthly, effr_grouped, left_index = True, right_index = True, how="inner")
merge_table


# In[197]:


# Obtain coordinates to plot graph
stock = merge_table[["Date", "Close","Federal Funds Rate"]]
stock.head()


# In[205]:


x = stock["Federal Funds Rate"]
y = stock ["Close"]
plt.scatter(x, y, linewidth=1, marker="o", facecolors="blue", edgecolors="black", s=x_axis, alpha=0.75)
plt.title('Note : Affect of Interest Rate on Facebook Stock Price')
plt.xlabel('Effective Federal Funds Rate(Interest Rate)')
plt.ylabel('Facebook Stock Price(Closing)')
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color = "red")


# In[206]:


x_3 = stock.iloc[:-3,2]
y_3 = stock.iloc[:-3,1]
plt.scatter(x_3, y_3, linewidth=1, marker="o", facecolors="blue", edgecolors="black", s=x_axis, alpha=0.75)
plt.title('Note : Affect of Interest Rate on Facebook Stock Price')
plt.xlabel('Effective Federal Funds Rate(Interest Rate)')
plt.ylabel('Facebook Stock Price(Closing)')
plt.plot(np.unique(x_3), np.poly1d(np.polyfit(x_3, y_3, 1))(np.unique(x_3)), color = "red")


# In[ ]:




