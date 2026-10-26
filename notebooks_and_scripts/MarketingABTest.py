import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import urllib


# Re-establish connection
# The Engineering Foundation: Establish Secure Database Connection.
params = urllib.parse.quote_plus(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=localhost\\SQLEXPRESS;' # Use your server name
    r'DATABASE=MarketingABTest;'
    r'Trusted_Connection=yes;'
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# 1. Connect to your local SQL Server instance (SSEXPRESS)
# (Make sure 'YourDatabaseName' matches the database name you created earlier!)
engine = create_engine(
    "mssql+pyodbc://@localhost\\SQLEXPRESS/MarketingABtest"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# 2. Pull your data directly into 'df' using SQL!
query = "SELECT * FROM campaign_results"
df = pd.read_sql(query, con=engine)

print("Data successfully loaded from SQL Server! Total rows:", len(df))



# # 2. Ask SQL Server to list all available tables for us!
# query_check = (
#     "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE"
#     " TABLE'"
# )
# tables_df = pd.read_sql(query_check, con=engine)
# print("Here are the actual tables in your database:")
# print(tables_df)



# TASK: Find the average number of ads seen by people who converted vs those who didn't
# query = """
# SELECT 
#     converted, 
#     AVG(total_ads) as avg_ads_seen,
#     COUNT(*) as user_count
# FROM campaign_results
# GROUP BY converted
# """

# verification_df = pd.read_sql_query(query, engine)
# print(verification_df)

# Task: Get the Top 10 users who saw the most ads
query = """
SELECT TOP 10 
    user_id, 
    total_ads, 
    converted, 
    most_ads_day
FROM campaign_results
ORDER BY total_ads DESC;
"""
df=pd.read_sql_query(query, engine)
print("Query to find the top 10 users who saw the most ads:")
#pd.set_option('display.max_columns', None)  # Show all columns
#pd.set_option('display.width', 1000)  # Adjust display width
print(df)

# top_ads_df = pd.read_sql_query(query, engine)
# print("--- THE TOP 10 AD CONSUMERS ---")
# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.width', 1000)  # Adjust display width
# print(top_ads_df) 

# task: Compare the conversion rate of the 'ad' group vs the 'psa' group
# query = """
# SELECT 
#     test_group,
#     COUNT(*) as total_users,
#     SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) as total_conversions
# FROM campaign_results
# GROUP BY test_group;

# """

# ab_results = pd.read_sql_query(query, engine)

# # Calculate conversion rates percentages
# ab_results['conversion_rate'] = (ab_results['total_conversions'] / ab_results['total_users']) * 100

# print("--- A/B TEST RESULTS ---")
# print(ab_results) 

# SQL Query using  NTILE or CASE to create buckets of users based on the number of ads seen, and then calculate the conversion rate for each bucket
# query = """
# SELECT 
#     CASE
#         WHEN total_ads <= 5 THEN '1-5'
#         WHEN total_ads <= 10 THEN '6-10'
#         WHEN total_ads <= 20 THEN '11-20'
#         WHEN total_ads <= 50 THEN '21-50'
#         ELSE '50+ ads'
#     END AS ad_exposure_bucket,
#     COUNT(*) AS total_users,
#     SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS total_conversions
# FROM campaign_results
# WHERE test_group = 'ad' -- we only care about people who actually saw ads
# GROUP BY 
#     CASE 
#         WHEN total_ads <= 5 THEN '1-5'
#         WHEN total_ads <= 10 THEN '6-10'
#         WHEN total_ads <= 20 THEN '11-20'
#         WHEN total_ads <= 50 THEN '21-50'
#         ELSE '50+ ads'
#     END
# ORDER BY MIN(total_ads);
# """

# df_efficiency =pd.read_sql_query(query, engine)
# df_efficiency['conversion_rate_%'] = (df_efficiency['total_conversions'] /  df_efficiency['total_users']) * 100

# print("--- AD EFFICIENCY (FATIGUE) REPORT ---")
# print(df_efficiency[['ad_exposure_bucket', 'total_users', 'total_conversions', 'conversion_rate_%']]) 


# the "TIMING" analysis (THE GOLDEN HOURS)Query to find conversion rate by hour. 
# query = """
# SELECT 
#     most_ads_hour,
#     COUNT(*) AS total_users,
#     SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS total_conversions
# FROM campaign_results
# GROUP BY most_ads_hour
# ORDER BY most_ads_hour;
# """
# df_timing = pd.read_sql_query(query, engine)
# df_timing['conversion_rate_%'] = (df_timing['total_conversions'] / df_timing['total_users']) * 100

# #Let's find top 3 hours with the highest conversion rates.
# top_3_hours = df_timing.sort_values(by='conversion_rate_%', ascending=False).head(3)

# print("\n--- THE GOLDEN HOURS---")
# print(top_3_hours) 


# 2. SQL Query to get day, hour, and conversion rate. The Heatmap will show us which day/hour combinations have the highest conversion rates.
# query = """
# SELECT 
#     most_ads_day,
#     most_ads_hour,
#     CAST(SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS FLOAT) / COUNT (*) * 100 AS conv_rate
# FROM campaign_results
# GROUP BY most_ads_day, most_ads_hour

# """
# df_heat=pd.read_sql_query(query, engine)
# # 3. Pivot the data so days are rows, hours are columns, and conversion rates are values. Also, need to ensure the days follow a logical order (Monday, Tuesday, etc.) and hours are in 24-hour format.

# day_order =['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# pivot_table = df_heat.pivot(index='most_ads_day', columns='most_ads_hour', values='conv_rate')
# pivot_table = pivot_table.reindex(day_order)

# # 4. Create the heatmap using Seaborn.
# plt.figure(figsize=(15, 8))
# sns.heatmap(pivot_table, annot=False, cmap='YlGnBu', cbar_kws={'label': 'Conversion Rate (%)'})

# plt.title('The marketing Heatmap: Best Time to Show Ads', fontsize=16)
# plt.xlabel('Hour of Day (24hr format)', fontsize=12)
# plt.ylabel('Day of the Week', fontsize=12)

# plt.show() 

# Task: find the day with worst 'ads-to-conversion' ratio.
# query_efficiency = """
# SELECT 
#     most_ads_day,
#     SUM(total_ads) AS total_ads_shown,
#     SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS total_conversions,
#     CAST(SUM(total_ads) AS FLOAT) / NULLIF(SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END), 0) AS ads_per_sale 
# FROM campaign_results
# WHERE test_group = 'ad'
# GROUP BY most_ads_day
# ORDER BY ads_per_sale DESC;
# """

# df_low_eff = pd.read_sql_query(query_efficiency, engine)
# print("--- AD EFFiCIENCY BY DAY ( HIGHEST 'Ads per Sale' is worst) ---") 
# print(df_low_eff)

# using the ab_results dataframe we created earlier to visualize the A/B test results with a bar chart.
# plt.figure(figsize=(8, 6))
# sns.barplot(x='test_group', y='conversion_rate', data=ab_results, palette='viridis') 

# plt.title('Ad Group vs. PSA Group: Conversion Rates', fontsize=14) 
# plt.ylabel('Conversion Rate (%)',) 
# plt.show() 

# Pull a sample for the histogram (plotting 600k points is slow 50k is enough to see the distribution) 
# query_dist = "SELECT TOP 50000 total_ads FROM campaign_results WHERE test_group = 'ad'" 
# df_dist = pd.read_sql_query(query_dist, engine) 

# plt.figure(figsize=(10, 6)) 
# # we use a log scale because some people saw 2000 ads while most saw 10. 
# sns.histplot(df_dist['total_ads'], bins=50, kde=True, color='purple') 
# plt.xscale('log') 

# plt.title('Distribution of Ad Exposure (log Scale)', fontsize=14) 
# plt.xlabel('Number of Ads Seen')
# plt.ylabel('Number of Users')
# plt.show() 


# We pull a sample to keep the plot clean.

# query_box =""" 
# SELECT TOP 20000 total_ads, converted 
# FROM campaign_results 
# WHERE test_group = 'ad'
# """

# df_box = pd.read_sql_query(query_box, engine) 

# plt.figure(figsize=(10, 6))
# # again using log scale because of the high exposure outliers.
# sns.boxplot(x='converted', y='total_ads', data=df_box, hue='converted', palette='Set2') 
# # Log scale is crucial because of the 'Whales'.
# plt.yscale('log') 

# plt.title('Ad Exposure Distribution: Converted vs Not Converted', fontsize=14) 
# plt.xlabel('Did they Converted')
# plt.ylabel('Number of Ads Seen (log scale)') 
# plt.show() 


# 1. SQL Query: Get raw counts per hour for both groups. 
# query_time_split = """
# SELECT 
#     converted, 
#     most_ads_hour,
#     COUNT(*) AS user_count
# FROM campaign_results
# GROUP BY converted, most_ads_hour
# ORDER BY converted, most_ads_hour;
# """

# df_time = pd.read_sql_query(query_time_split, engine) 

#NEW CODE:
# print("Unique values in 'converted' column:", df_time['converted'].unique())
# print("Data type of converted' column:", df_time['converted'].dtype) 


# 2. The Robust Calculation Logic.
# We group by 'converted' and find the sum of 'user_count' for each group.
# transform('sum') creates a column of totals aligned with our rows.
# df_time['group_total'] = df_time.groupby('converted')['user_count'].transform('sum') 

#Calculate percentage. We add a tiny 'epsilon' (1e-9) to avoid 0 division just in case.
# df_time['pct_of_group'] = (df_time['user_count'] / df_time['group_total'] * 100) 

# 3. 
#------------------------------------------------------
#OLD CODE:
# 2. professor's logic: Normalize the data.
# We find the total number of people in the 'True' group and 'false' group.
# total_true = df_time[df_time['converted'] == 'True']['user_count'].sum() 
# total_false = df_time[df_time['converted'] == 'False']['user_count'].sum()

# Create a new column for 'percentage of group'
# df_time['pct_of_group'] = df_time.apply(
#     lambda x: (x['user_count'] / total_true * 100) if x['converted'] == 'True'
#     else (x['user_count'] / total_false * 100), axis=1
# ) 
#------------------------------------------------------


# # 3. Visualisation: The Overlapping Line Plot.
# plt.figure(figsize=(12, 6))
# # We use 'hue' to automatically split the lines by the 'converted' status.
# sns.lineplot(data=df_time, x='most_ads_hour', y='pct_of_group', hue='converted', marker='o')

# plt.title('Daily Routine: Buyers vs. Browser (Normalized)', fontsize=14) 
# plt.xlabel('Hour of day (24hr format)')
# plt.ylabel('% of Group Active at this Hour') 
# plt.xticks(range(0, 24))
# plt.grid(True, linestyle='--', alpha=0.3) 

# plt.show() 

#--------------------------------------------------------
# Professor's Drill-down Query
# query_saturday_vs_monday = """
# SELECT 
#     most_ads_day, 
#     most_ads_hour, 
#     CAST(SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as conv_rate
# FROM campaign_results
# WHERE most_ads_day IN ('Monday', 'Saturday')
# GROUP BY most_ads_day, most_ads_hour
# """

# df_drill = pd.read_sql_query(query_saturday_vs_monday, engine)

# plt.figure(figsize=(12, 6))
# sns.lineplot(data=df_drill, x='most_ads_hour', y='conv_rate', hue='most_ads_day', palette='Set1', marker='o')

# plt.title('Battle of the Days: Monday (Efficiency) vs. Saturday (Gems)', fontsize=14)
# plt.ylabel('Conversion Rate (%)')
# plt.xticks(range(0, 24))
# plt.grid(True, alpha=0.3)
# plt.show() 

# Query to pulling both Rate And Volume
# query_volume_check = """
# SELECT 
#     most_ads_day,
#     most_ads_hour,
#     COUNT(*) AS total_traffic,
#     SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS total_conversions,
#     CAST(SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS conversion_rate_pct
# FROM campaign_results
# WHERE most_ads_day IN ('Monday', 'Saturday')
# GROUP BY most_ads_day, most_ads_hour
# ORDER BY most_ads_hour, most_ads_day;
# """

# #Execute and view the dataframe
# df_volume = pd.read_sql_query(query_volume_check, engine)

# #let's filter specifically for the 5 AM and 3 PM windows to compare directly.
# print("---TARGETED HOUR DRILL-DOWN---") 
# print(df_volume[df_volume['most_ads_hour'].isin([5, 15])].to_string(index=False))


# 2. The Analytical Core: High-Level Aggregation Query.
# query_final_summary = """
# SELECT 
#     test_group, 
#     COUNT(*) as total_audience,
#     SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) as total_conversion,
#     CAST(SUM(CASE WHEN converted = 'True' THEN 1 ELSE 0 END) as FLOAT) / COUNT(*) * 100 as conversion_rate_pct 
# FROM campaign_results
# GROUP BY test_group;
# """ 

# # 3. Extract and Transform
# df_summary = pd.read_sql_query(query_final_summary, engine) 

# # 4. Business logic Layer: Financial Impact Modeling 
# # Assign an estimated Average Order Value (AOV) of $50 per transaction
# AVERAGE_ORDER_VALUE = 50.00
# df_summary['estimate_revenue'] = df_summary['total_conversion'] * AVERAGE_ORDER_VALUE

# # 5. Output Layer: Human_Readable Execution Presentation
# print("==================================================================")
# print("                FINAL EXECUTIVE PORTFOLIO SUMMARY                 ")
# print("==================================================================")
# print(df_summary.to_string(index=False, formatters={
#     'total_audience': '{:,}'.format,
#     'total_conversions': '{:,}'.format,
#     'conversion_rate_pct': '{:.3f}%'.format,
#     'estimated_revenue': '${:,.2f}'.format
# }))
# print("==================================================================")

# focused more on Scipy and Numpy and learning.

# Quick structural check: print column names so we see what we're working with
# print("\n--- 2. Dataset Columns ---")
# print(df.columns.tolist())

# print("\n--- 3. Running SciPy Statistical Analysis ---")
# # NOTE: Make sure 'test_group' and 'converted' match your actual column names from above!
# if "test_group" in df.columns and "converted" in df.columns:
#   # Build contingency table for Chi-Square Test of Independence
#   contingency_table = pd.crosstab(df["test_group"], df["converted"])
#   print("\nContingency Table:")
#   print(contingency_table)

#   # Execute Chi-Square Test
#   chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)

#   print(f"\nChi-Square Statistic : {chi2_stat:.4f}")
#   print(f"p-value              : {p_val:.4e}")

#   # Business Verdict
#   if p_val < 0.05:
#     print(
#         "RESULT: Statistically Significant! (p < 0.05) The ad campaign drove a"
#         " genuine conversion lift."
#     )
#   else:
#     print(
#         "RESULT: Not Significant. Differences between groups could be random"
#         " chance."
#     )
# else:
#   print(
#       "Notice: Check your column names above and update 'test_group' or"
#       " 'converted' if needed."
#   )