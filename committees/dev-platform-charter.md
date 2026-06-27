# Standing Committee 3: Developer Platform Charter

**Governed by:** Constitution Article VII
**Domain:** Developer experience, SDKs, plugin system, architecture documentation
**Bi-weekly meeting:** Wednesday 11:00 UTC

---

## COMMITTEE MANDATE

Make Sovereign CRM a platform, not just a product. Any developer should be able to set it up, extend it, integrate with it, and contribute to it within 5 minutes of first contact.

---

## TIME TO FIRST SUCCESS TARGETS

| Milestone | Target | Measurement |
|-----------|:------:|-------------|
| git clone to running CRM | < 5 minutes | Timed from git clone to login page load |
| First API call | < 15 minutes (from clone) | curl /api/v1/contacts returns data |
| First custom field | < 30 minutes (from clone) | Admin UI -> create field -> see in UI |
| First plugin | < 2 hours | Install plugin SDK -> register -> see in UI |
| First code contribution | < 1 day (from first clone) | Fix a good-first-issue -> PR merged |

## SETUP EXPERIENCE SPEC

```
$ git clone https://github.com/sovereign-crm/sovereign
$ cd sovereign
$ docker compose up
  [Pulls postgres, redis, api, web]
  [Auto-runs migrations]
  [Creates admin user: admin@sovereign.local / admin1234]
$ open http://localhost:3000
  [Login page loads]
  [Time from clone: ~3 min on broadband]
```

**One command to dev:** docker compose up
**One command to test:** make test
**One command to reset:** make reset

## ARCHITECTURE CLARITY

Every new developer must be able to answer these questions by reading the architecture docs:

| Question | Where Documented | Format |
|----------|-----------------|--------|
| Where do I add a field? | /docs/architecture/data-model.md | Markdown |
| Where do I add a workflow? | /docs/architecture/workflow-engine.md | Markdown |
| Where do I add an API endpoint? | /docs/architecture/api-routing.md | Markdown + code |
| Where do I add a UI component? | /docs/architecture/ui-component-tree.md + Storybook | Interactive |
| How do extensions/plugins hook in? | /docs/architecture/plugin-system.md | Markdown + SDK |

**Key principle:** The answer to each question should be findable within 3 clicks from the repo README.

## SDK STRATEGY

| SDK | Priority | Version | Maintainer |
|-----|:--------:|:-------:|:----------:|
| REST API (curl-friendly docs) | P0 | v1 | Core team |
| TypeScript/JS SDK | P0 | v1 | Core team |
| Python SDK | P1 | v1 | Community |
| Go SDK | P1 | v1 | Core team |
| React hooks (for UI plugins) | P2 | v1 | Core team |

**SDK Requirements:**
- Auto-generated from OpenAPI spec (for REST)
- Published to npm/pypi/go registry
- TypeScript: full type definitions
- Python: type hints + pydantic models
- Go: strong types + interfaces

## PLUGIN SYSTEM ARCHITECTURE

### Plugin Types
| Type | Capabilities | Isolation | 
|------|-------------|:---------:|
| UI Plugin | Add UI component, menu item, dashboard widget | Iframe sandbox |
| API Plugin | Custom endpoints, middleware, webhooks | Sub-process |
| Data Plugin | Custom fields, entities, formulas | Metadata-only |
| Workflow Plugin | Custom workflow actions, triggers | Sub-process |
| Integration Plugin | Connector to external service | Sub-process |

### Plugin Lifecycle
```
Register -> Configure -> Activate -> Run -> Deactivate -> Uninstall
   |            |            |          |          |            |
   v            v            v          v          v            v
Manifest     Settings    Permissions  Execute   Cleanup      Remove
validated    stored      checked                 resources    metadata
```

### Plugin Manifest Example
```yaml
id: acme-analytics
name: ACME Advanced Analytics
version: 1.0.0
author: ACME Corp
license: MIT
hooks:
  - dashboard.widget
  - report.action
permissions:
  - deals:read
  - contacts:read
requires:
  sovereign: ">=2.0.0"
```

## EVALUATION FRAMEWORK

| Criterion | Target | Measured By |
|-----------|:------:|-------------|
| New contributor productive in 1 day | 80% of "good first issues" resolved < 4h | Issue resolution time |
| Build plugin without touching core | Plugin SDK covers all hook points | Plugin test suite |
| API client generated from spec | SDK auto-generation passes | CI pipeline |
| Setup without reading docs | 90% of devs complete setup without docs | User testing |
