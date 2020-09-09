#!/bin/bash
args=("$@")
node_version=${args[0]} 
command=${args[@]:1}

docker run \
  -it \ # Stay keep interactive console.
  --rm \ # Automatically remove the container when it exits.
  --name local-nodejs-version-${node_version}-bin \ # Assign a name to the container.
  --user $(id -u):$(id -g) \
  -v $PWD:/usr/src/app:delegated \
  -w /usr/src/app \
  --network="host" \
  node:${node_version} ${command}