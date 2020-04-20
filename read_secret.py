import os
import json
import logging
import boto3
import botocore


def get_secret():

    secret_name = os.environ.get("SECRET_NAME", "")
    region_name = os.environ.get("REGION_NAME", "")

    # Create a Secrets Manager client
    session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        config=botocore.config.Config(s3={'addressing_style': 'path'})
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        data = json.loads(get_secret_value_response['SecretString'])

        user = data['username']
        password = data['password']
        host = data['host']
        db = data['dbname']
        port = int(data['port'])

        return user, password, host, db, port
    except Exception as e:
        logging.error("Unable to read secrets")
        logging.error(e)
    return None, None, None, None, None


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_secret())
