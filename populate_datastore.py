"""
File: populate_datastore.py
Author: Nikhil Sengupta
Created On: 25-10-2024
Last Updated On: 27-10-2024
Email: nikhil.sengupta10@proton.me

Description: This script uploads files from a local directory to a Cloud Storage bucket,
             and then imports the documents from the bucket to a Datastore.
"""

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1alpha as discoveryengine
from google.cloud import storage
from google.cloud.storage import transfer_manager
from pathlib import Path
from helper import get_tfvars
import logging

# Path to the directory containing the files to upload
# You can change this to the path of the directory containing the files
# you want to upload
DATASOURCE_PATH = "./DataIntensivePapers"


def upload_files(bucket_name: str, source_dir: str):
    """
    Uploads files from a local directory to a Cloud Storage bucket.

    Args:
        bucket_name (str): The name of the Cloud Storage bucket.
        source_dir (str): The path to the local directory containing the files to upload.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get all files in the directory
    directory_as_path = Path(source_dir)
    paths = directory_as_path.rglob("*")

    # Filter out directories
    file_paths = [path for path in paths if path.is_file()]

    # Get the filenames
    string_paths = [str(path).split("/")[-1] for path in file_paths]

    logging.info(f"Uploading files to {bucket_name}...")
    results = transfer_manager.upload_many_from_filenames(
        bucket, string_paths, source_directory=source_dir, max_workers=8
    )

    for name, result in zip(string_paths, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.
        if isinstance(result, Exception):
            logging.error(
                "Failed to upload {} due to exception: {}".format(name, result)
            )
        else:
            logging.info("Uploaded {} to {}.".format(name, bucket.name))


def import_documents(
    project_id: str,
    location: str,
    data_store_id: str,
    bucket_name: str,
):
    """
    Imports documents from a Cloud Storage bucket to a Datastore.

    Args:
        project_id (str): The project ID.
        location (str): The location of the Datastore.
        data_store_id (str): The Datastore ID.
        bucket_name (str): The name of the Cloud Storage

    Returns:
        str: The operation name of the import operation.
    """
    # Create a client
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoverengine.googleapis.com")
        if location != "global"
        else None
    )
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # Full resource name of the search engine branch
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    source_documents = [f"gs://{bucket_name}/*"]

    # Create the request
    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=source_documents, data_schema="content"
        ),
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    logging.info(f"Importing documents from gs://{bucket_name}...")
    operation = client.import_documents(request=request)
    logging.info("Import operation started")

    try:
        operation.result()
        logging.info("Import operation completed successfully")
    except Exception as e:
        logging.error(f"Long running operation: {e}")

    discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    return operation.operation.name


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s %(levelname)s - %(message)s"
    )
    tfvars = get_tfvars("terraform.tfvars")
    upload_files(tfvars["bucket_name"], DATASOURCE_PATH)
    import_documents(
        tfvars["project_id"],
        tfvars["location"],
        tfvars["data_store_id"],
        tfvars["bucket_name"],
    )
