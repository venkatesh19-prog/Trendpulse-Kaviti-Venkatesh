import pandas as pd
import numpy as np

# load the clean csv we made in task 2
df = pd.read_csv("data/trends_clean.csv")

# print basic info so we know it loaded right
print(f"Loaded data: {df.shape}")
print("First 5 rows:")
print(df.head(), "\n")

# get the overall averages using normal pandas functions
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

# using :,.0f to format with commas and no decimals like the rubric wants
print(f"Average score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}\n")

print("--- NumPy Stats ---")

# pull just the scores into a basic numpy array for the math section
scores = df["score"].to_numpy()

# calculate the required stats with numpy
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

# print the numpy stats with the same comma formatting
print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_score:,.0f}")
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

# find which category appears the most times by checking value counts
top_subreddit = df["subreddit"].value_counts().idxmax()
top_count = df["subreddit"].value_counts().max()
print(f"Most stories in: {top_subreddit} ({top_count} stories)")

# find the row index with the highest comments, then grab that exact row
max_idx = df["num_comments"].idxmax()
top_story = df.loc[max_idx]
print(f"Most commented story: \"{top_story['title']}\" — {top_story['num_comments']:,} comments\n")


# --- adding new columns ---

# engagement formula: comments divided by score (+1 to avoid dividing by zero)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# create a true/false column checking if the score is above our average
df["is_popular"] = df["score"] > avg_score

# save everything to a new file for task 4 (index=False stops it from adding junk numbers)
df.to_csv("data/trends_analysed.csv", index=False)
print("Saved to data/trends_analysed.csv")