# Reddit Content Insight Dashboard

A data analytics project that collects Reddit post data, analyzes engagement patterns, and presents insights through an interactive dashboard.

## 🚀 Live Demo
https://redditcontentinsight-gahdauijg3mvzim7kjkywz.streamlit.app

## Overview

This project uses Reddit data from `r/photography` to explore how content features relate to engagement. It includes:

- Data collection from Reddit JSON endpoints
- Data cleaning and feature extraction
- Basic content categorization
- Engagement analysis
- Interactive dashboard visualization with Streamlit

The goal is to simulate a lightweight analytics workflow similar to what a data analyst or analytics engineer might build for content performance monitoring.

## Features

- Collects Reddit post data across multiple pages
- Stores raw data in CSV format
- Generates analytical summaries in text and CSV outputs
- Categorizes posts into groups such as:
  - question
  - advice
  - personal
  - other
- Visualizes:
  - top posts by score
  - category distribution
  - title length vs. score
  - comments vs. score
  - average score by category

## Tech Stack

- Python
- Pandas
- Requests
- Streamlit
- Plotly

## Project Structure

```text
.
├── reddit_test.py
├── app.py
├── reddit_data.csv
├── category_analysis.csv
├── analysis.txt
└── README.md
