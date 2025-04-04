# Channel week 3 - Multiprocessing with Python and Asyncio

## Thread: Understanding the GIL
**Sarah_Johnson** [2025-03-15 10:00 AM]  
I'm confused about when to use multiprocessing vs threading in Python. If I'm processing the NYC TLC dataset in chunks, which should I use?

**Prof_Martinez** [2025-03-15 10:10 AM]  
@Sarah_Johnson Great question! This comes down to understanding Python's Global Interpreter Lock (GIL). Here's a simple breakdown:

- **Threading**: Multiple threads share the same memory space, but the GIL prevents true parallel execution of Python code. Good for I/O-bound tasks (like reading files, network requests).

- **Multiprocessing**: Creates separate Python processes, each with its own memory and GIL. Good for CPU-bound tasks (like data processing, calculations).

For the NYC TLC dataset, if you're doing heavy computation on each chunk (like complex aggregations), use multiprocessing. If you're mostly waiting for I/O (like reading chunks from disk), threading might be more efficient.

**Sarah_Johnson** [2025-03-15 10:15 AM]  
@Prof_Martinez Thanks, that helps! My task involves calculating distance-based statistics for each taxi trip. Would that be considered CPU-bound?

**Prof_Martinez** [2025-03-15 10:22 AM]  
@Sarah_Johnson Yes, mathematical calculations like distance statistics would be CPU-bound, so multiprocessing would likely give you better performance. Here's a simple example:

```python
import pandas as pd
from multiprocessing import Pool

def process_chunk(file_chunk):
    # Read chunk into DataFrame
    df_chunk = pd.read_csv(file_chunk)
    
    # Calculate statistics
    result = {
        'avg_distance': df_chunk['trip_distance'].mean(),
        'max_distance': df_chunk['trip_distance'].max(),
        'total_miles': df_chunk['trip_distance'].sum()
    }
    return result

# Split your file into chunks (you can use the pandas chunksize parameter or physical file splits)
chunks = ['chunk1.csv', 'chunk2.csv', 'chunk3.csv', 'chunk4.csv']

# Process in parallel
with Pool(processes=4) as pool:
    results = pool.map(process_chunk, chunks)
    
# Combine results
final_result = {
    'avg_distance': sum(r['avg_distance'] for r in results) / len(results),
    'max_distance': max(r['max_distance'] for r in results),
    'total_miles': sum(r['total_miles'] for r in results)
}
```

**Sarah_Johnson** [2025-03-15 10:30 AM]  
@Prof_Martinez That code example makes it much clearer. One follow-up question: how do I determine the optimal number of processes? My laptop has 8 cores.

**TA_Wong** [2025-03-15 10:38 AM]  
@Sarah_Johnson Generally, you want to match the number of processes to the number of CPU cores available:

```python
import multiprocessing as mp

# Get number of available cores
num_cores = mp.cpu_count()
print(f"You have {num_cores} CPU cores available")

# Use all available cores (or slightly fewer)
with Pool(processes=num_cores) as pool:
    results = pool.map(process_chunk, chunks)
```

But there are a few considerations:
1. If your task is memory-intensive, using too many processes could cause your system to run out of memory
2. For very I/O heavy tasks, you might benefit from slightly more processes than cores
3. Leave at least 1-2 cores free if you need your computer to stay responsive for other tasks

**Sarah_Johnson** [2025-03-15 10:45 AM]  
@TA_Wong Thanks! I'll start with num_cores-1 to keep my laptop usable while processing.

## Thread: Asyncio for API Calls
**David_Kim** [2025-03-16 2:30 PM]  
I'm working on a project that needs to fetch product details from an API for each Amazon review. With over 10,000 reviews, doing this sequentially is taking forever. Is this a good case for asyncio?

**Prof_Martinez** [2025-03-16 2:40 PM]  
@David_Kim This is a perfect use case for asyncio! Since you're waiting on network responses (I/O-bound), asyncio can make hundreds of concurrent API calls without the overhead of threads or processes. Here's an example:

```python
import asyncio
import aiohttp
import pandas as pd

async def fetch_product_details(session, product_id):
    url = f"https://api.example.com/products/{product_id}"
    async with session.get(url) as response:
        return await response.json()

async def process_all_products(product_ids):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for product_id in product_ids:
            task = asyncio.create_task(fetch_product_details(session, product_id))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results

# Main code
df = pd.read_csv('amazon_reviews.csv')
unique_product_ids = df['product_id'].unique()

# Run the async function
results = asyncio.run(process_all_products(unique_product_ids))
```

**David_Kim** [2025-03-16 2:50 PM]  
@Prof_Martinez This looks promising! But I'm getting errors about event loops. Do I need to create one explicitly?

**TA_Patel** [2025-03-16 3:00 PM]  
@David_Kim The error might depend on how you're running the code. If you're in a Jupyter notebook, you need a slightly different approach since Jupyter already has an event loop:

```python
# For Jupyter notebooks:
import nest_asyncio
nest_asyncio.apply()

# Then your code should work with asyncio.run()
```

If you're running in a regular Python script, `asyncio.run()` should work fine. Also, you might want to add rate limiting to avoid overwhelming the API:

```python
import asyncio
import aiohttp
import pandas as pd
from asyncio import Semaphore

# Limit concurrency to 50 simultaneous requests
async def fetch_product_details(session, product_id, semaphore):
    async with semaphore:
        url = f"https://api.example.com/products/{product_id}"
        async with session.get(url) as response:
            return await response.json()

async def process_all_products(product_ids):
    semaphore = Semaphore(50)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for product_id in product_ids:
            task = asyncio.create_task(
                fetch_product_details(session, product_id, semaphore)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results
```

**David_Kim** [2025-03-16 3:10 PM]  
@TA_Patel The semaphore approach worked perfectly! I was indeed overwhelming the API before. Now it's running about 20x faster than my sequential version. Thanks!

**Prof_Martinez** [2025-03-16 3:15 PM]  
@David_Kim Excellent! This is a great example of choosing the right concurrency tool for the job. For network I/O tasks like API calls, asyncio is often the best choice because it:
1. Uses less memory than threads or processes
2. Can handle thousands of concurrent connections
3. Avoids the complexities of thread synchronization

Remember to add error handling for when API calls fail:

```python
async def fetch_product_details(session, product_id, semaphore):
    async with semaphore:
        try:
            url = f"https://api.example.com/products/{product_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error fetching {product_id}: Status {response.status}")
                    return None
        except Exception as e:
            print(f"Exception for {product_id}: {str(e)}")
            return None
```

**David_Kim** [2025-03-16 3:20 PM]  
@Prof_Martinez Great suggestion on the error handling! I've implemented it and now my code is much more robust.

## Thread: Combining Multiprocessing and Threading
**Tyler_Washington** [2025-03-17 11:10 AM]  
For my project, I need to:
1. Process multiple large CSV files from the NYC TLC dataset
2. For each file, make API calls to enrich the data
3. Write the results to a database

What's the best way to structure this using parallel processing?

**TA_Wong** [2025-03-17 11:20 AM]  
@Tyler_Washington This is a great case for combining multiprocessing and threading/asyncio! Here's a strategic approach:

1. Use multiprocessing to handle different files in parallel (CPU-bound file processing)
2. Within each process, use asyncio for the API calls (I/O-bound)
3. Use connection pooling for database writes (also I/O-bound)

Here's a skeleton:

```python
import pandas as pd
import asyncio
import aiohttp
import multiprocessing as mp
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

def process_file(filename):
    # 1. Read and process the CSV
    df = pd.read_csv(filename)
    
    # 2. Extract IDs for API enrichment
    ids_to_enrich = df['some_id_column'].unique()
    
    # 3. Run asyncio to fetch data
    enrichment_data = asyncio.run(fetch_enrichment_data(ids_to_enrich))
    
    # 4. Merge enrichment data with original dataframe
    # ...code to merge...
    
    # 5. Write to database
    engine = create_engine('postgresql://user:password@localhost/dbname', 
                          poolclass=QueuePool)
    df.to_sql('enriched_data', engine, if_exists='append', index=False)
    
    return f"Processed {filename} with {len(df)} rows"

async def fetch_enrichment_data(ids):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for id in ids:
            task = asyncio.create_task(fetch_single_id(session, id))
            tasks.append(task)
        return await asyncio.gather(*tasks)

async def fetch_single_id(session, id):
    # API call code here
    pass

# Main execution
if __name__ == '__main__':
    files = ['yellow_tripdata_2023-01.csv', 'yellow_tripdata_2023-02.csv', ...]
    
    with mp.Pool(processes=mp.cpu_count()-1) as pool:
        results = pool.map(process_file, files)
        
    for result in results:
        print(result)
```

**Tyler_Washington** [2025-03-17 11:32 AM]  
@TA_Wong This is exactly what I needed! But I'm concerned about memory usage. If each CSV is 2GB and I have 4 cores, won't this potentially use 8GB of RAM?

**Prof_Martinez** [2025-03-17 11:40 AM]  
@Tyler_Washington You're right to be concerned about memory. Here are some strategies to manage memory usage:

1. Process each file in chunks:
```python
def process_file(filename):
    results = []
    # Process in chunks of 100,000 rows
    for chunk in pd.read_csv(filename, chunksize=100000):
        # Process chunk
        # Enrich chunk with API data
        # Write chunk to database
        results.append(f"Processed chunk with {len(chunk)} rows")
    return results
```

2. Limit the process pool to fewer processes than your core count:
```python
# If you have 16GB RAM and each process might use 4GB
with mp.Pool(processes=min(3, mp.cpu_count()-1)) as pool:
    results = pool.map(process_file, files)
```

3. Consider using a shared memory approach with memory-mapped files for very large datasets.

**Tyler_Washington** [2025-03-17 11:50 AM]  
@Prof_Martinez The chunking approach is brilliant! I implemented it and my memory usage stays under control now. Is there any way to show a progress bar so I can see how far along each file is?

**TA_Patel** [2025-03-17 12:00 PM]  
@Tyler_Washington Yes! You can use the tqdm library for progress tracking:

```python
from tqdm import tqdm

def process_file(filename):
    # Get total rows for progress tracking
    total_rows = sum(1 for _ in open(filename)) - 1  # subtract header
    
    results = []
    # Create progress bar
    with tqdm(total=total_rows, desc=f"Processing {filename}") as pbar:
        for chunk in pd.read_csv(filename, chunksize=100000):
            # Process chunk
            # ...your processing code...
            
            # Update progress bar
            pbar.update(len(chunk))
            results.append(f"Processed chunk with {len(chunk)} rows")
    
    return results
```

For multiprocessing, you'll need a slightly different approach since tqdm needs to be thread-safe:

```python
from tqdm.contrib.concurrent import process_map

# Replace this:
# with mp.Pool(processes=mp.cpu_count()-1) as pool:
#     results = pool.map(process_file, files)

# With this:
results = process_map(process_file, files, max_workers=mp.cpu_count()-1)
```

**Tyler_Washington** [2025-03-17 12:10 PM]  
@TA_Patel This is fantastic! Now I can see multiple progress bars, one for each file being processed. This makes debugging and monitoring so much easier.

**Prof_Martinez** [2025-03-17 12:15 PM]  
@Tyler_Washington Great work integrating all these components! You've essentially built a mini data pipeline with:
1. Parallel file processing (multiprocessing)
2. Concurrent API requests (asyncio)
3. Efficient database writes (connection pooling)
4. Memory management (chunking)
5. Progress monitoring (tqdm)

This kind of architecture is very similar to what you'd see in production big data systems. In larger systems, you might replace these components with tools like Apache Spark (for processing), Kafka (for message queues), and specialized databases, but the core concepts remain the same.

## Thread: Asyncio vs. Multithreading Performance
**Aisha_Patel** [2025-03-18 2:15 PM]  
For my Amazon product reviews analysis, I need to download product images for sentiment analysis. Should I use threading or asyncio? I want to compare performance.

**TA_Wong** [2025-03-18 2:25 PM]  
@Aisha_Patel This is a great question for empirical testing! Let's write code to compare both approaches:

```python
import time
import requests
import threading
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Sample URLs (replace with your actual image URLs)
urls = [f"https://example.com/product_{i}.jpg" for i in range(100)]

# Threaded approach
def download_image_threaded(url):
    response = requests.get(url)
    # Process image data
    return len(response.content)

def run_threaded_download():
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(download_image_threaded, urls))
    
    end = time.time()
    print(f"Threaded download took {end - start:.2f} seconds")
    return results

# Asyncio approach
async def download_image_async(session, url):
    async with session.get(url) as response:
        data = await response.read()
        # Process image data
        return len(data)

async def run_async_download():
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    end = time.time()
    print(f"Asyncio download took {end - start:.2f} seconds")
    return results

# Compare both approaches
def compare_performance():
    # Run threaded version
    threaded_results = run_threaded_download()
    
    # Run asyncio version
    asyncio_results = asyncio.run(run_async_download())
    
    # Verify results are the same
    assert sum(threaded_results) == sum(asyncio_results)

if __name__ == "__main__":
    compare_performance()
```

Run this test with your actual URLs to see which performs better for your specific use case.

**Aisha_Patel** [2025-03-18 2:42 PM]  
@TA_Wong I ran the test, and asyncio was about 3x faster! But I'm confused why - I thought threading and asyncio were both good for I/O-bound tasks?

**Prof_Martinez** [2025-03-18 2:55 PM]  
@Aisha_Patel Great observation! Both threading and asyncio are indeed good for I/O-bound tasks, but they work differently:

1. **Threading overhead**: Each thread has memory overhead (few MB per thread) and context switching costs
2. **Connection pooling**: aiohttp reuses connections more efficiently than the requests library
3. **Event loop efficiency**: Asyncio's event loop can handle thousands of connections with less overhead

For HTTP requests specifically, asyncio often outperforms threading because the asyncio libraries (like aiohttp) are specifically optimized for high-concurrency HTTP workloads.

However, there are cases where threading might perform better:
- When you're calling C extensions that release the GIL
- When you have significant CPU work mixed with I/O
- When you need true parallel execution

To make your asyncio version even faster, consider adding connection pooling limits and timeouts:

```python
conn = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
timeout = aiohttp.ClientTimeout(total=60)
async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
    # Your code
```

**Aisha_Patel** [2025-03-18 3:05 PM]  
@Prof_Martinez With the connection pooling changes, it's now almost 4x faster than threading! This is going to save me hours of processing time.

**TA_Patel** [2025-03-18 3:15 PM]  
@Aisha_Patel Another consideration: if you need to process the downloaded images (like image analysis or transformations), that processing is CPU-bound. For that part, you might want to:

1. Download all images asynchronously with asyncio
2. Process the images with multiprocessing

Something like:

```python
async def download_all_images():
    # Your asyncio download code
    # Returns a list of image_data

def process_image(image_data):
    # CPU-intensive image processing
    # Return processed results

# Main flow
image_data_list = asyncio.run(download_all_images())

with mp.Pool(processes=mp.cpu_count()) as pool:
    results = pool.map(process_image, image_data_list)
```

This gives you the best of both worlds: fast asyncio downloads and parallel CPU processing.

**Aisha_Patel** [2025-03-18 3:25 PM]  
@TA_Patel That's exactly what I need! I'm doing sentiment analysis on the product images using a machine learning model, which is definitely CPU-intensive. I'll implement this hybrid approach.
