resource "helm_release" "otel_collector" {
  name       = "otel-collector"
  repository = "https://open-telemetry.github.io/opentelemetry-helm-charts"
  chart      = "opentelemetry-collector"
  version    = "0.178.1"

  namespace = kubernetes_namespace_v1.observability.metadata[0].name

  values = [
    file("${path.module}/otel-collector-values.yaml")
  ]

  wait    = true
  timeout = 600
}
