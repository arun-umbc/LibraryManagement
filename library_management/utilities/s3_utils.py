import boto3
from django.conf import settings


def generate_presigned_url(key_name, bucket):
    s3 = boto3.client('s3',
                      region_name='us-east-1',
                      endpoint_url='https://s3.amazonaws.com'
                      )
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key_name
        },
        ExpiresIn=172800,
    )
    return url


def upload_to_s3(file, file_path, bucket):
    upload_path = 'media/' + file_path
    try:
        s3 = boto3.client(
            "s3"
        )
        s3.upload_file(
            file,
            bucket,
            upload_path
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e
    return settings.MEDIA_URL + file_path
