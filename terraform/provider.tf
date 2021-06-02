// Identifies allowable version range for Terraform Google Provider
provider "google" {
  project = var.project
  version = "~> 3.0.0"
}
