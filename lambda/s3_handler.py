import json

def lambda_handler(event, context):
    results = []
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key    = record['s3']['object']['key']
        size   = record['s3']['object'].get('size', 0)
        print(f"[S3 TRIGGER] New file: s3://{bucket}/{key} ({size} bytes)")
        results.append({"bucket": bucket, "key": key, "size": size})
    return {"statusCode": 200, "processed": results}
