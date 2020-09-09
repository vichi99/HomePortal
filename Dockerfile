FROM node:12-alpine as frontend-dev
LABEL maintainer umpalumpa
COPY frontend/ /app
WORKDIR /app
RUN yarn install
ENTRYPOINT ["./startup.sh"]