# $REGISTRY variable is set in github actions by default
variable "REGISTRY" {
    default = "local"
}

variable "IMAGE_NAME" {
    default = "app"
}

variable "REPOSITORY" {
    default = "${REGISTRY}/${IMAGE_NAME}"
}

variable "COMMIT_SMA" {
    default = "local"
}

group "default" {
    targets = [
        "app"
    ]
}

target "app" {
    dockerfile = "Dockerfile"
    tags = [
        "${REPOSITORY}:latest",
        "${REPOSITORY}:${COMMIT_SHA}",
    ]
    contexts = {
        "src" = "../app/"
    }
}

