# importing necessary libraries for api requests, time delays, and file saving
import requests
import json
import time
import os
from datetime import datetime

# the 5 subreddits required for the assignment
subreddits = ["technology", "worldnews", "sports", "science", "entertainment"]

# custom user-agent header to prevent reddit from blocking the request (429 error)
headers = {"User-Agent": "TrendPulse/1.0"}

# main list to store all the final post dictionaries
all_collected_posts = []

# loop through each subreddit in our list one by one
for subreddit in subreddits:
    print(f"Fetching trending posts from r/{subreddit}...")

    # construct the api url for the current subreddit, limiting to 25 posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
    
    # send the GET request to the reddit api
    response = requests.get(url, headers=headers)
    
    # pause for 2 seconds to respect reddit's rate limits
    time.sleep(2)

    # grab the current time right when we process this specific subreddit
    current_time = datetime.now().isoformat()
    
    # check if the request was successful before trying to parse the data
    if response.status_code == 200:
        # convert the text response into a json dictionary
        reddit_data = response.json()
        
        # go inside json and get posts
        posts = reddit_data["data"]["children"]

        # loop through every individual post in that subreddit
        for post in posts:
            # the actual post details are nested inside another 'data' key
            post_data = post["data"]

            # extract only the 7 specific fields needed for the rubric
            extracted_post = {
                "post_id": post_data["id"],
                "title": post_data["title"],
                "subreddit": post_data["subreddit"],
                "score": post_data["score"],
                "num_comments": post_data["num_comments"],
                "author": post_data["author"],
                "collected_at": current_time
            }
            
            # append the cleaned-up dictionary to our master list
            all_collected_posts.append(extracted_post)
            
    else:
        # if the request fails (like a 404 or 429), print the error and move on
        print(f"Error: Failed to fetch r/{subreddit}. Status code: {response.status_code}. Skipping.")

# SAVING THE DATA (Runs only after the loop is completely finished) 

# create a folder called 'data' in the current directory if it doesn't exist yet
os.makedirs("data", exist_ok=True)

# format today's date as YYYYMMDD to use in the file name
date_str = datetime.now().strftime("%Y%m%d")

# construct the final file path
filename = f"data/trends_{date_str}.json"

# open the file in write mode and save the main list as a formatted json file
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_collected_posts, f, indent=4)

# print the final success message showing the total count
print(f"Collected {len(all_collected_posts)} posts. Saved to {filename}")