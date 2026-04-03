import pandas as pd
import matplotlib.pyplot as plt
import os

# get data and create output folder
df = pd.read_csv("data/trends_analysed.csv")
os.makedirs("outputs", exist_ok=True)

# --- chart 1: top 10 horizontal bar ---
# grab top 10 scores
top10 = df.nlargest(10, "score").copy()

# slice long titles so they fit on the graph
top10["short_title"] = top10["title"].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)
top10 = top10.sort_values("score", ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(top10["short_title"], top10["score"], color="skyblue")
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.tight_layout() # keeps text from getting cut off
plt.savefig("outputs/chart1_top_stories.png")
plt.close() # reset canvas

# --- chart 2: category bar chart ---
counts = df["subreddit"].value_counts()
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]

plt.figure(figsize=(8, 5))
plt.bar(counts.index, counts.values, color=colors[:len(counts)])
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# --- chart 3: scatter plot ---
# split into two dataframes for the different colors
popular = df[df["is_popular"] == True]
normal = df[df["is_popular"] == False]

plt.figure(figsize=(8, 5))
plt.scatter(normal["score"], normal["num_comments"], color="gray", label="Normal", alpha=0.6)
plt.scatter(popular["score"], popular["num_comments"], color="red", label="Popular", alpha=0.7)
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# --- bonus: combined dashboard ---
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold")

# 1. top 10
axs[0, 0].barh(top10["short_title"], top10["score"], color="skyblue")
axs[0, 0].set_title("Top 10 Stories")

# 2. categories
axs[0, 1].bar(counts.index, counts.values, color=colors[:len(counts)])
axs[0, 1].set_title("Stories per Category")
axs[0, 1].tick_params(axis='x', rotation=25)

# 3. scatter
axs[1, 0].scatter(normal["score"], normal["num_comments"], color="gray", label="Normal", alpha=0.6)
axs[1, 0].scatter(popular["score"], popular["num_comments"], color="red", label="Popular", alpha=0.7)
axs[1, 0].set_title("Score vs Comments")
axs[1, 0].legend()

# 4. hide empty subplot
axs[1, 1].axis("off")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Saved all 4 charts to outputs/ folder")