import boto3
import datetime
import numpy as np
import base64

s3 = boto3.client('s3',region_name = 'us-east-1')

def getBucket():    
    return [bucket['Name'] for bucket in s3.list_buckets()['Buckets'] \
         if 'si3mshady' in bucket['Name']][0]


def decodeImage(_bytes):    
    return np.frombuffer(_bytes, np.uint8)   

def s3PutObject(bucket, fileObj):
    today = datetime.datetime.now()
    date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
    response = s3.put_object(
        ACL='public-read',
        Body=fileObj,
        Bucket=bucket,
        ContentType='image/png',
        Key=f'test-{date_time}.png' )

def lambda_handler(event, context):
    for record in event['Records']:
        #Kinesis data is base64 encoded so decode here
        decodedData=base64.b64decode(record["kinesis"]["data"])
        decodedImageData = decodeImage(decodedData)
        print("Decoded Numpy Array " + str(decodedImageData))
        bucket = getBucket()
        s3PutObject(bucket,decodedData)

    
  
