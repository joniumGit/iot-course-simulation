FROM node:17-alpine
WORKDIR /home/node/app
COPY ./package*.json .
RUN npm install
CMD [ "npx", "nodemon", "app.js" ]