provider "kubernetes" {
  config_path = "/home/vijay/.kube/k3s-config"
}

provider "helm" {
  kubernetes {
    config_path = "/home/vijay/.kube/k3s-config"
  }
}
