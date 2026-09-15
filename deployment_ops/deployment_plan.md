# Deployment Plan

## Environments
- **Pilot:** single-tenant Docker Compose deployment (extraction/reconciliation service + audit log store),
  matching the `docker-compose.yml` pattern from `multi-agent-support-capstone`.
- **Production (post-pilot):** see `productization/productization_recommendations.md` for the path to a
  queue-backed, horizontally-scaled deployment.

## Secrets
All credentials (SharedLLM gateway API key, database connection strings) are supplied via environment
variables. `.env` is gitignored; `.env.example` documents every required variable with no real values.

## Scaling Path
1. **Pilot:** single container processing invoices synchronously as they arrive — sufficient for the pilot's
   single vendor segment and volume.
2. **Growth:** introduce a message queue (invoice-received events) in front of the extraction service so
   multiple worker instances can process invoices in parallel as volume grows beyond the pilot segment.
3. **Scale:** horizontally scale extraction workers independently of the reconciliation engine (extraction is
   the LLM-bound, higher-latency step; reconciliation is fast and rarely the bottleneck).

## Rollback
- The extraction prompt and model version are pinned and versioned alongside the code (no silent model
  upgrades). A bad deploy (accuracy regression caught by the golden-dataset gate) is rolled back by reverting
  to the prior pinned container image/prompt version.
- Because every decision is audit-logged with the prompt/model version that produced it, a rollback's impact
  can be scoped precisely to the affected time window.
