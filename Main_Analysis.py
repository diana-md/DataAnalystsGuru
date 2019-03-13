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


# In[ ]:#!/usr/bin/env python
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




#!/usr/bin/env python
# coding: utf-8

# In[18]:


get_ipython().run_line_magic('matplotlib', 'inline')
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress

# File to Load (Remember to change these)
vix_data_to_load = "Resources/vix-daily.csv"
fb_data_to_load = "Resources/FB_daily_stock_yahoo.csv"

# Read the City and Ride Data
vix_data_df = pd.read_csv(vix_data_to_load)
fb_data_df = pd.read_csv(fb_data_to_load)
#fb_data_df
renamed_fb_df = fb_data_df.rename(columns={"Date": "Date", "Open": "FB Open", "High": "FB High", "Low": "FB Low", "Close": "FB Close",
                                          "Volume": "FB Volume"})
renamed_fb_df.head()


# In[19]:


#vix_data_df.tail()
combined_data_df = pd.merge(vix_data_df, renamed_fb_df, how='inner', on='Date')
combined_data_df.head()


# In[20]:


# Obtain the x and y coordinates
vix_fb_df = combined_data_df[["Date", "VIX Close","FB Close"]]
vix_fb_df.head()


# In[21]:


# Create a handle for each plot
plt.scatter(vix_fb_df["VIX Close"], vix_fb_df["FB Close"],color="blue", linewidth=1, label="VIX Close Price")
plt.plot(np.unique(vix_fb_df["VIX Close"]), np.poly1d(np.polyfit(vix_fb_df["VIX Close"], vix_fb_df["FB Close"], 1))(np.unique(vix_fb_df["VIX Close"])), color = "red")


# In[22]:


plt.plot(vix_fb_df["Date"], vix_fb_df["FB Close"])
plt.plot(vix_fb_df["Date"], vix_fb_df["VIX Close"])
plt.show()


# In[65]:


fig, ax1 = plt.subplots(1, 2, figsize=(8, 4))
ax1[0].plot(vix_fb_df["Date"], vix_fb_df["FB Close"], 'b-')
ax1[0].set_xlabel('Date (day)')

# Make the y-axis label, ticks and tick labels match the line color.
ax1[0].set_ylabel('Facebook (Price)', color='b')
ax1[0].tick_params('y', colors='b')

ax2 = ax1[0].twinx()
ax2.plot(vix_fb_df["Date"], vix_fb_df["VIX Close"], 'r-')

ax2.set_ylabel('VIX (Fear)', color='r')
ax2.tick_params('y', colors='r')

# fig.tight_layout()

# # Save Figure
# plt.savefig("dualaxes_line_plot.png", bbox_inches="tight")

(slope, intercept, _, _, _) = linregress(vix_fb_df["VIX Close"], vix_fb_df["FB Close"])
fit = slope * vix_fb_df["VIX Close"] + intercept

ax1[1].set_xlim(5, 35)
ax1[1].set_ylim(100, 220)

ax1[1].set_xlabel("Market Fear (in days)")
ax1[1].set_ylabel("Facebook Stock Price (in days)")

ax1[1].plot(vix_fb_df["VIX Close"], vix_fb_df["FB Close"], linewidth=0, marker='o')
ax1[1].plot(vix_fb_df["VIX Close"], fit, 'b--')

plt.subplots_adjust(hspace=-5)

# Save Figure
plt.savefig("combine_line-scatter_plot.png", bbox_inches="tight")

# plt.show()
plt.show()


# In[46]:


(slope, intercept, _, _, _) = linregress(vix_fb_df["VIX Close"], vix_fb_df["FB Close"])
fit = slope * vix_fb_df["VIX Close"] + intercept

fig, ax = plt.subplots(figsize=(8, 4))

fig.suptitle("Market Fear VIX vs Facebook Stock Price", fontsize=16, fontweight="bold")

ax.set_xlim(10, 35)
ax.set_ylim(100, 220)
plt.grid(axis='both', alpha=0.5)

ax.set_xlabel("Market Fear (in days)")
ax.set_ylabel("Facebook Stock Price (in days)")

ax.plot(vix_fb_df["VIX Close"], vix_fb_df["FB Close"], linewidth=0, marker='o')
ax.plot(vix_fb_df["VIX Close"], fit, 'b--')

# Save Figure
plt.savefig("linreg_scatter_plot.png", bbox_inches="tight")

plt.show()


# In[56]:


fig, ax1 = plt.subplots(figsize=(8, 4))
fb_handle, = ax1.plot(vix_fb_df["Date"], vix_fb_df["FB Close"], 'b-')
ax1.set_xlabel('Date (day)')
plt.legend(loc="upper left")

# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Facebook (Price)', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
vix_handle, = ax2.plot(vix_fb_df["Date"], vix_fb_df["VIX Close"], 'r-')

ax2.set_ylabel('VIX (Fear)', color='r')
ax2.tick_params('y', colors='r')

ax1.legend(['Facebook Close Prices'], loc='upper left')
ax2.legend(['VIX Close Prices'], loc='upper right')
# plt.legend(loc="upper left")

fig.tight_layout()


# Create a legend


# Save Figure
plt.savefig("dualaxes_line_plot.png", bbox_inches="tight")


# In[ ]:




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




