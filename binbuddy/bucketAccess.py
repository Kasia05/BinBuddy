from google.cloud import storage
from google.api_core.exceptions import Forbidden, NotFound
from params import *

def check_bucket_access(bucket_name):
    client = storage.Client()
    try:
        # Attempt to get the bucket metadata
        bucket = client.get_bucket(bucket_name)
        print(f"Access to bucket '{bucket_name}' verified.")
        return True
    except NotFound:
        print(f"Bucket '{bucket_name}' does not exist.")
        return False
    except Forbidden:
        print(f"Access to bucket '{bucket_name}' is forbidden.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
if __name__ == "__main__":
    # Load environment variables from .env file (if applicable)
    # If you're not using .env file, make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    print(f"Bucket name: {BUCKET_NAME}")
    bucket_name = BUCKET_NAME
    print(f"Using bucket name: {bucket_name}")

    has_access = check_bucket_access(bucket_name)
    print(f"Access status: {has_access}")
