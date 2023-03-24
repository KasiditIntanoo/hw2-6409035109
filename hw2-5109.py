#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import boto3
import botocore
#import pandas as pd
#from IPython.display import display, Markdown

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

def create_bucket(bucket):
    import logging

    try:
        s3.create_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        return 'Bucket ' + bucket + ' could not be created.'
    return 'Created or already exists ' + bucket + ' bucket.'

#create_bucket('nyctlc-cs653-5109')
#ถ้าไม่มี bucket ต้องใช้คำสั่งนี้

def copy_among_buckets(from_bucket, from_key, to_bucket, to_key):
    s3_resource.meta.client.copy({'Bucket': from_bucket, 'Key': from_key},
                                        to_bucket, to_key)
    print(f'File {to_key} saved to S3 bucket {to_bucket}')

#copy_among_buckets(from_bucket='nyc-tlc', from_key='trip data/yellow_tripdata_2017-01.parquet',
#                      to_bucket='nyctlc-cs653-5109',to_key='yellow_tripdata_2017-01.parquet')

#copy_among_buckets(from_bucket='nyc-tlc', from_key='trip data/yellow_tripdata_2017-02.parquet',
#                     to_bucket='nyctlc-cs653-5109',to_key='yellow_tripdata_2017-02.parquet')

#copy_among_buckets(from_bucket='nyc-tlc', from_key='trip data/yellow_tripdata_2017-03.parquet',
#                      to_bucket='nyctlc-cs653-5109',to_key='yellow_tripdata_2017-03.parquet')

#ส่วนของ Query

# Set up S3 Select parameters
query ="select * from s3object s  limit 10"
bucket = 'nyctlc-cs653-5109'
key = 'yellow_tripdata_2017-01.parquet'
expression_type = 'SQL'
input_serialization = {'Parquet': {}}
output_serialization = {'CSV': {}}

# Execute S3 Select query
response = s3.select_object_content(
    Bucket=bucket,
    Key=key,
    Expression=query,
    ExpressionType=expression_type,
    InputSerialization=input_serialization,
    OutputSerialization=output_serialization,
)

# Iterate through the response and print each line
for event in response['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)

