import pandas as pd
import glob
import os

# --- 1. LOAD THE JSON FILE ---

# use glob to find the json file in the data folder regardless of the date it was created
json_files = glob.glob("data/trends_*.json")

if len(json_files) == 0:
    print("Error: No JSON file found. Please run task 1 first.")
    exit()

# grab the most recently modified file in case there are multiple
target_file = max(json_files, key=os.path.getmtime)

# load the json into a pandas dataframe
df = pd.read_json(target_file)
print(f"Loaded {len(df)} stories from {target_file}")


# --- 2. CLEAN THE DATA ---

# remove any rows that have the exact same post_id
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# drop rows if they are missing critical data in these specific columns
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# force score and num_comments to be integers (they sometimes load as floats/strings)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# filter the dataframe to only keep rows where the score is 5 or higher
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# strip leading and trailing whitespaces from the title strings
df["title"] = df["title"].str.strip()


# --- 3. SAVE AS CSV ---

csv_path = "data/trends_clean.csv"

# save to csv. index=False prevents pandas from writing row numbers to the file
df.to_csv(csv_path, index=False)
print(f"Saved {len(df)} rows to {csv_path}")

# print summary of remaining stories per category
print("Stories per category:")
category_counts = df["subreddit"].value_counts()

# loop through the counts and format them with spacing to match the rubric output
for category, count in category_counts.items():
    print(f"  {category:<15} {count}")