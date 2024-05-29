import zipfile
from io import BytesIO
import os
from PIL import Image
from google.cloud import storage
from tqdm import tqdm
from binbuddy.params import *


def check_existing_data(directory):
    # Check if the directory exists and contains files
    return os.path.exists(directory) and any(os.scandir(directory))

def load_images(bucket_name = BUCKET_NAME,
                                      zip_blob_name=BLOB_NAME,
                                      extract_to='raw_data'):

    if check_existing_data(extract_to):
        print(f"Data already exists in {extract_to}. Skipping download.")
        return load_images_from_directory(extract_to)

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

    # Initialize a client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the blob
    blob = bucket.blob(zip_blob_name)

     # Check if the blob exists
    if not blob.exists():
        raise FileNotFoundError(f"The blob {zip_blob_name} does not exist in the bucket {bucket_name}.")

    # Get the size of the blob for the progress bar
    blob.reload()  # Ensure the blob metadata is loaded
    blob_size = blob.size

    if blob_size is None:
        raise ValueError("Unable to determine the size of the blob.")

    # Get the size of the blob for the progress bar
    blob_size = blob.size

    # Download the zip file in chunks with progress indicator
    chunk_size = 1024 * 1024 * 100 # 100 MB
    zip_data = BytesIO()

    with tqdm(total=blob_size, unit='B', unit_scale=True, desc=zip_blob_name) as pbar:
        start = 0
        while start < blob_size:
            end = min(start + chunk_size, blob_size)
            chunk = blob.download_as_bytes(start=start, end=end-1)
            zip_data.write(chunk)
            pbar.update(len(chunk))
            start = end

    zip_data.seek(0)  # Reset the buffer position to the beginning

    # Create a directory to extract images
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Extract the zip file
    with zipfile.ZipFile(zip_data, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    images = load_images_from_directory(extract_to)
    print(f'Extracted and loaded {len(images)} images')
    return images

def load_images_from_directory(directory):
    # Load images from the extracted files
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg')):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        images.append(img.copy())
                except Exception as e:
                    print(f"Error loading image {file_path}: {e}")
    return images
