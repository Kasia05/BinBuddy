import glob
import os
from colorama import Fore, Style
from google.cloud import storage
from binbuddy.params import *
from tensorflow import keras

def load_model() -> keras.Model:
    """
    Return a saved model:
    - locally (latest one i`n alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'

    Return None (but do not Raise) if no model is found

    """

    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

        # Define the relative path to the local model directory
        local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
        local_model_paths = glob.glob(f"{local_model_directory}/*")

        print(f"Searching for models in directory: {local_model_directory}")
        print(f"Found paths: {local_model_paths}")

        if not local_model_paths:
            print(Fore.RED + f"\nNo local model was found..." + Style.RESET_ALL)
            return None

        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

        print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

        latest_model = keras.models.load_model(most_recent_model_path_on_disk)

        print(f"✅ Model loaded from local disk {most_recent_model_path_on_disk}")

        return latest_model

    elif MODEL_TARGET == "gcs":
        # 🎁 We give you this piece of code as a gift. Please read it carefully! Add a breakpoint if needed!
        print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

        client = storage.Client()
        blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))

        try:
            latest_blob = max(blobs, key=lambda x: x.updated)
            latest_model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, "models", latest_blob.name)
            latest_blob.download_to_filename(latest_model_path_to_save)
            latest_model = keras.models.load_model(latest_model_path_to_save)
            print(f"✅ Latest model downloaded from cloud storage {latest_blob.name} and loaded successfully!")
            return latest_model
        except:
            print(f"\n❌ No model found in GCS bucket {BUCKET_NAME}")

            return None
    else:
        return None
