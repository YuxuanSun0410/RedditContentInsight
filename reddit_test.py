import requests
import pandas as pd
import time

base_url = "https://www.reddit.com/r/photography/hot.json"

headers = {
    "User-Agent": "persona-project"
}

posts = []
after = None

for _ in range(5):
    if after:
        url = f"{base_url}?after={after}"
    else:
        url = base_url

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    for post in data["data"]["children"]:
        p = post["data"]
        posts.append({
            "title": p["title"],
            "selftext": p["selftext"],
            "score": p["score"],
            "comments": p["num_comments"],
            "created": p["created_utc"],
            "title_length": len(p["title"])
        })

    after = data["data"]["after"]
    if after is None:
        break

    time.sleep(1)

df = pd.DataFrame(posts)
df = df.drop_duplicates(subset=["title"])

print(df.head())

df.to_csv("reddit_data.csv", index=False)

df = pd.read_csv("reddit_data.csv")

print("\n--- Title Length vs Score ---")
print(df[["title_length", "score"]].sort_values(by="score", ascending=False).head())

df["has_text"] = df["selftext"].apply(lambda x: 0 if x == "" else 1)

print("\n--- Has Text vs Average Score ---")
print(df.groupby("has_text")["score"].mean())

print("\n--- Correlation (comments vs score) ---")
print(df["comments"].corr(df["score"]))

def classify_post(title):
    title = title.lower()
    if "?" in title:
        return "question"
    elif "help" in title or "advice" in title:
        return "advice"
    elif "my" in title or "first" in title:
        return "personal"
    else:
        return "other"

df["category"] = df["title"].apply(classify_post)

print("\n--- Category vs Average Score ---")
print(df.groupby("category")["score"].mean())

print("\n--- Category Distribution ---")
print(df["category"].value_counts())

df.groupby("category")["score"].mean().to_csv("category_analysis.csv")

with open("analysis.txt", "w") as f:
    f.write("=== Analysis Results ===\n\n")

    f.write("Top Title Length vs Score:\n")
    f.write(df[["title_length", "score"]].sort_values(by="score", ascending=False).head().to_string())

    f.write("\n\nHas Text vs Average Score:\n")
    f.write(df.groupby("has_text")["score"].mean().to_string())

    f.write("\n\nCorrelation (comments vs score):\n")
    f.write(str(df["comments"].corr(df["score"])))

    f.write("\n\nCategory vs Average Score:\n")
    f.write(df.groupby("category")["score"].mean().to_string())

    f.write("\n\nCategory Distribution:\n")
    f.write(df["category"].value_counts().to_string())