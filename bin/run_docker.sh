#/bin/bash

# Run the docker container
docker run --rm -p 127.0.0.1:5000:5000 --env APP_SECRET_KEY=192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf local/app:latest
