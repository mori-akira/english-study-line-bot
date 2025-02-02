import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name: str, region_name: str = "ap-northeast-1"):
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return get_secret_value_response['SecretString']


if __name__ == '__main__':
    print(get_secret("englishStudyBot"))
