import json
import os
import boto3
import requests
import re
from datetime import datetime

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'\\u[0-9A-Fa-f]{4}', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def lambda_handler(event, context):
    api_key = os.environ.get('NEWS_API_KEY')  #Use proper env var
    if not api_key:
        raise Exception("API key not found in environment variables.")

    url = f"https://newsapi.org/v2/everything?q=*&language=en&pageSize=20&sortBy=publishedAt&apiKey={api_key}"  #Use the variable here

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"NewsAPI request failed: {response.status_code} - {response.text}")

    news_json = response.json()
    articles = news_json.get("articles", [])
    filtered_articles = []

    for article in articles:
        filtered_articles.append({
            "published_at": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
            "source": clean_text(article["source"]["name"]),
            "title": clean_text(article["title"]),
            "description": clean_text(article.get("description", ""))
        })

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Fetched at: {timestamp}")

    s3 = boto3.client('s3')
    filename = "news_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".json"

    s3.put_object(
    Bucket="newsapi-s3",
    Key="news_data/" + filename,
    Body=json.dumps(filtered_articles, ensure_ascii=False, indent=2),  # Add indent=2
    ContentType="application/json"
)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "News fetched and uploaded", "fetched_at": timestamp})
    }
