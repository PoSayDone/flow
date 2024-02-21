FROM oven/bun:1 as base
WORKDIR /usr/src/app

FROM base AS install
COPY package.json bun.lockb .
RUN bun install --frozen-lockfile

COPY . .
