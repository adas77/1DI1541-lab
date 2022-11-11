get-content .env | ForEach-Object {
    if ($_) {
        $name, $value = $_.split('=')
    }
    set-content env:\$name $value
}

# use sudo: https://support.circleci.com/hc/en-us/articles/360045816254-How-to-sudo-on-Powershell-Windows-executor
$img = sudo docker images -q ${env:DOCKER_IMAGE_NAME}

# if (-Not $img ) {
#     sudo docker build --tag ${env:DOCKER_IMAGE_NAME} .
# }
sudo docker build --tag ${env:DOCKER_IMAGE_NAME} .
Write-Output "RUNNING ON PORT: ${env:FLASK_DOCKER_PORT}"
sudo docker run -v ${env:DOCKER_DB_PATH}:/src/instance --publish ${env:FLASK_DOCKER_PORT}:5000 ${env:DOCKER_IMAGE_NAME}