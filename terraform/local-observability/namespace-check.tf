data "kubernetes_namespace_v1" "existing_default" {
  metadata {
    name = "default"
  }
}
