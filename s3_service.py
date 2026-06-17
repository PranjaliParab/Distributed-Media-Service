import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

load_dotenv()  # .env file madhe credentials astat

# AWS credentials .env madhu yeto
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# S3 client banav
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


def upload_file_to_s3(local_file_path: str, s3_folder: str = "processed") -> str:
    """
    Local file la S3 bucket var upload karto.
    s3_folder: S3 madhe konata folder (e.g. "processed/images")
    Returns: Public URL of uploaded file
    """
    filename = os.path.basename(local_file_path)
    s3_key = f"{s3_folder}/{filename}"   # S3 madhe path

    try:
        s3_client.upload_file(
            local_file_path,
            S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ACL": "public-read"}  # Public access
        )
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        print(f"[S3] Uploaded: {file_url}")
        return file_url

    except NoCredentialsError:
        print("[S3] Error: AWS credentials milale nahi!")
        raise
    except ClientError as e:
        print(f"[S3] Error: {e}")
        raise


def generate_presigned_url(s3_key: str, expiry_seconds: int = 3600) -> str:
    """
    Private file sathi temporary URL banav (expiry_seconds nantar expire hoto).
    """
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=expiry_seconds
    )
    print(f"[S3] Pre-signed URL: {url}")
    return url