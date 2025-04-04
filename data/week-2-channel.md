# Channel week 2 - Shell Programming for Big Data

## Thread: AWK Pattern Matching Issues
**Leila_Hassan** [2025-03-08 9:15 AM]  
I'm trying to extract all trips in the NYC TLC dataset where the fare amount is greater than $50 using awk, but I'm getting zero results:
```bash
awk -F, '$10 > 50 {print $0}' yellow_tripdata_2023-02.csv > high_fare_trips.csv
```
What am I doing wrong?

**Prof_Martinez** [2025-03-08 9:22 AM]  
@Leila_Hassan It looks like you're assuming the fare amount is in the 10th column. Let's double check the column structure:
```bash
head -n 1 yellow_tripdata_2023-02.csv
```
Also, remember that CSV fields might have quotes or spaces that affect how awk parses them.

**Leila_Hassan** [2025-03-08 9:28 AM]  
@Prof_Martinez Here's the header:
```
VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge,airport_fee
```
So fare_amount is actually column 11, not 10!

**Prof_Martinez** [2025-03-08 9:35 AM]  
@Leila_Hassan Exactly! In awk, fields are 1-indexed, so you should use $11 instead of $10. Try:
```bash
awk -F, '$11 > 50 {print $0}' yellow_tripdata_2023-02.csv > high_fare_trips.csv
```
Also, be aware that if your CSV has quoted fields with commas inside them, you might need a more sophisticated CSV parser than awk.

**Leila_Hassan** [2025-03-08 9:40 AM]  
@Prof_Martinez That worked! I got 14,256 trips with fares over $50. And good point about the quoted fields - luckily the TLC data doesn't have that issue.

**TA_Patel** [2025-03-08 9:45 AM]  
@Leila_Hassan @Prof_Martinez Great troubleshooting! As a follow-up exercise, you might want to try extracting only certain columns from those high-fare trips:
```bash
# Extract pickup time, dropoff time, trip distance, and fare amount
awk -F, '$11 > 50 {print $2","$3","$5","$11}' yellow_tripdata_2023-02.csv > high_fare_details.csv
```
Don't forget to add a header!

**Leila_Hassan** [2025-03-08 9:50 AM]  
@TA_Patel Thanks for the suggestion! I added the header with:
```bash
echo "pickup_time,dropoff_time,trip_distance,fare_amount" > high_fare_details.csv
awk -F, '$11 > 50 {print $2","$3","$5","$11}' yellow_tripdata_2023-02.csv >> high_fare_details.csv
```
Now I have a nice clean CSV with just the data I need!

## Thread: Sed Substitution Errors
**Marcus_Brown** [2025-03-09 2:10 PM]  
I'm trying to clean the Amazon product reviews dataset by replacing all commas in review text with semicolons using sed, but it's not working:
```bash
sed 's/,/;/g' amazon_reviews.csv > amazon_reviews_cleaned.csv
```
Now my CSV structure is completely broken!

**TA_Wong** [2025-03-09 2:20 PM]  
@Marcus_Brown The issue is that you're replacing ALL commas, including the ones that separate CSV fields! You only want to replace commas within the review text field. Assuming the review text is in quotes, you could try:
```bash
sed 's/\("[^"]*\),\([^"]*"\)/\1;\2/g' amazon_reviews.csv > amazon_reviews_cleaned.csv
```
But honestly, for this kind of CSV manipulation, I'd recommend using Python or a proper CSV tool.

**Marcus_Brown** [2025-03-09 2:25 PM]  
@TA_Wong That sed command is quite complex and still doesn't seem to work correctly. Is there a simpler shell approach?

**Prof_Martinez** [2025-03-09 2:35 PM]  
@Marcus_Brown @TA_Wong This is a great example of when shell tools start to show their limitations. For properly handling quoted fields in CSVs, I'd recommend using a tool designed for that purpose:
```bash
# Using csvkit (you might need to install it)
csvformat -D ';' amazon_reviews.csv > amazon_reviews_cleaned.csv

# Or using Python in one line
python -c "import csv,sys; w=csv.writer(sys.stdout,delimiter=',');r=csv.reader(open('amazon_reviews.csv'),delimiter=',',quotechar='\"');[w.writerow([field.replace(',',';') for field in row]) for row in r]" > amazon_reviews_cleaned.csv
```

**Marcus_Brown** [2025-03-09 2:42 PM]  
@Prof_Martinez I tried the Python one-liner and it worked perfectly! I see what you mean about the limitations of sed for this kind of task.

**TA_Wong** [2025-03-09 2:50 PM]  
@Marcus_Brown @Prof_Martinez This is a good lesson in choosing the right tool for the job. While sed is powerful for simple text transformations, parsing structured formats like CSV often requires more specialized tools. For next week's homework on the Amazon reviews, I recommend sticking with Python's CSV module or pandas.

**Marcus_Brown** [2025-03-09 2:55 PM]  
@TA_Wong Makes sense. Thanks for the help!

## Thread: Shell Scripting for Data Preparation
**David_Kim** [2025-03-10 11:05 AM]  
I need to prepare the NYC TLC dataset for analysis by:
1. Combining Jan-Mar 2023 data files
2. Removing rows with zero passengers
3. Removing rows with fare_amount <= 0
4. Saving as a new CSV

Can I do this efficiently with shell commands?

**Jamie_Rodriguez** [2025-03-10 11:15 AM]  
@David_Kim Yes, you can! Here's a basic approach:
```bash
# Step 1: Extract headers from one file
head -n 1 yellow_tripdata_2023-01.csv > combined_clean.csv

# Step 2: Combine data, exclude header lines, filter by conditions
for month in 01 02 03; do
  tail -n +2 yellow_tripdata_2023-$month.csv | \
  awk -F, '$4 > 0 && $11 > 0' >> combined_clean.csv
done
```
This assumes passenger_count is column 4 and fare_amount is column 11.

**David_Kim** [2025-03-10 11:22 AM]  
@Jamie_Rodriguez I get this error:
```
awk: cmd. line:1: (FILENAME=- FNR=1) fatal: Invalid back reference
```

**TA_Patel** [2025-03-10 11:30 AM]  
@David_Kim The error suggests there might be some special characters in your data that awk is interpreting as pattern matching characters. Let's try a slightly modified approach:
```bash
# Step 1: Extract headers from one file
head -n 1 yellow_tripdata_2023-01.csv > combined_clean.csv

# Step 2: Process each file
for month in 01 02 03; do
  echo "Processing month $month..."
  tail -n +2 yellow_tripdata_2023-$month.csv | \
  awk -F, '{if ($4 > 0 && $11 > 0) print $0}' >> combined_clean.csv
done
```
The explicit `if` condition should help avoid interpretation issues.

**David_Kim** [2025-03-10 11:40 AM]  
@TA_Patel That worked! Here's what I got:
```
Processing month 01...
Processing month 02...
Processing month 03...
```
And the output file looks good with all the filters applied.

**Prof_Martinez** [2025-03-10 11:50 AM]  
@David_Kim Great job! One thing to consider: with large datasets like the NYC TLC data, it's useful to add some progress monitoring to your shell scripts. Here's an enhanced version:
```bash

# Step 1: Extract headers from one file
head -n 1 yellow_tripdata_2023-01.csv > combined_clean.csv

# Step 2: Process each file with progress monitoring
for month in 01 02 03; do
  echo "Processing month $month..."
  TOTAL_LINES=$(wc -l < yellow_tripdata_2023-$month.csv)
  PROCESSED_LINES=0
  KEPT_LINES=0
  
  tail -n +2 yellow_tripdata_2023-$month.csv | \
  awk -F, -v processed=0 -v kept=0 '
    BEGIN {OFS=FS}
    {
      processed++
      if (processed % 100000 == 0)
        print "Processed " processed " lines..." > "/dev/stderr"
      
      if ($4 > 0 && $11 > 0) {
        print $0
        kept++
      }
    }
    END {
      print "Month " "'$month'" ": Kept " kept " out of " processed " records (" (kept/processed*100) "%)" > "/dev/stderr"
    }
  ' >> combined_clean.csv
done
```
This version prints progress updates and gives you statistics on how many records were kept vs. filtered out.

**David_Kim** [2025-03-10 12:05 PM]  
@Prof_Martinez This is fantastic! I ran it and got:
```
Processing month 01...
Processed 100000 lines...
Processed 200000 lines...
...
Month 01: Kept 2856432 out of 3012234 records (94.8%)
Processing month 02...
...
```
Now I have a better understanding of the filtering impact. Thank you!

**TA_Wong** [2025-03-10 12:10 PM]  
@David_Kim @Prof_Martinez Great work! This is a perfect example of how shell scripting can be used for data preparation. For future reference, you might want to save this as a reusable script:
```bash
#!/bin/bash
# clean_tlc_data.sh
# Usage: ./clean_tlc_data.sh year month_start month_end output_file

YEAR=$1
MONTH_START=$2
MONTH_END=$3
OUTPUT=$4

# Extract headers from first file
head -n 1 yellow_tripdata_$YEAR-$(printf "%02d" $MONTH_START).csv > $OUTPUT

# Process each month
for ((month=$MONTH_START; month<=$MONTH_END; month++)); do
  MONTH_PADDED=$(printf "%02d" $month)
  echo "Processing $YEAR-$MONTH_PADDED..."
  # Add the rest of your processing code here
done
```
Then you can call it as `./clean_tlc_data.sh 2023 1 3 combined_clean.csv`

**David_Kim** [2025-03-10 12:15 PM]  
@TA_Wong Thanks for the script template! I'll definitely use this for future assignments.

## Thread: Parallel Processing with GNU Parallel
**Zoe_Garcia** [2025-03-11 3:20 PM]  
For my project on Amazon product reviews, I need to process 50 different product categories in parallel. I've written a script that processes one category, but running it 50 times sequentially will take too long. Any suggestions?

**Prof_Martinez** [2025-03-11 3:30 PM]  
@Zoe_Garcia This is a perfect use case for GNU Parallel. Assuming you have a script `process_category.sh` that takes a category name as input:
```bash
# First, create a file with all categories
awk -F, '{print $7}' amazon_reviews.csv | sort | uniq > categories.txt

# Then run your script for each category in parallel
cat categories.txt | parallel -j 8 './process_category.sh {}'
```
The `-j 8` flag tells parallel to run 8 jobs simultaneously. Adjust based on your machine's CPU cores.

**Zoe_Garcia** [2025-03-11 3:40 PM]  
@Prof_Martinez I'm getting an error: `bash: parallel: command not found`

**TA_Patel** [2025-03-11 3:45 PM]  
@Zoe_Garcia You need to install GNU Parallel first:
```bash
# On Ubuntu/Debian
sudo apt-get install parallel

# On macOS with Homebrew
brew install parallel

# On CentOS/RHEL
sudo yum install parallel
```
After installing, you might want to run `parallel --citation` once to dismiss the citation notice.

**Zoe_Garcia** [2025-03-11 3:52 PM]  
@TA_Patel Got it installed, and it's working now! This is amazing - the processing that would have taken hours is now done in about 20 minutes. Is there any way to see progress?

**Prof_Martinez** [2025-03-11 4:00 PM]  
@Zoe_Garcia Absolutely! GNU Parallel has built-in progress reporting:
```bash
cat categories.txt | parallel --progress './process_category.sh {}'
```
You can also get more detailed output with:
```bash
cat categories.txt | parallel --eta './process_category.sh {}'
```
This will show an estimated time of completion.

**Zoe_Garcia** [2025-03-11 4:05 PM]  
@Prof_Martinez The `--eta` flag is super helpful! Now I can see exactly how long it will take to complete.

**TA_Wong** [2025-03-11 4:10 PM]  
@Zoe_Garcia Another useful flag is `--joblog` which creates a log file of all the jobs:
```bash
cat categories.txt | parallel --eta --joblog process_log.txt './process_category.sh {}'
```
This helps track which categories have been processed, how long each took, and if any failed.

**Zoe_Garcia** [2025-03-11 4:15 PM]  
@TA_Wong Perfect! I see now that some categories take much longer than others. This will be very useful for my final report.

## Thread: Shell Pipes and Redirects for Log Analysis
**Alex_Chen** [2025-03-12 10:30 AM]  
I have access logs from my web server where people download the NYC TLC dataset. I need to:
1. Find which taxi data files are most popular
2. Identify peak download hours
3. Check which IPs are downloading the most

The log format is: `timestamp IP requested_file status_code response_size`
Any suggestions for shell commands?

**Jamie_Rodriguez** [2025-03-12 10:40 AM]  
@Alex_Chen Here are some one-liners for each task:

1. Most popular taxi data files:
```bash
awk '{print $3}' access.log | grep -E 'yellow_tripdata|green_tripdata' | sort | uniq -c | sort -nr | head -10
```

2. Peak download hours:
```bash
awk '{split($1,t,":"); print t[2]}' access.log | sort | uniq -c | sort -nr
```

3. IPs with most downloads:
```bash
awk '{print $2}' access.log | sort | uniq -c | sort -nr | head -10
```

**Alex_Chen** [2025-03-12 10:47 AM]  
@Jamie_Rodriguez When I try the first command, I get weird results. Here's a sample of my log:
```
2025-03-01T08:23:15Z 192.168.1.42 /data/yellow_tripdata_2023-01.csv 200 523872
2025-03-01T09:14:22Z 192.168.1.105 /data/green_tripdata_2023-02.csv 200 489213
```
The format seems different from what you expected.

**TA_Patel** [2025-03-12 10:55 AM]  
@Alex_Chen Based on your log format, try these modified commands:

1. Most popular taxi data files:
```bash
awk '{print $3}' access.log | sort | uniq -c | sort -nr | head -10
```

2. Peak download hours:
```bash
awk '{split($1,t,"T"); split(t[2],h,":"); print h[1]}' access.log | sort | uniq -c | sort -nr
```

3. IPs with most downloads:
```bash
awk '{print $2}' access.log | sort | uniq -c | sort -nr | head -10
```

**Alex_Chen** [2025-03-12 11:05 AM]  
@TA_Patel These worked much better! Here's what I found:
- Most popular file is yellow_tripdata_2023-01.csv with 1452 downloads
- Peak download hour is 14 (2PM) with 523 downloads
- Top IP has 89 downloads (probably a script)

**Prof_Martinez** [2025-03-12 11:15 AM]  
@Alex_Chen Great analysis! For a more comprehensive view, you might want to:

1. Look at downloads by day of week:
```bash
awk '{cmd="date -d \""substr($1,1,10)"\" +%u"; cmd | getline dow; print dow}' access.log | sort | uniq -c
```

2. Check if there are unsuccessful downloads (non-200 status codes):
```bash
awk '$4 != 200 {print $0}' access.log | less
```

3. Calculate total download volume:
```bash
awk '{sum += $5} END {print sum/1024/1024/1024 " GB"}' access.log
```

**Alex_Chen** [2025-03-12 11:22 AM]  
@Prof_Martinez The day of week command gives an error: `date: invalid date`

**TA_Wong** [2025-03-12 11:30 AM]  
@Alex_Chen The date format needs adjustment for your timestamp. Try:
```bash
awk '{cmd="date -d \""substr($1,1,10)"\" +%u"; cmd | getline dow; print dow}' access.log | sort | uniq -c
```
If you're on macOS, the date command syntax is different:
```bash
awk '{cmd="date -j -f \"%Y-%m-%d\" \""substr($1,1,10)"\" +%u"; cmd | getline dow; print dow}' access.log | sort | uniq -c
```

**Alex_Chen** [2025-03-12 11:38 AM]  
@TA_Wong The macOS version worked! I see that most downloads happen on weekdays, especially Tuesday and Wednesday. Thanks everyone for the help! This will be very useful for my report.

**Prof_Martinez** [2025-03-12 11:45 AM]  
@Alex_Chen Excellent! This kind of log analysis is a common task in big data scenarios. In the real world, you'd typically use tools like Elasticsearch, Splunk, or even Apache Spark for log analysis at scale, but these shell commands are perfect for quick insights on smaller datasets.