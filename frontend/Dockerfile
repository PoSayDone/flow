FROM node:21-alpine AS builder

ARG VITE_API_URL
ARG VITE_IMAGES_URL

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_IMAGES_URL=$VITE_IMAGES_URL

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn --frozen-lockfile
COPY . .
RUN yarn run build

FROM node:21-alpine
WORKDIR /app
COPY --from=builder /app/build build/

COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]
