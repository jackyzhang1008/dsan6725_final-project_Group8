# Channel week 1 - Introduction to Big Data

## Thread: Pandas Memory Issues
**Jordan_Lee** [2025-03-01 2:15 PM]  
I'm trying to load the NYC TLC dataset for January 2023 using pandas, but I keep getting a memory error. My code is:
```python
import pandas as pd
df = pd.read_csv('yellow_tripdata_2023-01.csv')
```
My laptop has 8GB RAM. Any suggestions?

**TA_Wong** [2025-03-01 2:20 PM]  
@Jordan_Lee The full NYC TLC dataset is quite large! Try using the `chunksize` parameter:
```python
chunks = pd.read_csv('yellow_tripdata_2023-01.csv', chunksize=100000)
# Then you can process each chunk separately
for chunk in chunks:
    # Process the chunk
    print(chunk.shape)
```

**Jordan_Lee** [2025-03-01 2:25 PM]  
@TA_Wong That worked! Now I'm able to process the data in smaller chunks. What's the best way to combine results from all chunks?

**TA_Wong** [2025-03-01 2:32 PM]  
@Jordan_Lee It depends on what you're trying to do. If you need aggregate statistics, you can compute them incrementally:
```python
total_count = 0
sum_fare = 0
for chunk in chunks:
    total_count += len(chunk)
    sum_fare += chunk['fare_amount'].sum()
average_fare = sum_fare / total_count
```

**Prof_Martinez** [2025-03-01 2:40 PM]  
@Jordan_Lee @TA_Wong Good discussion! This is exactly why we need big data tools. For week 1, we're using pandas to understand the limitations of single-machine processing. In future weeks, we'll look at distributed computing with Spark which handles these datasets more naturally.

**Jordan_Lee** [2025-03-01 2:45 PM]  
@Prof_Martinez @TA_Wong Thanks! Looking forward to learning Spark!

## Thread: Pandas DataFrame Manipulation
**Aisha_Patel** [2025-03-02 10:05 AM]  
I'm trying to filter the Amazon product reviews dataset to only include reviews with 4 or 5 stars, but my code isn't working:
```python
filtered_df = amazon_df[amazon_df.stars >= 4]
```
I'm getting a KeyError: 'stars'

**Jamie_Rodriguez** [2025-03-02 10:12 AM]  
@Aisha_Patel Can you share what columns are in your dataframe? You can use `amazon_df.columns` to check.

**Aisha_Patel** [2025-03-02 10:15 AM]  
@Jamie_Rodriguez Here's what I get:
```
Index(['marketplace', 'customer_id', 'review_id', 'product_id', 'product_parent',
       'product_title', 'product_category', 'star_rating', 'helpful_votes',
       'total_votes', 'vine', 'verified_purchase', 'review_headline',
       'review_body', 'review_date'],
      dtype='object')
```

**Jamie_Rodriguez** [2025-03-02 10:20 AM]  
@Aisha_Patel I see the issue! The column is called 'star_rating' not 'stars'. Try:
```python
filtered_df = amazon_df[amazon_df.star_rating >= 4]
```

**Aisha_Patel** [2025-03-02 10:23 AM]  
@Jamie_Rodriguez That worked! Thank you so much!

**TA_Patel** [2025-03-02 10:30 AM]  
@Aisha_Patel Just a quick tip: I find it helpful to always check `.head()` and `.info()` when working with a new dataset, especially public ones like the Amazon reviews, as column names can sometimes be different than expected:
```python
print(amazon_df.head())
print(amazon_df.info())
```

**Aisha_Patel** [2025-03-02 10:35 AM]  
@TA_Patel Thanks for the tip! That's a good habit to develop.

## Thread: Pandas Time Series Analysis
**Marcus_Brown** [2025-03-03 3:45 PM]  
I'm trying to analyze ride patterns in the NYC TLC data by hour of day, but I'm having trouble converting the 'tpep_pickup_datetime' column to datetime. Here's my code:
```python
df['pickup_time'] = pd.to_datetime(df['tpep_pickup_datetime'])
```
But I'm getting an error: "ValueError: Unknown string format"

**TA_Wong** [2025-03-03 3:52 PM]  
@Marcus_Brown Can you share the first few values from the 'tpep_pickup_datetime' column? You can use:
```python
print(df['tpep_pickup_datetime'].head())
```

**Marcus_Brown** [2025-03-03 3:58 PM]  
@TA_Wong Here's what I get:
```
0    2023-01-01 00:32:10
1    2023-01-01 00:38:22
2    2023-01-01 00:45:09
3    2023-01-01 00:12:56
4    2023-01-01 00:27:14
Name: tpep_pickup_datetime, dtype: object
```

**TA_Wong** [2025-03-03 4:05 PM]  
@Marcus_Brown That's strange. Those format should work with `pd.to_datetime()`. Let's try with an explicit format:
```python
df['pickup_time'] = pd.to_datetime(df['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
```
Also, check if there are any null values:
```python
print(df['tpep_pickup_datetime'].isnull().sum())
```

**Marcus_Brown** [2025-03-03 4:12 PM]  
@TA_Wong No null values in that column. The explicit format worked! Now I'm able to extract the hour:
```python
df['hour'] = df['pickup_time'].dt.hour
hourly_rides = df.groupby('hour').size()
```
Thanks for your help!

**Prof_Martinez** [2025-03-03 4:20 PM]  
@Marcus_Brown Great work! Time series analysis is quite common in big data projects. For those working with NYC TLC data, remember that analyzing patterns by hour, day of week, and month can reveal interesting insights about urban mobility.

**Marcus_Brown** [2025-03-03 4:25 PM]  
@Prof_Martinez Thanks! I'm already seeing interesting patterns - rides peak during evening rush hour and weekend nights!

## Thread: Pandas Groupby and Aggregation
**Zoe_Garcia** [2025-03-04 11:10 AM]  
I'm trying to analyze the Amazon product reviews by category and star rating. Is there an efficient way to count reviews and average rating by product category?

**TA_Patel** [2025-03-04 11:18 AM]  
@Zoe_Garcia Yes, you can use pandas groupby with multiple aggregations:
```python
category_stats = amazon_df.groupby('product_category').agg({
    'review_id': 'count',
    'star_rating': 'mean'
}).rename(columns={'review_id': 'review_count', 'star_rating': 'avg_rating'})

print(category_stats.sort_values('review_count', ascending=False))
```

**Zoe_Garcia** [2025-03-04 11:25 AM]  
@TA_Patel That worked great! Now I'm trying to filter to only include categories with at least 1000 reviews, but I'm not sure how to do that after the groupby.

**TA_Patel** [2025-03-04 11:30 AM]  
@Zoe_Garcia You can use the `.filter()` method or just filter the resulting dataframe:
```python
# Method 1: Using filter()
filtered_stats = amazon_df.groupby('product_category').filter(lambda x: len(x) >= 1000).groupby('product_category').agg({
    'review_id': 'count',
    'star_rating': 'mean'
}).rename(columns={'review_id': 'review_count', 'star_rating': 'avg_rating'})

# Method 2: Filter after aggregation
filtered_stats = category_stats[category_stats['review_count'] >= 1000]
```
Method 2 is usually more efficient for this case.

**Zoe_Garcia** [2025-03-04 11:36 AM]  
@TA_Patel Perfect! Method 2 worked well and was much faster. Thank you!

**Prof_Martinez** [2025-03-04 11:45 AM]  
@Zoe_Garcia Nice analysis! As a follow-up exercise, consider looking at the distribution of ratings within each category. Are some product categories more polarized (lots of 1-star and 5-star reviews) while others more centered around 3-4 stars?

**Zoe_Garcia** [2025-03-04 11:52 AM]  
@Prof_Martinez That's a great idea! I'll try to create a visualization of rating distributions by category.

## Thread: Pandas Visualization
**Tyler_Washington** [2025-03-05 1:30 PM]  
I'm trying to visualize the distribution of trip distances in the NYC TLC dataset but matplotlib is giving me weird results because there are some extreme outliers. Any suggestions?

**Jamie_Rodriguez** [2025-03-05 1:38 PM]  
@Tyler_Washington Try setting a limit on your plot or using log scale:
```python
import matplotlib.pyplot as plt
import numpy as np

# Option 1: Filter outliers
df_filtered = df[df['trip_distance'] < 50]  # Trips less than 50 miles
plt.hist(df_filtered['trip_distance'], bins=50)
plt.title('Trip Distance Distribution (< 50 miles)')
plt.xlabel('Distance (miles)')
plt.ylabel('Count')
plt.show()

# Option 2: Log scale
plt.hist(df['trip_distance'], bins=np.logspace(np.log10(0.1), np.log10(100), 50))
plt.xscale('log')
plt.title('Trip Distance Distribution (log scale)')
plt.xlabel('Distance (miles)')
plt.ylabel('Count')
plt.show()
```

**Tyler_Washington** [2025-03-05 1:45 PM]  
@Jamie_Rodriguez The log scale approach worked amazingly! Now I can see there's a bimodal distribution - lots of short trips (1-3 miles) and a second peak around 15-20 miles (probably airport runs). Thanks!

**TA_Wong** [2025-03-05 1:52 PM]  
@Tyler_Washington Nice observation on the bimodal distribution! You might want to try a kernel density estimation plot too:
```python
import seaborn as sns
sns.kdeplot(df_filtered['trip_distance'], bw_adjust=0.5)
plt.title('Trip Distance KDE')
plt.xlabel('Distance (miles)')
plt.show()
```
This often shows multi-modal distributions more clearly than histograms.

**Tyler_Washington** [2025-03-05 2:00 PM]  
@TA_Wong The KDE plot makes it even clearer! This is really helpful for my analysis.

**Prof_Martinez** [2025-03-05 2:10 PM]  
@Tyler_Washington Great work on the visualization! Remember that understanding your data distribution is a crucial first step in any data science project. Those airport trips you identified could be an interesting subset to analyze separately - they might have different pricing patterns, tipping behaviors, or time-of-day distributions.

**Tyler_Washington** [2025-03-05 2:15 PM]  
@Prof_Martinez Thanks for the suggestion! I'll look into comparing the airport trips with the shorter intra-city trips.
