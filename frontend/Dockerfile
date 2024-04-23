FROM node:21-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn --frozen-lockfile
COPY . .
RUN yarn run build

FROM node:21-alpine
WORKDIR /app
COPY --from=builder /app/build build/
# COPY --from=builder /app/node_modules node_modules/
COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]
