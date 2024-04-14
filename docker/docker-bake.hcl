# $REGISTRY variable is set in github actions by default
variable "REGISTRY" {
    default = "$REGISTRY"
}

variable "IMAGE_NAME" {
    default = "app"
}

variable "REPOSITORY" {
    default = "${REGISTRY}/${IMAGE_NAME}
}

group "default" {
    targets = [
        "app"
    ]
}

target "app" {
    dockerfile = "Dockerfile"
    tags = [
        "${REPOSITORY}:latest"
    ]
    contexts = {
        "src" = "../app/"
    }
}

