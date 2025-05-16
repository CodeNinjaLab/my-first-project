# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned dataset
df = pd.read_csv('02_data_clean/sales_data_clean.csv')

# Step 1: Correlation Between Products
# I’ll check how different products are correlated with each other to see if there's a relationship
# in sales.
# This is useful for understanding if the sales of one product are linked with another.
# Step 1: Correlation Between Products
#
# In this step, I want to understand if the sales of different products
# are related to each other. To do this, I am calculating the *correlation*
# between products.
#
# What does correlation mean? Basically, it tells me how much two things
# move together. The value goes from -1 to +1:
#
# +1 means they move exactly the same (strong positive link).
#  0 means there is no connection between them.
# -1 means they move in the opposite direction (strong negative link).
#
# For example:
# If M01AB and M01AE both go up and down at the same time,
# their correlation might be around 0.90 or even higher.
#
# But if M01AB goes up and M01AE goes down, the correlation will be
# negative, like -0.5.
#
# If there’s no pattern at all between them, the correlation will be close to 0.
#
# Why am I doing this?
# It helps me find out if customers are buying some products together.
#
# For example, maybe when people buy painkillers (like N02BA),
# they also buy cough medicines (like R03).
#
# That would be useful to know for making marketing plans or
# product bundles.
#
# Now I’m going to select the product columns I want to check,
# and then use the .corr() function to create a correlation matrix.

correlation_matrix = df[['m01ab', 'm01ae', 'n02ba', 'n02be', 'n05b', 'n05c', 'r03', 'r06']].corr()

# Visualize the correlation matrix using a heatmap

# Now I want to **visualize** the correlation matrix I created.
#
# I’m using a heatmap for this, which is basically a colored table
# that shows how strongly the products are related to each other.
#
# Dark red means strong positive correlation (closer to +1).
# Dark blue means strong negative correlation (closer to -1).
# White or light shades mean weak or no correlation (close to 0).
#
# I’m using seaborn’s heatmap() function to do this.
#
# figsize=(10, 8) makes the plot bigger so it’s easier to read.
#
# annot=True means the actual numbers (like 0.92, -0.35) will show up
# inside the boxes.if annot = False then there will be only colour inside
# the chart no values.
#
# cmap='coolwarm' sets the color scheme — warm colors for positive,
# cool colors for negative.
#
# fmt='.2f' means round the numbers to 2 decimal places.
#
# cbar=True adds the color scale bar on the side so I can see
# what the colors mean.with cbar = False there will be no
# colour bar at the side of the chart for me to view and know
# what each colour means.
#
# Finally, I added a title to explain what the chart is showing.
# plt.show() displays the chart.

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title('Correlation Between Products', fontsize=16)
plt.show()

# Step 2: Moving Averages & Seasonality
# To observe seasonality in the data, I will calculate a moving average for the sales of a few products.
# This helps in smoothing out fluctuations and identifying clear patterns over time.
# Now I’m going to calculate the moving average for product M01AB.
#
# I use .rolling(window=30) to create a 30-day moving window.
# This means it will look at the last 30 rows (30 days of sales).
#
# Then I use .mean() to get the average of those 30 days.
#
# So instead of just showing one day’s sales,
# it shows the average sales from the past 30 days.
#
# This helps smooth out any daily ups and downs in the data.
#
# The result is stored in a new column called 'm01ab_rolling_avg'.
#
# I do the same for M01AE — calculating its 30-day moving average
# and saving it in a column called 'm01ae_rolling_avg'.
#
# These rolling averages will help me see the sales trend
# more clearly when I plot them.
# I'm calculating a 30-day rolling average for product sales.
# This helps smooth out daily "noise" — random ups and downs in sales.
# For example, sales may jump from 200 to 120 to 300 in three days.
# That doesn’t mean a real trend — it’s just noise (like weather or discounts).
# So I use a 30-day window to get a clearer pattern.
# How it works:
# - First it averages sales from Day 1 to Day 30.
# - Then Day 2 to Day 31, then Day 3 to Day 32, and so on.
# This rolling average is useful to reveal real trends (like seasonality or growth).

df['m01ab_rolling_avg'] = df['m01ab'].rolling(window=30).mean() # for product M01AB,30-day moving average

# same as upper step i want to see the rolling average of this product also.

df['m01ae_rolling_avg'] = df['m01ae'].rolling(window=30).mean()

# First, I'm creating a new figure for the plot and setting its size.
# This makes sure the chart is wide enough to clearly see the lines.

plt.figure(figsize=(12, 6))

# This line plots the **original M01AB daily sales**
# It uses 'datum' (date) for the x-axis and 'm01ab' (sales) for the y-axis.
# The line will look a bit jagged(rough/uneven) because it's showing the actual ups and downs every day.
# The 'alpha=0.7' makes the line a little bit transparent so overlapping lines are easier to see.

plt.plot(df['datum'], df['m01ab'], label='M01AB Sales', alpha=0.7)

# This line plots the **30-day rolling average for M01AB**
# It's a smoother version of the original sales line, showing the trend over time.
# The 'linestyle="--"' makes it a dashed line so i can easily tell it apart from the original sales line

plt.plot(df['datum'], df['m01ab_rolling_avg'], label='M01AB Rolling Avg', linestyle='--')

# This line plots the **original M01AE daily sales**
# Just like before, it shows the real daily sales of another product (M01AE).
# Again, using 'alpha=0.7' to help with visibility when lines overlap.

plt.plot(df['datum'], df['m01ae'], label='M01AE Sales', alpha=0.7)

# This line plots the **30-day rolling average for M01AE**
# It shows the smoothed-out sales trend for M01AE over time.
# Dashed line again to keep it visually separate from the original sales.

plt.plot(df['datum'], df['m01ae_rolling_avg'], label='M01AE Rolling Avg', linestyle='--')

# Setting the title of the chart so it's clear what the plot is about.

plt.title('Sales & Moving Averages of M01AB and M01AE', fontsize=16)

# Labeling the x-axis to show that it represents dates.

plt.xlabel('Date')

# Labeling the y-axis to show that it represents sales numbers.

plt.ylabel('Sales')

# 🧭 Adding a legend so viewers know which line is which.
plt.legend()

# 👀 Finally, showing the plot so it appears on screen.
plt.show()

# Step 3: Sales by Weekday & Hour
# I’ll analyze how sales change depending on the day of the week and hour of the day.
# This helps to understand patterns related to time—whether certain products sell more on specific
# days or hours.

sales_by_weekday = df.groupby('weekday_name')[['m01ab', 'm01ae', 'n02ba']].sum()

# Plotting sales by weekday
sales_by_weekday.plot(kind='bar', figsize=(10, 6))
plt.title('Sales by Weekday', fontsize=16)
plt.xlabel('Weekday')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# Step 4: Sales by Hour (How sales change during the day)
sales_by_hour = df.groupby('hour')[['m01ab', 'm01ae', 'n02ba']].sum()

# Plotting sales by hour
sales_by_hour.plot(kind='line', figsize=(10, 6))
plt.title('Sales by Hour of the Day', fontsize=16)
plt.xlabel('Hour of the Day')
plt.ylabel('Total Sales')
plt.show()

# Step 5: Identifying Top 10 Sales Spikes/Dips
# I’ll identify the days with the highest and lowest sales.
# This can be valuable for understanding peak sales periods and why certain days
# ee large fluctuations in sales.
# Selecting only 'datum', 'm01ab', and 'm01ae' columns from df
# Then setting 'datum' as the index (row labels)
# This makes it easier to find sales by date and sort by sales values
#
# Example before:
#   index  datum       m01ab  m01ae
#   0      2020-01-01  100    200
#   1      2020-01-02  150    180
#
# After setting index:
#            m01ab  m01ae
# datum                 
# 2020-01-01  100    200
# 2020-01-02  150    180
#
# This helps us find days with biggest sales spikes or dips easily.

sales_spikes_dips = df[['datum', 'm01ab', 'm01ae']].set_index('datum')

# Sorting and picking top 10 sales spikes and dips for M01AB
# Now, I want to find the days when the product M01AB had the biggest drops in sales,
# meaning the days with the lowest sales numbers.
# To do this, I sort the sales data by the 'm01ab' column.
# Notice I did NOT write 'ascending=True' here.
# That’s because in pandas, if i don't specify ascending = TRUE OR FALSE then, 
# it automatically sorts in ascending order by default (from smallest to largest).
# So, this line sorts the sales from the lowest to the highest,
# and then .head(10) picks the first 10 rows, which means the 10 days with the lowest sales.
# This helps me find the sales dips to understand when the product was selling poorly.

top_10_spikes = sales_spikes_dips.sort_values(by='m01ab', ascending=False).head(10)
top_10_dips = sales_spikes_dips.sort_values(by='m01ab').head(10)

# Displaying the top 10 sales spikes and dips
print("Top 10 Sales Spikes (M01AB):")
print(top_10_spikes)

print("\nTop 10 Sales Dips (M01AB):")
print(top_10_dips)


# -------------------- FINAL NOTE --------------------
# This code explores sales trends for pharma products.
# It covers:
# - Correlation between products
# - Moving averages to show trends
# - Sales patterns by weekday/hour
# - Top 10 sales spikes & dips

# Purpose:
# To find patterns, spot seasonality, and understand product behavior over time.

# Adaptability:
# Replace the dataset to reuse.
# Add/remove products or change the rolling window easily.
# Useful for other industries too (e.g. e-commerce, finance).

