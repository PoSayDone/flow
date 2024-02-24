# FROM oven/bun:1 as base
# WORKDIR /usr/src/app
#
# FROM base AS install
# COPY package.json bun.lockb .
# RUN bun install --frozen-lockfile
#
# COPY . .

FROM node:18-alpine AS builder
WORKDIR /usr/src/app
COPY package.json .
RUN yarn --frozen-lockfile
COPY . .
