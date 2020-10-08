FROM node:12-alpine as homeportal-front-dev
LABEL maintainer jan
COPY frontend/ /app
WORKDIR /app
RUN yarn install
ENTRYPOINT ["./startup.sh"]