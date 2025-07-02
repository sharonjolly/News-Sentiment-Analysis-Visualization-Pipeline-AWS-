# News-Sentiment-Analysis-Visualization-Pipeline-AWS-
This project is a fully serverless pipeline for analyzing the sentiment of real-time news articles using VADER NLP and visualizing insights via a Streamlit dashboard. Built with scalable AWS services like Lambda, EventBridge, RDS, S3, ECS Fargate, and Docker, it automatically
![Architecture](https://github.com/user-attachments/assets/87cd1712-98c1-4334-9c1c-7c33c2715add)
1. Fetching News Articles from News API
The pipeline begins by programmatically retrieving the latest news articles from a third-party News API. This API provides real-time access to headlines and news stories, which serve as the raw input for the sentiment analysis process.
2. AWS Lambda – News Ingestion and Sentiment Analysis
The Lambda function performs multiple tasks:
  i.It loads news articles using HTTP requests from the News API.
  ii.Each article is processed with the VADER SentimentIntensityAnalyzer to generate sentiment scores (positive, negative, neutral, compound).
  a.1st lambda fuction
![1 0](https://github.com/user-attachments/assets/ce5b5387-6b45-40d9-9ced-0b2e70d0ac3c)
  b.2nd lambda function
![2 0](https://github.com/user-attachments/assets/b41cd9aa-bf8f-4d07-be31-07ac13b72557)
  c.3rd lambda function
![3 0](https://github.com/user-attachments/assets/aa88e9f7-f35c-4b7e-831f-30e509afd130)
3. EventBridge – Scheduled Trigger
AWS EventBridge is configured to trigger the Lambda function every 5 minutes. This ensures the system continuously pulls fresh news data without any manual intervention, enabling real-time sentiment updates.
  i.files in S3 Bucket
![4 0](https://github.com/user-attachments/assets/98417b94-d6dd-4e97-b71f-af87ae4c62f4)
  ii.files in S3 Bucket
![5 0](https://github.com/user-attachments/assets/c34629cd-bb0e-45c6-9d87-5fd27c16b0cd)
5. Amazon RDS (PostgreSQL) – Data Storage
The structured output (headlines, timestamps, sentiment scores, etc.) is stored in a PostgreSQL database hosted on Amazon RDS. This relational database allows fast querying of sentiment data to power dashboards or reports.
