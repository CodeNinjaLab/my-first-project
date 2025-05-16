# Importing the essential library to work with data

import pandas as pd

# Load the raw sales dataset
# I'm loading the raw sales data from a CSV file (sales_data.csv) into a DataFrame
# called df. This will allow me to manipulate and clean the data.
# I used read_csv for pandas to know that it is reading a CSV file. There are many
# types of files, and if I don't specify the type, it won't work.
# 'df' is the variable I have created here.
# Now, by doing pd.read_csv('sales_data.csv'), I have loaded the dataset that I
# downloaded from Kaggle, and it has been converted into a dataset using pandas.

df = pd.read_csv('sales_data.csv')

# Step 1: Handle missing values
# First, I’ll check if there are any missing values in the dataset.
# I'm using df.isnull() to check how many empty values there are. Pandas has already
# marked them as NaN, and it will mark the empty values as TRUE and the non-empty
# values as FALSE when ill give command to sum them thats how it will sum them true = 1 , false = 0.
# By doing df.isnull().sum(),it will tell me the total count of missing values in
# the entire dataset.

missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values)

# Dropping rows with missing values
# By using df.dropna(), all the rows with empty values will be dropped and will not
# be part of the dataset for analysis.
# I dropped the rows with missing values to ensure the analysis is based on complete
# data.
# I chose to drop rows with missing values because the percentage of rows with missing
# values is relatively low across the dataset.
# To determine this, I checked the number of missing values per row and calculated the
# percentage.
# I calculated the percentage of rows missing by using missing_rows = df.isnull().any(axis=1).sum()
# this gave me the total number of  rows which had atleast one missing value. Then, I used df.shape[0] to get the total number of
# rows from the dataset. Then I applied the percentage formula.
# I did this all in another Python file made right next to this one. I wanted my code to
# be accurate and to the point, which is why I chose not to include it.
# Removing these rows won't significantly impact the analysis or lead to biased results.
# If more than 5% of the rows in the dataset had missing values, I would have considered
# alternative methods like filling missing values.

df = df.dropna()  

# Step 2: Correct data types
# The 'datum' column should be in a date format, so I'll convert it to a datetime object.
# Over here, the df has my original dataset's date column under the 'datum' column.
# By running pd.to_datetime(df['datum']), the dates under the 'datum' column get
# formatted into a format that pandas can read.

df['datum'] = pd.to_datetime(df['datum'])

# Step 3: Remove duplicates
# I want to make sure there are no duplicate rows, so I’ll clean them up.
# Over here, by running df.drop_duplicates(), I drop all the rows that are exactly the
# same, keeping only the first row.
# I do this for accurate analysis. The other duplicate rows might have been mistakenly
# created, so I removed them to make sure that each row in my dataset represents unique
# data.

df = df.drop_duplicates()

# Step 4: Standardize Column Names
# I’ll clean up the column names to make them easier to work with by making them
# lowercase and replacing spaces with underscores.
# Over here, I convert all the column headers to lowercase so pandas can read them
# accurately and not make errors.
# Similarly, I replace the empty space between words with underscores to avoid any
# errors, as pandas reads them with underscores more easily.

df.columns = df.columns.str.lower().str.replace(' ', '_')

# Save the cleaned data to a new file
# I’ll save the cleaned dataset into a new file so I don’t overwrite the original one.
# Over here, df.to_csv() converts the dataset in df to a CSV file, which I can load
# later as a cleaned dataset for further analysis or share with others if needed.
# '02_data_clean/sales_data_clean.csv' is the path where the CSV file will be stored
# on my laptop. '02_data_clean/' is the name of the folder, and 'sales_data_clean.csv'
# will be the name of the file.
# I have set index=False because pandas, by default, keeps it as TRUE.
# By setting it to False, my dataset will be stored as it is after being cleaned.
# Otherwise, pandas would assign row numbers starting from 0 to 2000. I didn’t want that.

df.to_csv('02_data_clean/sales_data_clean.csv', index=False)

# Display the cleaned dataset
# Finally, the dataset has been cleaned. Now I am going to display its output.

print("\nCleaned dataset:")
print(df.head())