resource "kubernetes_namespace_v1" "observability" {
  metadata {
    name = "observability"

    labels = {
      purpose    = "monitoring"
      managed_by = "terraform"
    }
  }
}
