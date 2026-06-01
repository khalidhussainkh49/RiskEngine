# Business Requirement Specification (BRS)
## Project: Nigeria Customs Declaration Intelligence & Profiling System (NCDIPS)

### 1. Executive Summary
The NCDIPS is a production-grade intelligence platform designed to enhance the risk management capabilities of the Nigeria Customs Service. By analyzing declaration data from the Bodogwu platform, the system identifies anomalies, suspicious trade patterns, and financial risks through a combination of rules, statistical profiling, and machine learning.

### 2. Objectives
- **suspicion Scoring**: Quantify the risk of every declaration based on historical and semantic patterns.
- **Valuation Intelligence**: Detect under-valuation and over-valuation using statistical z-scores.
- **Entity Profiling**: Resolve disparate company names into canonical identities to track behavior over time.
- **Explainability**: Provide human-readable justifications for every risk flag to assist analysts.

### 3. Functional Requirements
#### FR1: Data Ingestion
- Real-time polling of Bodogwu SGD APIs.
- Support for incremental synchronization and historical backfill.
- Deduplication and raw JSON preservation.

#### FR2: Risk Engine
- Hybrid rules-based scoring (e.g., zero weights, new importers).
- HS code semantic validation comparing commercial descriptions to official ontologies.
- Statistical valuation profiling by HS code and unit type.

#### FR3: Intelligence Workflows
- High-risk queue for analyst review.
- Detailed declaration view with risk breakdowns and entity history.
- Global search for declarations, companies, and HS codes.

#### FR4: Graph Intelligence
- Visualizing relationships between importers, exporters, brokers, and containers.
- Detecting suspicious trade rings and shell company patterns.

### 4. Non-Functional Requirements
- **Scalability**: Support for millions of historical declarations.
- **Latency**: Sub-second response time for search and dashboard filtering.
- **Auditability**: Complete logging of all analyst actions and system decisions.
- **Security**: Role-Based Access Control (RBAC) and encrypted data transmission.
