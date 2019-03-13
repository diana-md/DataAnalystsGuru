#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np


# In[2]:


#Add your file path here
stock_path = os.path.join("Resources","FB_daily_stock_yahoo.csv")
employee_reviews_path = os.path.join("Resources","employee_reviews.csv")


# ## Facebook Stock Data 

# In[3]:


stock = pd.read_csv(stock_path)
stock_price=stock[['Date','Close']]
stock_price.head()


# In[4]:


#Get the average stock price per month
stock["YYYY-MM"] = [x[:7] for x in stock["Date"]]
stock_grouped = stock.groupby("YYYY-MM")
stock_monthly = pd.DataFrame(stock_grouped["Close"].mean())
stock_monthly["Year Month"] = pd.to_datetime(stock_monthly.index)
stock_monthly.head()


# In[5]:


employment="employmentrates.csv"
employment_rate = pd.read_csv(employment)


# In[6]:


employment_rate=employment_rate.loc[employment_rate['SUBJECT']=='LREM64TT']
employment_rate["Time"] = pd.to_datetime(employment_rate["Time"])
employment=employment_rate.rename(columns={"Time":"Year Month","Value":"Employment Rate" })
employment.head(40)


# In[7]:


combined_data=pd.merge(employment,stock_monthly,on='Year Month', how='inner')
combined_data.head()


# In[8]:


employment_and_interest=combined_data[['Year Month','Employment Rate','Close']]
employment_and_interest.head(27)


# In[16]:


plt.figure(figsize=(10,8))
plt.scatter(employment_and_interest["Employment Rate"], employment_and_interest["Close"], color='b', alpha=0.5)
plt.grid()
plt.xlabel('Employment Rate')
plt.ylabel('Facebook Avg Monthly Close Price')
plt.title('Facebook Stock Price vs Employment Rate')
plt.plot(np.unique(employment_and_interest["Employment Rate"]), np.poly1d(np.polyfit(employment_and_interest["Employment Rate"],employment_and_interest["Close"] , 1))(np.unique(employment_and_interest["Employment Rate"])), color = "red")
plt.show()


# In[14]:


plt.figure(figsize=(10,8))
plt.scatter(employment_and_interest["Employment Rate"], employment_and_interest["Close"], color='b', alpha=0.5)
plt.grid()
plt.xlabel('Employment Rate')
plt.ylabel('Facebook Avg Monthly Close Price')
plt.title('Facebook Stock Price vs Employment Rate')

for label, x, y in zip(employment_and_interest["Year Month"], employment_and_interest["Employment Rate"], employment_and_interest["Close"]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
plt.show()


# In[ ]:


trump="trump.csv"
trump_approval = pd.read_csv(trump)
trump_approval.head(20)


# In[ ]:


trump_gallup=trump_approval.loc[trump_approval['survey_organization']=='Gallup']
trump_ratings=trump_gallup[["end_date","approve_percent"]]
trump_disapproval=trump_ratings.rename(columns={"end_date":"Date","approve_percent":"Approval Percentage" })
trump_disapproval.head()


# In[ ]:


combined=pd.merge(trump_disapproval,stock_price,on='Date', how='inner')
combined.head(40)


# In[ ]:


plt.figure(figsize=(10,8))
plt.scatter(combined["Approval Percentage"], combined["Close"], color='b', alpha=0.5)
plt.grid()
plt.xlabel('Trump Approval Rate')
plt.ylabel('Facebook Avg Monthly Close Price')
plt.title('Facebook Stock Price vs Trump Approval Rate')
plt.plot(np.unique(combined["Approval Percentage"]), np.poly1d(np.polyfit(combined["Approval Percentage"],combined["Close"] , 1))(np.unique(combined["Approval Percentage"])), color = "red")
plt.show()


# In[ ]:




