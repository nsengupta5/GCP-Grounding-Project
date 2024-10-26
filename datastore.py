from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1alpha as discoveryengine
from google.cloud import storage
from google.cloud.storage import transfer_manager
from pathlib import Path
from helper import get_tfvars

import logging

DATASOURCE_PATH = "./DataIntensivePapers"


def upload_files(bucket_name: str, source_dir: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    directory_as_path = Path(source_dir)
    paths = directory_as_path.rglob("*")

    file_paths = [path for path in paths if path.is_file()]

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
        response = operation.result()
        logging.info("Import operation completed successfully")
    except Exception as e:
        logging.error(f"Long running operation: {e}")

    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    return operation.operation.name


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s %(levelname)s - %(message)s"
    )
    tfvars = get_tfvars("terraform.tfvars")
    print(tfvars)
    upload_files(tfvars["bucket_name"], DATASOURCE_PATH)
    import_documents(
        tfvars["project_id"],
        tfvars["location"],
        tfvars["data_store_id"],
        tfvars["bucket_name"],
    )
