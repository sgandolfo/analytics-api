## Docker

- `docker build -t analytics-api -f Dockerfile.web .`
- `docker run analytics-api`

become

- `docker compose up --watch`
- `docker compose down` or `docker compose down -v` (to remove volumes)
