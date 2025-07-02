import json
import boto3
import os
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from botocore.exceptions import ClientError

analyzer = SentimentIntensityAnalyzer()

def get_all_news_files(s3_client, bucket, prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' not in response:
            return []
        return [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]
    except ClientError as e:
        raise Exception(f"Error listing S3 objects: {str(e)}")

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        bucket = "newsapi-s3"
        input_prefix = "news_data/"
        output_prefix = "new_sentiment/"

        file_keys = get_all_news_files(s3, bucket, input_prefix)
        if not file_keys:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No files found in news_data'})
            }

        processed = []

        for key in file_keys:
            obj = s3.get_object(Bucket=bucket, Key=key)
            articles = json.loads(obj['Body'].read().decode('utf-8'))

            updated_articles = []
            for article in articles:
                text = article.get('description') or article.get('title') or ''
                sentiment = analyze_sentiment(text)

                updated_articles.append({
                    "published_at": article.get("published_at"),
                    "source": article.get("source"),
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "sentiment_label": sentiment
                })

            # Save to new_sentiment folder with same filename
            new_key = output_prefix + os.path.basename(key)
            s3.put_object(
                Bucket=bucket,
                Key=new_key,
                Body=json.dumps(updated_articles, ensure_ascii=False, indent=2),
                ContentType="application/json"
            )

            # Delete original file
            s3.delete_object(Bucket=bucket, Key=key)
            processed.append(new_key)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Sentiment analysis completed and saved to new_sentiment/',
                'files': processed,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        }
