# System Architecture & Software Design Document (SDD)

### 1. Architectural Overview
NCDIPS follows a modular, event-driven architecture designed for high throughput and intelligence depth.

#### Components:
- **FastAPI Backend**: Provides high-performance async REST APIs.
- **Celery Worker**: Handles long-running ingestion and risk-scoring tasks.
- **Next.js Frontend**: React-based dashboard for real-time visualization.
- **Data Layers**:
  - **PostgreSQL/PostGIS**: Relational storage for declarations and geospatial data.
  - **Neo4j**: Graph database for entity relationship discovery.
  - **Elasticsearch**: Full-text and semantic search indexing.
  - **Redis**: Message broker and caching layer.

### 2. Data Models
#### Relational Schema (PostgreSQL)
- `declarations`: Core SGD metadata.
- `goods_items`: Line items with weights, values, and HS codes.
- `companies`: Normalized entity profiles with canonical resolution.
- `risk_scores`: Aggregate scoring and breakdown.
- `risk_findings`: Individual anomalies with evidence and explanations.

#### Graph Schema (Neo4j)
- Nodes: `Declaration`, `Company`, `Container`, `Vessel`.
- Edges: `HAS_IMPORTER`, `HAS_CONTAINER`, `LINKED_TO` (for multi-declaration entities).

### 3. Intelligence Engines
#### Valuation Engine
- Uses **Z-Score Analysis** on historical unit prices.
- Flags declarations falling outside the 95% confidence interval for a specific HS code.

#### HS Validation Engine
- Uses **Sentence Embeddings** (MiniLM-L6-v2) to calculate cosine similarity.
- Flags mismatches between commercial descriptions and official HS descriptions.

#### Anomaly ML
- **Isolation Forest** model trained on features like CIF-to-Weight ratios and frequency of amendments.

### 4. Security Design
- **Authentication**: JWT-based stateless authentication.
- **RBAC**: Roles (Admin, Analyst, Supervisor) enforced at the API route level.
- **Audit Trails**: Every write operation is logged with a user ID and timestamp.
