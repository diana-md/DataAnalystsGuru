#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


#Add your file path here
stock_path = os.path.join("Resources","FB_daily_stock_yahoo.csv")
employee_reviews_path = os.path.join("Resources","employee_reviews.csv")


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


# ## Employee Reviews

# In[5]:


reviews_df = pd.read_csv(employee_reviews_path)
fb_reviews_df = reviews_df[reviews_df["company"] == "facebook"]
fb_reviews_df.head()


# In[9]:


fb_reviews_short = fb_reviews_df[[True if x[-4:] == "2018" or x[-4:] == "2017" else False for x in fb_reviews_df["dates"]]]
fb_reviews_short.loc[:,"Month Year"] = [x[:5] + x[-4:] for x in np.array(fb_reviews_short["dates"])]


# In[21]:


grouped_reviews = fb_reviews_short.groupby("Month Year")
monthly_rating = pd.DataFrame(grouped_reviews["overall-ratings"].mean())
monthly_rating.index.names = ["Date"]
monthly_rating["Month Year"] = pd.to_datetime(monthly_rating.index)
monthly_rating_sorted = monthly_rating.sort_values(by="Month Year")
monthly_rating_sorted = monthly_rating_sorted.rename(columns = {"Month Year":"Year Month"})
monthly_rating_sorted.head()


# In[22]:


# Join the two data sets
joined_stock = pd.merge(monthly_rating_sorted,stock_monthly, on = "Year Month")
joined_stock.head()


# In[31]:


# Plot the data
x = joined_stock["overall-ratings"]
y = joined_stock["Close"]
plt.scatter(x,y)
plt.title("Relationship between employee reviews and Facebook stock value")
plt.xlabel("Average Monthly Employee Overall Review")
plt.ylabel("Average Monthly Stock Value ($)")
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color = "red")


# In[ ]:




