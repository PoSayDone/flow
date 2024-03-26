FROM node:21-alpine AS builder
WORKDIR /usr/src/app
COPY package.json yarn.lock .
RUN yarn --frozen-lockfile
COPY . .
