FROM node:lts-alpine

# install simple http server for serving static content
RUN npm install -g http-server
WORKDIR /SkaldbotUI

COPY package*.json ./

RUN npm install
RUN npm audit fix
COPY . .
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]