FROM node:22-alpine

COPY web /app/
WORKDIR /app

RUN npm install
RUN npm run build
CMD node ./dist/server/entry.mjs
EXPOSE 4321