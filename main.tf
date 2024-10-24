terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.0.0"
    }
  }
  required_version = ">= 0.13"
}

provider "google" {
  project               = var.project_id
  billing_project       = var.billing_project
  region                = var.region
  user_project_override = true
}

# Enable the Discovery Engine API 
resource "google_project_service" "discovery_engine_api" {
  project = var.project_id
  service = "discovery.googleapis.com"

  disable_on_destroy = false
}

# Enable the Vertex AI API
resource "google_project_service" "vertex_ai_api" {
  project = var.project_id
  service = "aiplatform.googleapis.com"

  disable_on_destroy = false
}

# Create a Data Store
resource "google_discovery_engine_data_store" "basic" {
  location          = "global"
  data_store_id     = "data-intensive-store-id"
  display_name      = "data-intensive-store"
  industry_vertical = "GENERIC"
  solution_types    = ["SOLUTION_TYPE_SEARCH"]
  content_config    = "CONTENT_REQUIRED"
}

# Create a Search Engine
resource "google_discovery_engine_search_engine" "basic" {
  engine_id      = "data-intensive-search-engine-id"
  collection_id  = "default_collection"
  location       = google_discovery_engine_data_store.basic.location
  display_name   = "data-intensive-search-engine"
  data_store_ids = [google_discovery_engine_data_store.basic.data_store_id]
  search_engine_config {
    search_tier    = "SEARCH_TIER_ENTERPRISE"
    search_add_ons = ["SEARCH_ADD_ON_LLM"]
  }
}

# Create a GCS Data Source
resource "google_storage_bucket" "data_source" {
  name                        = "data-intensive-paper-source"
  location                    = var.region
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}
