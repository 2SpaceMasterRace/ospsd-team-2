from aws_client_impl import S3Client
from cloud_storage_client_api import CloudStorageClient


def main() -> None:
    client: CloudStorageClient = S3Client(bucket_name="my-bucket")
    print(f"Created client: {client}")
    print("Hello from Team 2!")


if __name__ == "__main__":
    main()
