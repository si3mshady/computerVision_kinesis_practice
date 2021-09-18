import boto3
import numpy as np


def getStream():
    kinesis = boto3.client('kinesis', region_name = 'us-east-1' )
    return kinesis, [stream for stream in  kinesis.list_streams(Limit=2)['StreamNames'] \
        if 'StreamShadyKinesis' in stream ][0]


def getBucket():
    s3 = boto3.client('s3')
    return s3, [bucket['Name'] for bucket in s3.list_buckets()['Buckets'] \
         if 'si3mshady' in bucket['Name']][0]


def decodeImage(strencode):
    return  np.frombuffer(strencode, np.uint8)   


