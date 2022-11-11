get-content .env | ForEach-Object {
    if ($_) {
        $name, $value = $_.split('=')
        set-content env:\$name $value
    }
    
}

$img = docker images -q ${env:DOCKER_IMAGE_NAME}

if (-Not $img ) {
    docker build --tag ${env:DOCKER_IMAGE_NAME} .
}
Write-Output "RUNNING ON PORT: ${env:FLASK_DOCKER_PORT}"
docker run -v ${env:WINDOWS_DOCKER_DB_PATH}:/src/instance --publish ${env:FLASK_DOCKER_PORT}:5000 ${env:DOCKER_IMAGE_NAME}