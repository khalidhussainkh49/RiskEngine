# Production Deployment & Operations Guide

### 1. Prerequisites
- Docker & Docker Compose
- 16GB+ RAM (Elasticsearch and Neo4j requirements)
- SSL Certificates for domain-bound deployment

### 2. Quick Start
```bash
# Clone and enter repo
git clone ...
cd ncdips

# Build and start services
docker-compose up -d --build
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```
POSTGRES_PASSWORD=secret_db_pass
SECRET_KEY=long_random_string_for_jwt
NEO4J_PASSWORD=secret_graph_pass
BODOGWU_API_KEY=your_api_key
```

### 4. Database Migrations
The system uses Alembic for PostgreSQL:
```bash
docker-compose exec backend alembic upgrade head
```

### 5. Observability
- **Logs**: `docker-compose logs -f backend`
- **Health Check**: `GET /health` on the backend port.
- **Monitoring**: Integration with Prometheus/Grafana is recommended for tracking queue latency and risk engine processing times.
