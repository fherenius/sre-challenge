# $REGISTRY variable is set in github actions by default
variable "REGISTRY" {
    default = "$REGISTRY"
}

group "default" {
    targets = [
        "app"
    ]
}

target "app" {
    dockerfile = "Dockerfile"
    tags = [
        "${REGISTRY}/app:latest"
    ]
}

