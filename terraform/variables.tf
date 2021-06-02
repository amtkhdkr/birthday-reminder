variable "zone" {
  description = "The zone in which to create the Kubernetes cluster. Must match the region"
  type        = string
}

variable "project" {
  description = "the project for this network"
  type        = string
}