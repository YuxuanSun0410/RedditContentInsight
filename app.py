import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Reddit Content Insight Dashboard", layout="wide")

st.title("Reddit Content Insight Dashboard")
st.write("Analyze Reddit post engagement patterns and simple content categories.")

df = pd.read_csv("result/reddit_data.csv")

df["has_text"] = df["selftext"].apply(lambda x: 0 if x == "" else 1)

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

st.subheader("Raw Data")
st.dataframe(df)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Posts by Score")
    top_posts = df[["title", "score", "comments", "category"]].sort_values(by="score", ascending=False).head(10)
    st.dataframe(top_posts)

with col2:
    st.subheader("Category Distribution")
    fig_cat = px.bar(
        df["category"].value_counts().reset_index(),
        x="category",
        y="count",
        labels={"category": "Category", "count": "Number of Posts"},
        title="Number of Posts by Category"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

st.subheader("Title Length vs Score")
fig_scatter = px.scatter(
    df,
    x="title_length",
    y="score",
    hover_data=["title", "category"],
    title="Title Length vs Engagement Score"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Average Score by Category")
avg_score = df.groupby("category", as_index=False)["score"].mean()
fig_avg = px.bar(
    avg_score,
    x="category",
    y="score",
    title="Average Score by Category"
)
st.plotly_chart(fig_avg, use_container_width=True)

st.subheader("Comments vs Score")
fig_comments = px.scatter(
    df,
    x="comments",
    y="score",
    hover_data=["title", "category"],
    title="Comments vs Score"
)
st.plotly_chart(fig_comments, use_container_width=True)

st.subheader("Key Insights")

corr = df["comments"].corr(df["score"])

st.write(f"- Correlation between comments and score: **{corr:.2f}**")
st.write("- Moderately concise titles may perform better than very long titles.")
st.write("- Content categories can be used as a simple approximation of audience interest patterns.")
st.write("- This dashboard is a first-step prototype for content insight and audience analysis.")
