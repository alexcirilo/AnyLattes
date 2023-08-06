version: '2.4'

services:
  anylattes:
    build: .
    container_name: anylattes
    ports:
      - '5000:5000'
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
    container_name: redis