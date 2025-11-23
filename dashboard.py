import streamlit as st
import pandas as pd
from data_collection import fetch_twitter_posts, load_mock_data
from text_processing import clean_text
from sentiment_analysis import analyze_sentiment

st.title("Social Media Sentiment Dashboard")

topic = st.text_input("Enter topic or keyword", "healthcare")
limit = st.slider("Number of posts to analyze", 10, 200, 50)

if st.button("Run Sentiment Analysis"):

    posts = fetch_twitter_posts(topic, limit)
    if posts is None or len(posts) == 0:
        st.warning("API failed. Using mock data instead.")
        posts = load_mock_data(topic, limit)

    rows = []
    for post in posts:
        cleaned = clean_text(post["text"])
        sent = analyze_sentiment(cleaned)
        rows.append({
            "timestamp": post["timestamp"],
            "original_text": post["text"],
            "cleaned_text": cleaned,
            "sentiment_label": sent["label"],
            "sentiment_score": sent["score"]
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date

    st.subheader("Posts")
    st.dataframe(df)

    st.subheader("Sentiment Distribution")
    st.bar_chart(df["sentiment_label"].value_counts())

    st.subheader("Sentiment Trend Over Time")
    trend = df.groupby(["date", "sentiment_label"]).size().unstack().fillna(0)
    st.line_chart(trend)

    st.subheader("Insights")
    pos = (df["sentiment_label"] == "positive").mean() * 100
    neg = (df["sentiment_label"] == "negative").mean() * 100
    neu = (df["sentiment_label"] == "neutral").mean() * 100

    st.write(f"Positive: {pos:.2f}%")
    st.write(f"Negative: {neg:.2f}%")
    st.write(f"Neutral: {neu:.2f}%")
