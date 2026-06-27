# Standing Committee 2: Mobile & Field Sales OS Charter

**Governed by:** Constitution Article VII
**Domain:** Mobile architecture, offline, field workflows, mobile-specific features
**Bi-weekly meeting:** Wednesday 14:00 UTC

---

## COMMITTEE MANDATE

Design and build the mobile experience as a "Field Sales Operating System" — not a CRM app. The mobile experience must be usable in poor connectivity, designed for one-handed operation, and feature-complete enough that field reps can go all day without a laptop.

---

## RESEARCH REQUIREMENTS (Pre-Build)

Before any mobile code is written, observe and document:

### Field Sales Verticals
| Vertical | Key Mobile Workflows | Connectivity |
|----------|---------------------|:------------:|
| Pharmaceutical sales | Visit planning, doctor meeting notes, sample tracking | Variable (hospitals = poor) |
| FMCG sales | Route optimization, shelf audit, order capture | Variable (retail = mixed) |
| Insurance sales | Lead management, document capture, policy issuance | Good (urban), Poor (rural) |
| Real estate | Property listing, photo capture, client meeting | Good |
| B2B field sales | Account visit, meeting notes, expense capture | Mixed |

### Key Mobile Workflows (Must Work Offline)
| Task | Frequency | Offline Critical? | Notes |
|------|:---------:|:-----------------:|-------|
| View today's schedule | Multiple times/day | YES | Must load instantly |
| Log a call/meeting | After every interaction | YES | Core activity logging |
| View contact details | Before every interaction | YES | Full contact record offline |
| Take notes (voice/text) | During/after interaction | YES | Voice->text on device |
| Update deal stage | After meetings | YES | Sync when online |
| View pipeline | Daily review | YES | Cached last-version |
| Capture expense photo | Weekly | YES | Queue for upload |
| GPS check-in | Per visit | YES | Queue if no signal |
| Navigate to next appointment | Per visit | NO | Google Maps/Apple Maps |
| Route planning | Morning | YES | Cache daily route |

## OFFLINE ARCHITECTURE DECISIONS

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Sync protocol | CRDT (Automerge) subset | Same as desktop. Field-level sync. |
| Local storage | SQLite (via Drizzle ORM) | Cross-platform, well-tested, CRDT-compatible |
| Conflict resolution | Last-writer-wins (per field) | Simple, predictable. Manual merge UI for conflicts. |
| Attachment handling | Queue + background upload | Photos queue locally, upload when connected. Thumbnail immediately visible. |
| Large dataset handling | Partial sync: last 90 days of activity, all active deals | Historical data fetched on demand. |
| Incremental sync | Timestamp-based delta | Pull changes since last sync. Push local changes. |
| Sync trigger | On app open + periodic (15 min) + manual | Multiple triggers for reliability. |
| Offline duration | Unlimited (with storage warning at 500MB) | User gets "storage warning" not "can't work" |

## MOBILE TECH STACK

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | React Native | Share types with web app. Larger community. |
| State | Zustand + Automerge | Lightweight, CRDT-compatible. |
| Offline DB | SQLite (via expo-sqlite) | Proven, no sync overhead beyond CRDT. |
| Navigation | React Navigation | Standard. Good DX. |
| Maps | Mapbox (self-hosted option) | Privacy-respecting, offline tiles. |
| Voice | Whisper.cpp (on-device) | Private, works offline. |
| Biometrics | Local auth (Face ID / fingerprint) | One-tap unlock. |

## MVP FEATURE SET (Mobile v1)

| Feature | Sprint | Priority |
|---------|:------:|:--------:|
| Login + biometric unlock | S5 | P0 |
| Today's schedule view | S5 | P0 |
| Contact list + search (offline) | S5 | P0 |
| Contact detail (full, offline) | S5 | P0 |
| Activity logging (call, meeting, note) | S5 | P0 |
| Voice note capture (on-device) | S5 | P0 |
| Pipeline kanban (read-only) | S6 | P1 |
| Deal update (stage, amount) | S6 | P1 |
| GPS check-in | S6 | P1 |
| Photo capture (expense/visit) | S6 | P1 |
| Route planner (daily view) | S7 | P2 |
| Push notifications | S7 | P2 |
| Dark mode | S7 | P2 |
| Offline sync status indicator | S7 | P2 |
| Background sync | S8 | P2 |

## FAILURE SCENARIOS & MITIGATIONS

| Scenario | Mitigation |
|----------|------------|
| Phone offline for 14 days | Unlimited offline. Storage warning at 500MB. Sync resume without data loss. |
| Two reps update same record offline | Field-level LWW. Conflict log in sync history. Manual review UI. |
| Sync partially fails | Transactional sync: all-or-nothing per record. Retry queue with exponential backoff. |
| Voice note fails to transcribe | Store audio file. Label "pending transcription." Transcribe when online. |
| Photos consume all storage | Warning at 80%. Auto-compress to 1080p. Recommend Wi-Fi upload. |
