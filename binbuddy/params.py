import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

##################  VARIABLES  ##################
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_PROJECT_WAGON = os.environ.get("GCP_PROJECT_WAGON")
GCP_REGION = os.environ.get("GCP_REGION")

BUCKET_NAME = os.environ.get("BUCKET_NAME")

BLOB_NAME = os.environ.get("BLOB_NAME")

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
