variable "billing_project" {
  description = "The project to bill for all the resources"
  type        = string
}

variable "project_id" {
  description = "The project to create resources in"
  type        = string
}

variable "location" {
  description = "The location to create the search engine in"
  type        = string
  default     = "global"
}

variable "region" {
  description = "The region to create resources in"
  type        = string
  default     = "us-central1"
}

variable "data_store_id" {
  description = "The ID of the data store"
  type        = string
}

variable "data_store_display_name" {
  description = "The display name of the data store"
  type        = string
}

variable "bucket_name" {
  description = "The name of the GCS bucket to use as a data source"
  type        = string
}

variable "search_engine_id" {
  description = "The ID of the search engine"
  type        = string
}

variable "search_engine_display_name" {
  description = "The display name of the search engine"
  type        = string
}

variable "collection_id" {
  description = "The ID of the collection"
  type        = string
}
