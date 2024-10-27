# GCP-Grounding-Project
A mini project exploring grounding in Vertex AI

# Instructions
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
vim terraform.tfvars
```

The remaining values can be left as is, unless you want to change them.

8. Plan the Terraform deployment:
```
terraform plan -out "tfplan"
```
9. Apply the Terraform deployment:
```
terraform apply "tfplan"
```
This will create the necessary resources in GCP.

10. Run the Python script to populate the GCS bucket and Datastore:
```
python3 populate_datastore.py
```
