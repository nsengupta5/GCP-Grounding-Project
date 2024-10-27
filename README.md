# GCP-Grounding-Project
A mini project exploring grounding in Vertex AI

# Instructions

## Prerequisites
- Docker
- GCP account

## Setup
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
