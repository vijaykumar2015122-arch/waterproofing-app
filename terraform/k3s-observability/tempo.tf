resource "helm_release" "tempo" {
  name       = "tempo"
  repository = "https://grafana-community.github.io/helm-charts"
  chart      = "tempo"
  version    = "3.2.1"

  namespace = kubernetes_namespace_v1.observability.metadata[0].name

  values = [
    file("${path.module}/tempo-values.yaml")
  ]

  wait    = true
  timeout = 600
}
