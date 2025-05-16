# Import the libraries we need

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the cleaned dataset
# Here, I'm using the pd.read_csv() function to load the cleaned sales data from the 
# file 'sales_data_clean.csv' into a DataFrame called 'df'. 
# The file is in the '02_data_clean' folder. 
# Now, 'df' will hold the data, and I can start working with it in Python.

df = pd.read_csv("02_data_clean/sales_data_clean.csv")

# Step 1: Checking the columns of the dataset
# To understand the structure of the dataset and know which columns are related to products and time,
# I opened a separate Python file for exploratory work. This keeps things clean and organized.

# In that file, I used the following code:
# print(df.columns.tolist()) 
# This code shows a list of all the column names in the dataset.

# By looking at these column names, I was able to figure out which ones were related to product 
# categories (like 'm01ab', 'n02ba', etc.) and which ones were related to time 
# (like 'year', 'month', 'hour', 'weekday_name').
# By putting all the products columns in 'product_columns', I'll be able to perform further advanced 
# analysis of the data by creating charts.

product_columns = ['m01ab', 'm01ae', 'n02ba', 'n02be', 'n05b', 'n05c', 'r03', 'r06']

# I'll create a new column called 'total_sales' to sum all sales for each row. 
# This will represent the total daily/hourly sales.
# By running the code df['total_sales'] = df[product_columns].sum(axis=1),
# df['total_sales'] creates a new column, and df[product_columns].sum(axis=1) 
# sums all the sales for each row, placing the result in 'total_sales'.
# The axis=1 ensures the sum happens row by row, adding up the sales for each 
# individual entry.

df['total_sales'] = df[product_columns].sum(axis=1)

# Monthly Sales Trends — Are there any seasonal patterns?
# I'm checking if sales go up or down in certain months every year.
# Do some months always have high or low sales? Are there patterns that repeat every year?

# First, I group the data by 'year' and 'month' to make monthly sales data easier to analyze.
# For example, if January had sales of 200, 50, and 100 on different days (like 1 = 200 , 1 = 50 , 1 = 100),
# this will combine them into one row for January with total sales = 350 (1 = 350 in the dataset).

# I use this code:
# monthly_sales = df.groupby(['year', 'month'])['total_sales'].sum().reset_index()
# This gives me total sales for each month of each year.
# When I use groupby(), the 'year' and 'month' columns become part of the rows (index),
# instead of being regular columns.
# By using .reset_index(), I turn them back into normal columns, making the table easier to work with.
#
# For example, after grouping, it looks like this:
#                   total_sales
# year  month               
# 2022     1              250
# 2022     2              400
#
# Here, 'year' and 'month' are now part of the rows (index), not the column headers.
# After using reset_index(), it looks like this again:
#   year   month   total_sales
#   2022     1           250
#   2022     2           400
#
# Now 'year' and 'month' are back as normal column headers, making the table easier to read.

monthly_sales = df.groupby(['year', 'month'])['total_sales'].sum().reset_index()

# Pivot the data to get years as rows and months as columns (for easier plotting)
# In this step, I am pivoting (reorganizing or rearranging) the data to make it easier to visualize.
# I use this code:
# monthly_sales.pivot(index='year', columns='month', values='total_sales')

# Here’s what each part of the code does:
# - index='year': This sets the 'year' as the rows (the X-axis for the chart).
# - columns='month': This sets the 'month' as the columns (the Y-axis for the chart).
# - values='total_sales' will place the total sales values inside the table, 
# where the year and month meet, showing the total sales for each month of each year.




monthly_pivot = monthly_sales.pivot(index='year', columns='month', values='total_sales')

# Plot the monthly trends to see if there’s a seasonal pattern

# Here, I'm creating a line plot to show the trends (ups and downs) and seasonality of sales over time.
# A line plot is ideal for this because it clearly shows how values change across months and years.
# That's why I chose it instead of something like a heatmap.

# Now here's what this code does:
# monthly_pivot.plot will create the plot.
# kind='line' means it will be a line plot.
# marker='o' adds small circles at each data point to make the trend easier to see.
# figsize=(12, 6) sets the width to 12 inches and the height to 6 inches.
# title='Monthly Sales Trends' adds a title to the chart.

monthly_pivot.plot(kind='line', marker='o', figsize=(12, 6), title='Monthly Sales Trends')

# This sets 'Total Sales' as the label on the Y-axis (vertical axis).
plt.ylabel('Total Sales')

# This sets 'Year' as the label on the X-axis (horizontal axis).
plt.xlabel('Year')

# This rotates the X-axis labels by 45 degrees to avoid overlapping and make them easier to read.
plt.xticks(rotation=45)

# This ensures that nothing gets cut off in the plot (labels, title, etc.).
plt.tight_layout()

# This saves the plot as an image in the '04_outputs' folder.
plt.savefig('04_outputs/monthly_sales_trends.png')

# Finally, this shows the plot on the screen.
plt.show()





# Which product categories are selling the most overall?

# Here, I'm summing up the sales for each product column across the entire dataset.
# df[product_columns] selects all the product columns (like M01AB, M01AE, etc.).
# .sum() adds up the sales of each product over all rows (up to down, each row of each individual column).
# (i.e., total sales per product). .sort_values(ascending=False) sorts the total sales from highest 
# to lowest. The result is stored in total_product_sales , showing which products sold the most overall.

# 📌 Why this step is important:
# This gives me a clear picture of product-level performance — which products generate the most revenue.
# It's helpful for identifying top-selling and low-selling products so the company can
# make better business decisions.

total_product_sales = df[product_columns].sum().sort_values(ascending=False)

# Bar plot of top-selling product categories

# I am creating a bar plot to visualize the top 10 best-selling products.
# A bar plot is ideal for comparing sales across categories and shows the top performers clearly.
# I chose a bar plot because it makes comparing sales easy, while a line plot or heatmap might
# not highlight the comparison as well.

# Now, I'll plot the top 10 products.
# .head(10) gives me the top 10 products with the highest sales.
total_product_sales.head(10).plot(kind='bar', figsize=(10, 6), title='Top 10 Best-Selling Products')

# This sets 'Total Sales' as the label for the Y-axis (vertical axis), indicating that the height of each bar represents total sales for each product.
plt.ylabel('Total Sales')

# This sets 'Product Category' as the label for the X-axis (horizontal axis), representing the different product categories.
plt.xlabel('Product Category')

# This adjusts the layout to ensure everything fits neatly within the plot, avoiding any overlapping or cut-off elements.
plt.tight_layout()

# This saves the plot as an image in the '04_outputs' folder under the name 'top_10_products.png'.
plt.savefig('04_outputs/top_10_products.png')

# Finally, this displays the plot on the screen, allowing me to visually inspect the bar chart.
plt.show()







# Here's the code breakdown:
# total_product_sales.head(10) selects the top 10 products by total sales.
# .plot(kind='bar') creates the bar plot, where the height of each bar shows the total sales.
# figsize=(10, 6) sets the plot's size (10 inches wide, 6 inches tall).
# title='Top 10 Products by Sales' adds a title to the chart.

total_product_sales.head(10).plot(kind='bar', figsize=(10, 6), title='Top 10 Products by Sales')

# plt.ylabel('Total Sales') sets the Y-axis label to show sales amounts.
plt.ylabel('Total Sales')

# plt.xlabel('Product Category') labels the X-axis with product categories.
plt.xlabel('Product Category')

# plt.tight_layout() ensures everything fits within the plot without overlap.
plt.tight_layout()

# plt.savefig('04_outputs/top_10_products.png') saves the plot as an image.
plt.savefig('04_outputs/top_10_products.png')

# plt.show() displays the plot on the screen.
plt.show()

# Analyze sales by weekday to see if some days perform better than others

# Here, I'm grouping the dataset by the 'weekday_name' column (like Monday, Tuesday, etc.).
# For each weekday, I'm summing up the total sales using the 'total_sales' column.
# This helps me understand which days of the week have the highest overall sales.
# It's useful for identifying busy or slow days, which can help with marketing and staffing decisions.
# By running this code weekday_sales = df.groupby('weekday_name')['total_sales'].sum(), I will get the 
# total sales for each of the 7 weekdays (Monday through Sunday) across the entire span of the dataset.
# This allows me to analyze the sales performance on each weekday, which can help identify patterns like 
# whether some days consistently perform better than others.
# It's similar to the earlier step where I grouped data by month, but here I am focusing on weekdays 
# instead of months. This helps in understanding how sales fluctuate throughout the week.

weekday_sales = df.groupby('weekday_name')['total_sales'].sum()

# Reorder days to make the plot easier to read
# This step ensures that the days of the week appear in a logical order (Monday to Sunday) on the plot.
# If I don’t reorder, pandas might display the days alphabetically, which is not ideal for 
# understanding weekly trends.
# First, I'll create a list of weekdays in the order I want them to appear on the plot: Monday to Sunday.
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']





# Now, I use the 'reindex' function to reorder the 'weekday_sales' data to match the order
# in the 'ordered_days' list that I made.
# By running this code weekday_sales.reindex(ordered_days), the data of weekdays' total sales will appear
# in the correct sequence (from Monday to Sunday).

weekday_sales = weekday_sales.reindex(ordered_days)  
  
# Plot weekday performance
# In this step, I am creating a bar plot to visualize how the sales perform on each day of the week.
# A bar plot is a good choice because it helps to compare the total sales of each day clearly.
# I want to understand which day of the week brings in the most sales and which day performs poorly.

# weekday_sales.plot will generate the plot.
# kind='bar' tells Python that I want to create a bar plot.
# figsize=(10, 6) sets the plot size, making sure it’s wide enough and tall enough to see clearly.
# title='Sales by Weekday' gives the chart a title, so it’s clear what the plot is showing.
# color='skyblue' sets the color of the bars in the chart to a light blue shade for better visibility.

weekday_sales.plot(kind='bar', figsize=(10, 6), title='Sales by Weekday', color='skyblue')

# This sets 'Total Sales' as the label for the Y-axis (vertical axis). 
# It tells me that the height of the bars represents the total sales for each day.
plt.ylabel('Total Sales')

# This sets 'Weekday' as the label for the X-axis (horizontal axis). 
# It shows the days of the week (Monday to Sunday) along the bottom of the chart.
plt.xlabel('Weekday')

# This ensures that everything fits nicely within the chart. 
# It helps prevent labels, title, or other elements from being cut off or crowded.
plt.tight_layout()

# This saves the plot as an image in the '04_outputs' folder. 
# The file will be named 'sales_by_weekday.png' so I can keep it for reporting or future analysis.
plt.savefig('04_outputs/sales_by_weekday.png')

# Finally, this displays the plot on the screen so I can visually inspect the chart.
plt.show()

# Grouping the dataset by the 'hour' column and summing the 'total_sales' for each hour.
# This step calculates the total sales for each hour of the day across the entire dataset.
# The 'groupby' function groups all rows with the same hour value together.
# Then, the 'sum' function adds up the total sales for each hour.

# This step is similar to how we group the data by 'month' or 'weekday' — it’s just focusing on
# on hourly data.









# By running this code, 'hourly_sales' will contain the total sales per hour across the entire dataset.
# For example, if sales were recorded at 08:00, 09:00, 10:00, etc., 
# the total sales for each hour will be calculated and stored in 'hourly_sales'.

hourly_sales = df.groupby('hour')['total_sales'].sum()

# The following code creates a line plot to visualize the total sales per hour of the day.
# This helps me understand how sales fluctuate throughout the day, and whether certain hours 
# perform better than others.
# 'hourly_sales.plot(kind='line')' creates a line plot.
# The 'kind='line'' specifies that I want a line plot, which is suitable for showing trends over time
# (in this case, hourly sales).

# figsize=(10, 6) sets the size of the plot, making it 10 inches wide and 6 inches tall.
# This ensures the plot is large enough to read and visually appealing, fitting well on most screens.

# title='Sales by Hour of Day' sets the title of the plot to "Sales by Hour of Day," which will be
# displayed at the top of the chart. This title gives a clear indication of what the plot represents:
# the total sales for each hour.

# marker='o' adds circular markers to each data point in the line plot. This makes it easier to see
# individual sales values for each hour, which helps to better understand the trend.

# plt.ylabel('Total Sales') adds a label to the Y-axis, which represents the total sales for each hour.
# The Y-axis will show how much money was made during each hour of the day.

# plt.xlabel('Hour of Day') adds a label to the X-axis, which represents the hours of the day.
# The X-axis will show each hour from 0 (midnight) to 23 (11 PM), with the sales data plotted accordingly

# plt.grid(True) adds a background grid (horizontal and vertical lines) to the plot. TRUE means turn the
# grid on.
# This grid makes it easier to read the exact values from the graph,
# especially when comparing data points across hours.
# It helps the viewer clearly see which hour each point on the line belongs to,
# and what the exact sales value is by aligning the data point with both the X-axis (hour)
# and Y-axis (sales).
# Without the grid, it can be confusing — for example, you might not be sure
# if a point belongs to hour 5 or hour 6, or if the value is 300 or 350.

# Create the line plot for hourly sales
hourly_sales.plot(kind='line', figsize=(10, 6), title='Sales by Hour of Day', marker='o')

# Labeling the Y-axis to indicate that the values represent total sales.
plt.ylabel('Total Sales')

# Labeling the X-axis to indicate that the values represent hours of the day.
plt.xlabel('Hour of Day')

# Turn on grid for better readability of the plot.
plt.grid(True)

# Adjust the layout to make sure everything fits without overlap.
plt.tight_layout()

# Save the plot as an image in the '04_outputs' folder.
plt.savefig('04_outputs/sales_by_hour.png')

# Display the plot for inspection.
plt.show()














