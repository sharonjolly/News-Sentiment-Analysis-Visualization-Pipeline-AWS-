import json
import boto3
import os
from datetime import datetime
import psycopg2
from botocore.exceptions import ClientError

# PostgreSQL connection setup
def get_db_connection():
    return psycopg2.connect(
        host=os.environ['PG_HOST'],
        port=os.environ['PG_PORT'],
        dbname=os.environ['PG_DATABASE'],
        user=os.environ['PG_USER'],
        password=os.environ['PG_PASSWORD']
    )

# Get all .json files from new_sentiment/
def get_sentiment_files(s3_client, bucket, prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' not in response:
            return []
        return [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]
    except ClientError as e:
        raise Exception(f"S3 list error: {e}")

# Insert each article row into PostgreSQL
def insert_articles(conn, articles):
    cursor = conn.cursor()
    inserted_count = 0

    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO news_sentiment (
                    published_at, source_name, title, description, sentiment_label
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                article.get('published_at'),
                article.get('source'),  # or source_name, based on your JSON
                article.get('title'),
                article.get('description'),
                article.get('sentiment_label')
            ))
            inserted_count += 1
        except Exception as e:
            print(f"Failed to insert article: {article.get('title')}\nError: {str(e)}")

    conn.commit()
    cursor.close()
    return inserted_count

# Lambda handler
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = "newsapi-s3"
    input_prefix = "new_sentiment/"

    try:
        file_keys = get_sentiment_files(s3, bucket_name, input_prefix)
        if not file_keys:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No files to process'})
            }

        conn = get_db_connection()

        # Step 1: Clear the table before inserting
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM news_sentiment;")
            conn.commit()
            print("Cleared old data from news_sentiment table")

        total_inserted = 0
        processed_files = []

        # Step 2: Insert new articles
        for key in file_keys:
            obj = s3.get_object(Bucket=bucket_name, Key=key)
            articles = json.loads(obj['Body'].read().decode('utf-8'))

            print(f"Found {len(articles)} articles in {key}")

            inserted_count = insert_articles(conn, articles)
            total_inserted += inserted_count
            processed_files.append(key)

            s3.delete_object(Bucket=bucket_name, Key=key)
            print(f"Deleted processed file: {key}")

        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Replaced table with {total_inserted} new articles from S3',
                'processed_files': processed_files,
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
