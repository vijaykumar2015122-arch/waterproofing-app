resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "92.16.2"

  namespace = kubernetes_namespace_v1.observability.metadata[0].name

  values = [
    file("${path.module}/prometheus-values.yaml")
  ]

  wait    = true
  timeout = 600
}
