provider "kubernetes" {
  config_path = "/home/vijay/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "/home/vijay/.kube/config"
  }
}
