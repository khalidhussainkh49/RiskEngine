# Analyst Workflow & Intelligence Guide

### 1. The High-Risk Queue
Analysts should begin their day at the High-Risk Queue. This view prioritizes declarations with an overall score > 75.
- **Sort by**: Score (Descending).
- **Goal**: Review "Critical" findings before shipments are cleared.

### 2. Interpreting Risk Findings
Each finding includes **Explainable AI (XAI)** metadata.
- **Valuation Findings**: Check the "Historical Pattern" chart. If the declared value is an outlier but the importer has a clean history, it may be a one-off error. If the importer is a repeat offender, flag for manual inspection.
- **HS Mismatch**: View the semantic similarity score. A score < 0.3 strongly suggests misclassification to avoid higher duty rates.

### 3. Using Graph Intelligence
Click on an Importer or Broker name to view the relationship graph.
- **Look for**: A single phone number or address linked to multiple RC numbers (Company IDs). This is a hallmark of "phoenix companies" or trade rings.
- **Identify**: Clusters of companies sharing the same bank and vessel, even if they appear unrelated on paper.

### 4. Tagging & Notes
Analysts can add intelligence remarks. These notes are preserved and factor into the future risk scores of the entities involved.
