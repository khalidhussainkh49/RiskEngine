# API Documentation

### 1. Base URL
`http://api.ncdips.gov.ng/api/v1`

### 2. Authentication
Bearer Token (JWT) required for all endpoints except `/auth/login`.

---

### 3. Declarations
#### GET `/declarations/`
List recent declarations.
- **Query Params**: `page`, `page_size`, `min_score`, `importer_id`.
- **Response**: Array of Declaration objects.

#### GET `/declarations/{sgd_id}`
Get full details including items and risk findings.
- **Response**:
```json
{
  "sgd_id": "...",
  "status": "risk_assessed",
  "importer": { "name": "...", "tin": "..." },
  "risk_scores": { "overall_score": 84.5 },
  "risk_findings": [
    {
      "category": "Valuation",
      "severity": "High",
      "message": "Suspicious undervaluation",
      "explanation": "..."
    }
  ],
  "items": [...]
}
```

---

### 4. Search
#### GET `/search/`
Full-text search across entities and declarations.
- **Query Params**: `q` (string).

---

### 5. Analytics
#### GET `/analytics/overview`
Aggregated stats for the dashboard.

#### GET `/analytics/valuation-trends`
Historical unit price distribution for an HS code.
