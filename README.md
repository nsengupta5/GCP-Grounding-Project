# Searching with Vertex AI and Datastore

# Introduction
This is a mini project exploring the use of Vertex AI and Datastore to build a search engine where the knowledge base can be dynamically updated. The purpose of this project is to demonstrate how Datastore can be used to store and retrieve data, and how Vertex AI can be used to build a search engine.

This project will use PDF files on research papers on data intensive systems as the knowledge base. The PDF files will be stored in a GCS bucket, which will be used to populate the Datastore. The search engine will be built using Vertex AI. However, note that the source for the knowledge base can be any other source, including web pages, BigQuery, APIs, etc. 

# Instructions

## Setup Option 1: Run the project locally

### Prerequisites
- Python 3.9+
- GCP account
- Terraform
- Google Cloud SDK (with application-default credentials)

### Steps
1. Select or create a GCP project. Note the project ID
2. Ensure that billing is enabled for your project
3. Set the project ID:
```
gcloud config set project <PROJECT_ID>
```
4. Modify the `terraform.tfvars` file with the appropriate values for:
- `project_id`
- `billing_project`
- `bucket_name`
5. Create a Python virtual environment:
```
python3 -m venv env
source env/bin/activate
```
6. Install the required Python packages:
```
pip install -r requirements.txt
```

## Setup Option 2: Run the project in a Docker container

### Prerequisites
- Docker
- GCP account

### Steps
1. Select or create a GCP project. Note the project ID
2. Ensure that billing is enabled for your project
3. Run the Docker container:
```
docker run -it --rm gcp-datastore-demo /bin/bash
```
4. Authenticate with GCP:
```
gcloud auth login
```
5. Load application credentials:
```
gcloud auth application-default login
```
6. Set the project ID:
```
gcloud config set project <PROJECT_ID>
```
7. Modify the `terraform.tfvars` file with the appropriate values for:
- `project_id`
- `billing_project`
- `bucket_name`

```
nano terraform.tfvars
```
The remaining values can be left as is, unless you want to change them.

## Deployment
1. Create the resources using Terraform:
```
terraform plan -out "tfplan"
terraform apply "tfplan"
```
2. Run the Python script to populate the GCS bucket and Datastore:
```
python3 populate_datastore.py
```

## Interact with the Datastore
- Navigate to the Agent Builder in the GCP console

## Cleanup
1. If using a new project, delete the project:
```
gcloud projects delete <PROJECT_ID>
```
2. If using an existing project, delete the resources:
```
terraform plan -destroy -out "tfplan-destroy"
terraform apply "tfplan-destroy"
```
