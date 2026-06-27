"""Verification engine — cross-source verification of intelligence claims."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from .models import VerifiedClaim, Confidence, CollectionJob


MIN_SOURCES_FOR_CONFIDENCE = {
    Confidence.HIGH: 3,
    Confidence.MEDIUM: 2,
    Confidence.LOW: 1,
}


class VerificationEngine:
    def verify_job(self, job: CollectionJob) -> CollectionJob:
        for claim in job.results:
            claim = self.verify_claim(claim)
        return job

    def verify_claim(self, claim: VerifiedClaim) -> VerifiedClaim:
        claim.source_count = len(set(claim.sources))
        claim.last_verified = datetime.now()

        if claim.source_count >= 3:
            claim.confidence = Confidence.HIGH
        elif claim.source_count >= 2:
            claim.confidence = Confidence.MEDIUM
        elif claim.source_count >= 1:
            claim.confidence = Confidence.LOW
        else:
            claim.confidence = Confidence.UNVERIFIED

        return claim

    def cross_reference(self, claims_by_domain: dict[str, list[VerifiedClaim]]) -> list[VerifiedClaim]:
        merged = []
        for domain, claims in claims_by_domain.items():
            reconciled = self._reconcile_domain(domain, claims)
            merged.extend(reconciled)
        return merged

    def _reconcile_domain(self, domain: str, claims: list[VerifiedClaim]) -> list[VerifiedClaim]:
        by_key: dict[str, list[VerifiedClaim]] = {}
        for claim in claims:
            by_key.setdefault(claim.key, []).append(claim)

        reconciled = []
        for key, claim_group in by_key.items():
            unique_values = set()
            for c in claim_group:
                val = str(c.value) if not isinstance(c.value, (list, dict)) else str(c.value)
                unique_values.add(val)

            if len(unique_values) > 1:
                merged_sources = []
                for c in claim_group:
                    merged_sources.extend(c.sources)
                merged = VerifiedClaim(
                    domain=domain, key=key,
                    value=list(unique_values),
                    sources=list(set(merged_sources)),
                    source_count=len(set(merged_sources)),
                    confidence=Confidence.LOW,
                    last_verified=datetime.now(),
                )
                if len(unique_values) == 2:
                    merged.confidence = Confidence.MEDIUM
                reconciled.append(merged)
            elif claim_group:
                primary = claim_group[0]
                all_sources = list(set(s for c in claim_group for s in c.sources))
                primary.sources = all_sources
                primary.source_count = len(all_sources)
                primary = self.verify_claim(primary)
                reconciled.append(primary)

        return reconciled

    def detect_contradictions(self, claims: list[VerifiedClaim]) -> list[dict]:
        contradictions = []
        numeric_keys = {}

        for claim in claims:
            if isinstance(claim.value, (int, float)) and claim.key:
                if claim.key in numeric_keys:
                    prev = numeric_keys[claim.key]
                    delta = abs(claim.value - prev["value"])
                    if delta > 0:
                        contradictions.append({
                            "key": claim.key,
                            "value_a": prev["value"],
                            "value_b": claim.value,
                            "sources_a": prev["sources"],
                            "sources_b": claim.sources,
                            "delta": delta,
                        })
                else:
                    numeric_keys[claim.key] = {"value": claim.value, "sources": claim.sources}

        return contradictions
