#importing the necssary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned dataset
df = pd.read_csv("02_data_clean/sales_data_clean.csv")

# List of product columns
product_columns = ['m01ab', 'm01ae', 'n02ba', 'n02be', 'n05b', 'n05c', 'r03', 'r06']

# 1.Correlation Between Product Categories

# This helps to see if some products are usually bought together

# In this step, I am going to create a correlation matrix. It helps me understand how the 
# sales of one product are related to the sales of another. Basically, it shows if two 
# products’ sales go up and down together or not.

# When I run this code df[product_columns].corr()

# It checks each row (like each day/week) and compares how the sales numbers of each 
# product are changing. Then it gives a number to show how closely they are linked.

# If the value is close to 1.00 (like 0.98), that means strong connection.
# If it's low (like 0.40), that means weak connection.

# 🧪 Example:
# Sales for 4 products over 4 weeks:

# Week | AB | AE | AG | AH
# -------------------------
#  1   |100 |150 |200 | 50
#  2   |110 |160 |210 | 55
#  3   | 90 |140 |190 | 45
#  4   |105 |155 |205 | 50

# Now i run:
# df[["AB", "AE", "AG", "AH"]].corr()

# 🧩 Correlation Matrix:

#      | AB  AE  AG  AH
# ----------------------
#  AB  |1.00 .98 .98 .45
#  AE  |.98 1.00 1.00 .50
#  AG  |.98 1.00 1.00 .48
#  AH  |.45 .50 .48 1.00

# 🎯 Meaning:
# - AB and AE = 0.98 → stronger connection.
# - AE and AG = 1.00 → very strong.
# - AB and AH = 0.45 → weaker connection.

# This helps me find which products sell similarly. Useful for bundling or analysis.

corr = df[product_columns].corr()


# In this step, I am setting up a blank figure, basically an empty chart with no values inside.
# The chart will have a width of 10 inches and a height of 6 inches.

plt.figure(figsize=(10, 6))

# In this step, sns.heatmap() will create the heatmap.
# `corr` is the correlation matrix that I made earlier using .corr().
# `annot=True` means I’ll see the exact values (like 0.98) written inside the boxes, not just colors.
# So I can know the actual number for how strong the relationship is between products.
# The color will show the strength visually: dark/warm colors for strong correlation, light/cool colors
# for weak ones.
# `cmap='coolwarm'` is the color theme I’m using — cool colors for low correlation, warm for high.
# `fmt=".2f"` means round the numbers to 2 decimal places, like 0.98765 becomes 0.99.

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")

# the rest are the same as the steps that i did in exploration.py so im not gona give detail on these
# steps since i have already given that detail in previous python file.

plt.title("Correlation Between Product Categories")
plt.tight_layout()
plt.savefig("04_outputs/product_correlation_heatmap.png")
plt.show()
plt.close()

# 2. Moving Average of Total Sales (by Month)

# Helps smooth out noise and spot seasonality

# First, calculate total sales

# In this step, I’m going to calculate the total sales for each time period (e.g., each day or week).
# I do this by summing up the sales of all product categories row by row.
# For example, if one row (a week) has values like 10, 20, and 300 across products, the total for that
#  row becomes 330.
# This will give me one column called 'total_sales' showing combined sales for every time entry in 
# the dataset.

# In this step, I'm calculating the total sales for each time period (e.g., week) by adding up the sales 
# of all products in that period. The `.sum(axis=1)` part ensures that the sum is done across each row, 
# not down columns. So, for each row (representing a specific time period), it adds up the sales from 
# all products to give the total sales for that time period. The result is saved in a new column called 
# 'total_sales'.

df['total_sales'] = df[product_columns].sum(axis=1)

# Then calculate moving average (window of 3 months)

# In this step, I'm using the groupby function to organize my data by year and month.
# This means that all rows with the same year and month will be grouped together.
# However, im not yet summing the sales for each group — im just organizing the data into groups.

# For example, if January 2020 has multiple rows (with sales like 8, 2, 5), 
# those rows will be grouped together under (2020, 1) without changing the data itself.
# Similarly, February 2020 will be grouped as (2020, 2), with all February sales together.

# This step helps prepare the data for aggregation (like summing sales) but doesn't perform that
# calculation yet.
# If i only grouped without summing, the output would look like this (just showing groups):

# Group: (2020, 1)
# | year | month | total_sales |
# |------|-------|-------------|
# | 2020 |   1   |     8       |
# | 2020 |   1   |     2       |
# | 2020 |   1   |     5       |

# Group: (2020, 2)
# | year | month | total_sales |
# |------|-------|-------------|
# | 2020 |   2   |     10      |
# | 2020 |   2   |     7       |

# Once we add the summing step, we will get the total sales for each month, 
# which will help us in calculating the moving averages and identifying trends.

monthly_sales = df.groupby(['year', 'month'])['total_sales'].sum().reset_index()

# In this step, I’m calculating the moving average of total sales over a 3-month period.
# Using .rolling(window=3), I’m grouping the sales data in chunks of 3 months at a time and 
# then calculating the average for each chunk. This helps to smooth out short-term fluctuations 
# and identify longer-term trends or patterns in sales. 
# For example, January + February + March’s total sales will give the average for those 3 months, 
# then February + March + April will give the next average, and so on.
# The new moving average will be added as a column called 'moving_avg' to the dataset.


monthly_sales['moving_avg'] = monthly_sales['total_sales'].rolling(window=3).mean()


# In this step, I'm plotting the monthly sales data as a line chart. 
# 'monthly_sales['total_sales']' is used to plot the total sales for each month. 
# The 'label' argument adds a name ('Monthly Sales') to the line in the chart's legend. 
# 'alpha=0.5' makes the line semi-transparent, allowing other chart elements to be clearly visible 
# while still showing the sales trend.

# a lot of the steps are the same as resolution python file which i created earlier so im not gona go in
# their detail ill go in detail of those steps which are new like plt legend

# I haven't specified a color for this line, so it will automatically 
# be assigned the default color (usually blue). Additionally, I set 
# alpha=0.5, which makes the line semi-transparent. This transparency 
# helps if there are overlapping lines, making it easier to see all data.
# if no colour is assigned then it will assign it on default blue most likely.

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales['total_sales'], label='Monthly Sales', alpha=0.5)

# In this step, I'm plotting the 3-month moving average on the chart. 
# By using `color='red'`, I'm making sure the moving average line will be shown in red on the chart.
# This helps differentiate it from the other lines, so when you look at the chart, you can easily spot
# which line represents the moving average.
# The label '3-Month Moving Average' will appear in the legend, so you’ll know exactly which line it is.

plt.plot(monthly_sales['moving_avg'], label='3-Month Moving Average', color='red')
plt.title("Monthly Sales with Moving Average")

# plt.xlabel("Month Index") adds a label to the x-axis of the chart.
# The x-axis represents the order of months after grouping by year and month.
# It's named "Month Index" because each point shows monthly sales one after another.

plt.xlabel("Month Index")

# plt.ylabel("Sales") adds a label to the y-axis of the chart.
# The y-axis represents the total sales amount for each month.
# So, it shows total sales (after grouping).

plt.ylabel("Sales")

# The plt.legend() step adds a legend to the chart. 
# A legend is like a key or guide, showing what each line represents. 
# Without it, i wouldn't know which line corresponds to the 'Monthly Sales' 
# and which one represents the '3-Month Moving Average'. The labels 
# from the plt.plot() commands help in identifying these lines in the legend.

plt.legend()
plt.tight_layout()
plt.savefig("04_outputs/moving_average_sales.png")
plt.show()

# In this step, plt.close() is used to close the current plot after it has been displayed.
# It is useful when i want to make sure that the next plot you generate does not 
# overlap with the previous one, keeping your visualizations clean.
# It essentially clears the figure, freeing up memory and preparing the environment 
# for any future plotting. Without plt.close(), the current plot may stay open 
# until manually closed, potentially causing issues with multiple plots.

# basically plt.close makes sure that no over lapping maps all at once open up on my screen when i
# run the code but instead one by one when i close one only then next will pop up.

plt.close()


# 3. Sales by Weekday and Hour

# I,ll group the data to see which days + hours perform best

# In this step, I'm grouping the dataset by 'weekday_name' (day of the week) 
# and 'hour' (time of day) to organize the sales data based on each combination of weekday and hour.
# 
# I calculate the average sales for each group using .mean(). This gives the average total sales 
# for each combination of weekday and hour.
# 
# .unstack() reshapes the data, moving the 'hour' to columns. Now, rows represent weekdays 
# and columns represent hours, with the average sales in the table cells.
# 
# Example:
# If the data for Monday and Tuesday looks like this:
#
# | weekday_name | hour | total_sales |
# |--------------|------|-------------|
# | Monday       | 1    | 100         |
# | Monday       | 2    | 150         |
# | Tuesday      | 1    | 120         |
# | Tuesday      | 2    | 140         |
#
# After .groupby() and .unstack(), the result will be:
#
# | hour       | 1    | 2    |
# |------------|------|------|
# | Monday     | 100  | 150  |
# | Tuesday    | 120  | 140  |
#
# This shows average sales for each hour across weekdays, making comparison easy.


weekday_hour = df.groupby(['weekday_name', 'hour'])['total_sales'].mean().unstack()

plt.figure(figsize=(12, 6))

# In this step, I'm using seaborn's heatmap function to visualize the weekday-hour sales data 
# in the form of a heatmap. The variable 'weekday_hour' contains a DataFrame where:
# - Rows represent days of the week (e.g., Monday, Tuesday, etc.)
# - Columns represent the hour of the day (from 0 to 23)
# - Values represent the **average total sales** for each weekday-hour combination.

# The sns.heatmap() function creates a colored matrix, where each cell’s color intensity 
# reflects the value (i.e., average sales) it contains. This makes it easy to spot patterns 
# in the data — for example, which hours of the day typically see high sales, or which days 
# tend to be slower.

# 💥 HIGHLIGHT: The cmap='YlGnBu' argument is used to specify the **color palette** for the heatmap.
#               'YlGnBu' is short for **Yellow-Green-Blue**:
#   - Yellow represents the **lowest values** (low average sales)
#   - Green is in the **middle range**
#   - Blue represents the **highest values** (high average sales)
# This gradient makes it visually intuitive: lighter colors = low sales, darker colors = high sales.

# So when reading the heatmap:
# - Cells that are **yellow** indicate times with low average sales.
# - Cells that are **blue** indicate times with high average sales.
# - This color mapping helps reveal daily and hourly sales patterns instantly.


sns.heatmap(weekday_hour, cmap='YlGnBu')
plt.title("Average Sales by Weekday and Hour")

# In this step, I'm labeling the x and y axes of the heatmap to clarify what the data shows.

# plt.xlabel("Hour of Day")
# → This labels the x-axis, which shows the 'hour' values after grouping.
# → It represents the hour in 24-hour format (0 to 23), like 0 = midnight, 12 = noon, 18 = 6 PM.

# plt.ylabel("Day of Week")
# → This labels the y-axis, which shows the 'weekday_name' values after grouping.
# → It represents the day of the week: Monday, Tuesday, ..., Sunday.

# The heatmap is based on grouped data:
# → We grouped by both 'weekday_name' and 'hour', then calculated the average sales.
# → So each cell shows the *average* total sales for that weekday and hour.

# Example:
# - Cell at (Wednesday, 14) shows avg sales on Wednesdays at 2 PM.
# - Cell at (Saturday, 9) shows avg sales on Saturdays at 9 AM.

# This layout makes it easy to see patterns in sales activity across the week and day.
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.tight_layout()
plt.savefig("04_outputs/sales_by_weekday_hour_heatmap.png")
plt.show()
plt.close()


# 4. Top 10 Sales Spikes and Dips

# I,ll find which individual days had the highest or lowest sales

# Group sales by date
# In this step, I'm calculating the total sales for each individual date.

# df.groupby('datum')['total_sales'].sum()
# → This groups the dataset by the 'datum' column, which represents each calendar date.
# → For each date, it sums up the values in the 'total_sales' column.
# → This gives the *total* sales for each day.

# .reset_index()
# → After grouping, the result has 'datum' as the index.
# → reset_index() converts it back into a regular column so it's easier to work with as a DataFrame.

# The final result is a new DataFrame:
# - One row per date (from the original 'datum' column)
# - A column showing the total sales on that date

# Example:
# If your dataset had:
# | datum      | total_sales |
# |------------|-------------|
# | 2020-01-01 | 100         |
# | 2020-01-01 | 150         |
# | 2020-01-02 | 200         |

# After groupby and sum:
# | datum      | total_sales |
# |------------|-------------|
# | 2020-01-01 | 250         |
# | 2020-01-02 | 200         |
daily_sales = df.groupby('datum')['total_sales'].sum().reset_index()

# Top 10 highest sales days
# In this step, I'm identifying the top 10 dates with the highest total sales.

# daily_sales.sort_values(by='total_sales', ascending=False)
# → This sorts the DataFrame 'daily_sales' by the 'total_sales' column.
# → The parameter ascending=False means it sorts in *descending* order (highest sales first).

# .head(10)
# → After sorting, this selects the first 10 rows from the top.
# → These are the 10 days with the highest total sales.

# The resulting DataFrame 'top_spikes' contains:
# - The 10 individual dates that had the highest sales
# - Useful for spotting peak sales days, which could be due to promotions, holidays, or other events

# Example:
# If the highest sales days were on 2020-12-24, 2021-01-01, etc., those will appear in this result.
top_spikes = daily_sales.sort_values(by='total_sales', ascending=False).head(10)

# Top 10 lowest sales days (excluding zero sales if needed)
# In this step, I'm identifying the 10 dates with the lowest total sales.

# daily_sales.sort_values(by='total_sales', ascending=True)
# → This sorts the DataFrame 'daily_sales' by the 'total_sales' column in *ascending* order.
# → This means the dates with the lowest total sales will come first.

# .head(10)
# → After sorting, this selects the first 10 rows from the bottom.
# → These are the 10 days with the *least* sales.

# The resulting DataFrame 'top_dips' contains:
# - The 10 individual dates where sales were at their lowest
# - This can help identify issues such as system downtimes, holidays, or low customer activity days.

# Example:
# If sales were close to zero on public holidays or technical outage days, those dates would show up here

top_dips = daily_sales.sort_values(by='total_sales', ascending=True).head(10)

# Plotting both
# In this step, I’m visualizing the top 10 sales spikes (best days) and top 10 sales dips (worst days) 
# using bar charts.

# For the Top 10 Sales Spikes:
# I create a bar chart where each bar represents a day with the highest total sales.
# The x-axis represents the dates, and the y-axis shows the total sales.
# The x-axis labels (dates) are rotated for better readability.
# The title of the chart is "Top 10 Sales Spikes (Best Days)" to indicate that it shows the days 
# with the highest sales.
# The chart is saved as a PNG file in the "04_outputs" folder and displayed on the screen.

# For the Top 10 Sales Dips:
# I create a similar bar chart but for the days with the lowest sales.
# The title "Top 10 Sales Dips (Worst Days)" clearly shows that this chart represents 
# the days with the least sales.
# The x-axis labels are rotated for better readability, and the plot is saved and displayed as well.

# By visualizing both, I can easily identify the best and worst performing sales days 
# and look for trends, anomalies, or opportunities for improvement.

# sns.barplot(): This creates a bar chart using Seaborn, a Python data visualization library.
# It is used to show the relationship between the x and y variables in a bar chart format.

# x='datum': This sets the x-axis to represent the 'datum' column (dates).
# It shows which specific dates (days) correspond to the sales spikes.

# y='total_sales': This sets the y-axis to represent the 'total_sales' column.
# The height of each bar will correspond to the total sales for each specific date.

# data=top_spikes: This specifies that the data used for the chart comes from the 'top_spikes' DataFrame.
# 'top_spikes' contains the top 10 days with the highest total sales, allowing us to visualize 
# the best days for sales.

plt.figure(figsize=(10, 5))
sns.barplot(x='datum', y='total_sales', data=top_spikes)
plt.xticks(rotation=45)
plt.title("Top 10 Sales Spikes (Best Days)")
plt.tight_layout()
plt.savefig("04_outputs/top_10_sales_spikes.png")
plt.show()
plt.close()

plt.figure(figsize=(10, 5))
sns.barplot(x='datum', y='total_sales', data=top_dips)
plt.xticks(rotation=45)
plt.title("Top 10 Sales Dips (Worst Days)")
plt.tight_layout()
plt.savefig("04_outputs/top_10_sales_dips.png")
plt.show()
plt.close()

print(" Step 4 visualizations saved in 04_outputs/")

                      # CODE COMPLETED SUCCESFULLY #

# Purpose of the Code:
# The goal of this code is to analyze sales data from a pharmaceutical company 
# over the past 6 years. By cleaning, exploring, and visualizing the dataset, 
# we aim to identify key trends, seasonal patterns, correlations between product 
# categories, and high-performance timeframes to help make data-driven decisions. 
# The code also performs advanced analysis to understand the sales behavior and 
# offers insights for improving business strategies.

# 1. Data Cleaning and Preprocessing
# Objective: Preparing the data for analysis by handling missing values and 
# removing irrelevant columns.
#
# Approach:
# - The data is first loaded from the 'sales_data.csv' file.
# - Missing or null values are handled by filling them with appropriate substitutes 
# (e.g., using the median or mode for numerical data).
# - Unnecessary or irrelevant columns (such as customer IDs or sales IDs) are 
# removed to focus on the essential attributes that impact sales analysis.
# - The final cleaned data is stored in the '02_data_clean' folder to ensure it is 
# ready for analysis and further processing.

# 2. Timeframe-Based Grouping
# Objective: Grouping data by time-related variables (Year, Month, Weekday, Hour) 
# to analyze sales patterns over time.
#
# Approach:
# - The data is grouped by various timeframes such as Year, Month, Weekday, and Hour 
# to observe how sales change during different periods.
# - Aggregations are performed to calculate the total sales for each group, which 
# helps identify trends and seasonal behaviors.
# - This analysis enables the identification of peak sales times, the best months for 
# business growth, and the days with the highest activity.

# 3. Correlation Between Product Categories
# Objective: Identifying relationships between different product categories to 
# understand cross-selling opportunities.
#
# Approach:
# - A correlation matrix is created based on the sales data for different product 
# categories (e.g., M01AB, M01AE, etc.).
# - The correlation matrix is calculated to find which products tend to be bought 
# together, revealing patterns of co-purchase behavior.
# - A heatmap is generated using sns.heatmap() to visualize these correlations. 
# Strong correlations are highlighted with warmer colors, and weaker ones are shown 
# with cooler colors.
# - This heatmap helps businesses identify potential bundling opportunities or areas 
# for cross-selling strategies, allowing them to increase sales by targeting product 
# combinations.

# 4. Moving Average of Total Sales (by Month)
# Objective: Smoothing out short-term fluctuations in sales data to identify long-term 
# trends.
#
# Approach:
# - The total sales for each month are first calculated, then a 3-month moving 
# average is computed.
# - This technique helps to smooth out fluctuations in the sales data and emphasizes 
# the overall trend, which could be affected by seasonal changes or long-term growth.
# - A line plot is created to display the raw monthly sales alongside the moving average, 
# providing a clearer view of underlying trends while filtering out noise in the data.

# 5. Sales by Weekday and Hour
# Objective: Analyzing which days of the week and times of the day are the most 
# profitable.
#
# Approach:
# - The data is grouped by both weekday_name and hour, and the average sales for 
# each combination are calculated.
# - The result is then transformed into a matrix, where rows represent weekdays, 
# columns represent hours, and the values show the average sales during each timeframe.
# - A heatmap is used to visualize this matrix, with color intensity representing 
# the level of sales (dark blue for high sales, yellow for low sales).
# - This analysis allows businesses to identify peak sales times and optimize marketing 
# campaigns, staffing, and inventory management for high-performing hours or days.

# 6. Data Visualization
# Objective: Creating visualizations to present the findings in an easily understandable 
# format.
#
# Approach:
# - Several visualizations are generated using matplotlib and seaborn to illustrate 
# key insights from the data.
# - A variety of charts such as line plots, bar charts, and heatmaps are used to 
# present the correlation between product categories, sales trends, and peak sales times.
# - These visualizations help convey insights in a visual format that is accessible 
# and actionable for decision-makers.

# Conclusion:
# This code provides a comprehensive analysis of sales data, helping the pharmaceutical 
# company understand trends in customer behavior, identify high-performing sales periods, 
# and find correlations between products. The insights gained through this analysis can 
# be used to improve sales strategies, optimize marketing efforts, and make more informed 
# business decisions to drive growth.








