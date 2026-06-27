"""Main orchestrator — runs the account research agent loop end-to-end.

Follows the ODAI intelligence cycle:
Phase 1: Direction & Scoping
Phase 2: Multi-Source Collection
Phase 3: Cross-Source Verification
Phase 4: Multi-Layer Analysis
Phase 5: Production & Publication
Phase 6: Feedback & Accuracy Scoring
"""

from __future__ import annotations

import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

from .models import (
    AccountRequest, ResearchDepth, ResearchCycleReport,
    CollectionJob, ResearchDomain, AccountIntelligenceReport,
    CorrectionEvent, VerifiedClaim, Confidence,
)
from .collection_engine import CollectionEngine
from .verification_engine import VerificationEngine
from .intelligence_engine import IntelligenceEngine
from .report_publisher import ReportPublisher
from .feedback_processor import FeedbackProcessor
from .source_registry import SourceRegistry
from .database import StateDatabase


class AccountResearchOrchestrator:
    def __init__(self):
        self.db = StateDatabase()
        self.sources = SourceRegistry()
        self.sources.configure_default_sources()
        self.collector = CollectionEngine(self.sources)
        self.verifier = VerificationEngine()
        self.analyst = IntelligenceEngine()
        self.publisher = ReportPublisher()
        self.feedback = FeedbackProcessor(self.sources)

    #  Public API

    def research_account(self, request: AccountRequest) -> AccountIntelligenceReport:
        """Full research cycle for a single account."""
        print(f"\n{'='*60}")
        print(f"[AI-001] RESEARCH CYCLE: {request.account_name} [{request.depth.value}]")
        print(f"{'='*60}")

        self.db.upsert_account(request)
        cycle_id = self.db.start_cycle(request.account_id, request.depth)
        cycle = ResearchCycleReport(account_id=request.account_id, depth=request.depth)

        try:
            # Phase 1: Direction
            plan = self._create_plan(request)
            print(f"[PLAN]   Researching {request.account_name} across {len(plan)} domains")

            # Phase 2: Collection
            all_claims = []
            for domain in plan:
                job = self.collector.collect(domain, request.account_name)
                self.db.save_job(cycle_id, job)
                cycle.jobs.append(job)
                all_claims.extend(job.results)
                print(f"  [{job.status.upper()}] {domain.value}: {len(job.results)} claims ({job.duration_seconds:.1f}s)")

            # Phase 3: Verification
            print(f"[VERIFY] Cross-referencing {len(all_claims)} claims...")
            verified = self.verifier.cross_reference(self._group_by_domain(all_claims))
            contradictions = self.verifier.detect_contradictions(verified)
            if contradictions:
                print(f"  [!] {len(contradictions)} contradictions detected across sources")
                cycle.verification_errors = len(contradictions)

            # Phase 4: Analysis
            print(f"[ANALYZE] Running 3-layer analysis (Descriptive → Diagnostic → Predictive)...")
            report = self.analyst.analyze(request, verified)
            report.overall_confidence = self._calculate_confidence(verified)

            # Phase 5: Production & Publication
            print(f"[PUBLISH] Publishing intelligence reports...")
            self.publisher.publish_intelligence_profile(report)
            self.publisher.publish_financial(report)
            self.publisher.publish_techstack(report)
            self.publisher.publish_competitive(report)
            if report.organizational_chart.c_suite:
                self.publisher.publish_org_chart(report)

            self.db.save_report(request.account_id, report)

            # Compute cycle totals
            cycle.reports_published = [
                f"ai.account.intelligence.profile.{request.account_id}",
                f"ai.account.financial.{request.account_id}",
                f"ai.account.techstack.{request.account_id}",
                f"ai.account.competitive.{request.account_id}",
            ]

        except Exception as e:
            cycle.errors.append(str(e))
            print(f"[ERROR]  Research cycle failed: {e}")

        cycle.completed_at = datetime.now()
        self.publisher.publish_cycle_complete(cycle)
        self.db.complete_cycle(cycle_id, cycle)

        print(f"\n{'='*60}")
        print(f"[DONE]   {request.account_name} researched in {cycle.total_duration_seconds:.1f}s")
        print(f"         Claims: {len(all_claims)} | Confidence: {report.overall_confidence:.0%}")
        print(f"         Reports: {len(cycle.reports_published)} | Errors: {len(cycle.errors)}")
        print(f"{'='*60}\n")

        return report

    def monitor_accounts(self, account_ids: list[str] | None = None):
        """Ongoing monitoring loop for active accounts."""
        if account_ids:
            accounts = [self.db.get_account(aid) for aid in account_ids]
        else:
            rows = self.db._get_conn().execute(
                "SELECT account_id, account_name, depth FROM accounts WHERE status = 'researched'"
            ).fetchall()
            accounts = [dict(r) for r in rows]

        for acc in accounts:
            if not acc:
                continue
            request = AccountRequest(
                account_id=acc["account_id"],
                account_name=acc["account_name"],
                depth=ResearchDepth(acc.get("depth", "standard")),
            )
            print(f"[MONITOR] Checking {request.account_name} for new signals...")
            news_job = self.collector.collect(ResearchDomain.NEWS, request.account_name)
            if news_job.results:
                for claim in news_job.results:
                    self.publisher.publish_signal(
                        AccountIntelligenceReport(account_id=request.account_id, account_name=request.account_name, research_depth=request.depth),
                        {"domain": "news", "claim": claim.value, "confidence": claim.confidence.value},
                    )
                print(f"  [SIGNAL] {len(news_job.results)} new signals for {request.account_name}")

    def process_correction(self, event: CorrectionEvent):
        """Handle a human correction to an intelligence item."""
        result = self.feedback.process_correction(event)
        self.db.log_correction(event)
        print(f"[FEEDBACK] Correction logged for {event.account_id} ({event.domain})")
        for action in result["actions"]:
            print(f"  [ACTION] {action}")

    #  Internal

    def _create_plan(self, request: AccountRequest) -> list[ResearchDomain]:
        base_domains = [
            ResearchDomain.FIRMOGRAPHIC,
            ResearchDomain.FINANCIAL,
            ResearchDomain.TECHNOGRAPHIC,
            ResearchDomain.ORGANIZATIONAL,
            ResearchDomain.NEWS,
            ResearchDomain.JOBS,
        ]

        if request.depth in (ResearchDepth.STANDARD, ResearchDepth.DEEP):
            base_domains.extend([
                ResearchDomain.SOCIAL,
                ResearchDomain.COMPETITIVE,
                ResearchDomain.CULTURAL,
            ])

        if request.depth == ResearchDepth.DEEP:
            base_domains.extend([
                ResearchDomain.REGULATORY,
                ResearchDomain.PARTNER,
                ResearchDomain.INTENT,
            ])

        return base_domains

    def _group_by_domain(self, claims: list[VerifiedClaim]) -> dict[str, list[VerifiedClaim]]:
        groups: dict[str, list[VerifiedClaim]] = {}
        for claim in claims:
            groups.setdefault(claim.domain, []).append(claim)
        return groups

    def _calculate_confidence(self, claims: list[VerifiedClaim]) -> float:
        if not claims:
            return 0.0
        scores = {
            Confidence.HIGH: 1.0,
            Confidence.MEDIUM: 0.7,
            Confidence.LOW: 0.4,
            Confidence.UNVERIFIED: 0.1,
        }
        total = sum(scores.get(c.confidence, 0.0) for c in claims)
        return total / len(claims)

    def close(self):
        self.publisher.close()
        self.db.close()
