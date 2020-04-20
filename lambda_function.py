import os
import sys
import json
import logging
from parser import parse_sql
from read_secret import get_secret
import boto3
import botocore
import pymysql


#rds settings
user, password, host, db_name, db_port = get_secret()

region_name = os.environ.get("REGION_NAME", "")

# Resource S3
s3 = boto3.resource('s3', region_name=region_name,
                    config=botocore.config.Config(s3={'addressing_style': 'path'}))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host, user=user,
                           passwd=password, db=db_name, port=db_port, connect_timeout=10)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def lambda_handler(event, context):
    """
    This function runs sql scripts in MySQL RDS instance
    """

    bucket_name = os.environ.get('BUCKET_NAME', "")

    key = event['Records'][0]['s3']['object']['key']

    object = s3.Object(bucket_name, key=key)
    file_stream = object.get()['Body'].read()

    stmts = parse_sql(file_stream)

    with conn.cursor() as cur:
        for stmt in stmts:
            cur.execute(stmt)

        conn.commit()

    logger.info("INFO: SQL script successfully submitted")

    return json.dumps({'status': 'SQL script successfully submitted'})


if __name__ == '__main__':
    print(lambda_handler('', ''))
