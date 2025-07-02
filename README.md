# News-Sentiment-Analysis-Visualization-Pipeline-AWS-
This project is a fully serverless pipeline for analyzing the sentiment of real-time news articles using VADER NLP and visualizing insights via a Streamlit dashboard. Built with scalable AWS services like Lambda, EventBridge, RDS, S3, ECS Fargate, and Docker, it automatically.

![Architecture](https://github.com/user-attachments/assets/87cd1712-98c1-4334-9c1c-7c33c2715add)

1. Fetching News Articles from News API
The pipeline begins by programmatically retrieving the latest news articles from a third-party News API. This API provides real-time access to headlines and news stories, which serve as the raw input for the sentiment analysis process.

2. AWS Lambda – News Ingestion and Sentiment Analysis
The Lambda function performs multiple tasks:
  i.It loads news articles using HTTP requests from the News API.

  ii.Each article is processed with the VADER SentimentIntensityAnalyzer to generate sentiment scores (positive, negative, neutral, compound).

  a).1st lambda fuction
![1 0](https://github.com/user-attachments/assets/ce5b5387-6b45-40d9-9ced-0b2e70d0ac3c)
  
  b).2nd lambda function
![2 0](https://github.com/user-attachments/assets/b41cd9aa-bf8f-4d07-be31-07ac13b72557)
  
  c).3rd lambda function
![3 0](https://github.com/user-attachments/assets/aa88e9f7-f35c-4b7e-831f-30e509afd130)

4. EventBridge – Scheduled Trigger
AWS EventBridge is configured to trigger the Lambda function every 5 minutes. This ensures the system continuously pulls fresh news data without any manual intervention, enabling real-time sentiment updates.

  i).files in S3 Bucket
![4 0](https://github.com/user-attachments/assets/98417b94-d6dd-4e97-b71f-af87ae4c62f4)
  
  ii).files in S3 Bucket
![5 0](https://github.com/user-attachments/assets/c34629cd-bb0e-45c6-9d87-5fd27c16b0cd)

6. Amazon RDS (PostgreSQL) – Data Storage
The structured output (headlines, timestamps, sentiment scores, etc.) is stored in a PostgreSQL database hosted on Amazon RDS. This relational database allows fast querying of sentiment data to power dashboards or reports.

  a).RDS
![6 0](https://github.com/user-attachments/assets/496d9842-16dc-4c4a-9ebb-33918c65f287)
  
  b).PgAdmin(tables)
![3 1](https://github.com/user-attachments/assets/81808fad-ffcd-4287-9b13-70626eab4427)

8. Amazon S3 – Raw Data Storage
Each news article is also saved in its raw format to an S3 bucket. These files are stored in JSON format and serve as a backup or source for batch reprocessing. This ensures no data is lost and enables reproducibility.

9. Local Development – Streamlit Dashboard
A custom dashboard is created using Streamlit, a Python framework for building interactive data apps. The dashboard is developed locally to visualize sentiment trends and article statistics. It is containerized using Docker.

10. ECR (Elastic Container Registry) – Docker Image Storage
Once the dashboard container is built locally, the Docker image is pushed to AWS ECR (Elastic Container Registry). ECR acts as a managed Docker registry for storing container images securely and makes it easier to deploy to ECS.
![ecr](https://github.com/user-attachments/assets/a516bcc0-e452-4654-ae81-6d89dd549f6e)

11. ECS Fargate – Dashboard Hosting
The dashboard container is deployed to Amazon ECS using Fargate, which allows serverless container hosting. Fargate manages provisioning, scaling, and availability, and exposes the dashboard on port 8051.
  
  i).create cluster
![9 0](https://github.com/user-attachments/assets/ac577ac2-fbbd-438d-b194-969e2d9d64da)
  
  ii).task definition
![8 0](https://github.com/user-attachments/assets/88e88760-7e45-4f71-bcf7-ef3099b3e85b)

12. Web Dashboard – Access via Browser
End users can access the live dashboard from a browser using the public IP or domain mapped to ECS. This provides real-time insights into the sentiment of news articles updated every few minutes.
  
  i).create server and task
![11 0](https://github.com/user-attachments/assets/74bd084d-41ea-4627-a485-9edc006c75d0)
  
  ii.news sentiment dashboard
![12 0](https://github.com/user-attachments/assets/6ffd36e0-fc42-4745-85a3-ac4c135eea8e)







