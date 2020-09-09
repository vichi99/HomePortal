#!/bin/bash
docker-compose down -v
docker-compose -f docker-compose.dev.yaml down -v
docker rm $(docker ps -a -f status=exited -q)
docker rmi $(docker images -a -q)
docker volume prune -f
docker system df