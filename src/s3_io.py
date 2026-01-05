import boto3

class S3Client:
    def __init__(self, bucket: str, prefix: str = "raw"):
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        self.s3 = boto3.client("s3")

    def upload_file(self, local_path: str, filename: str) -> str:
        key = f"{self.prefix}/{filename}"
        self.s3.upload_file(local_path, self.bucket, key)
        return f"s3://{self.bucket}/{key}"

