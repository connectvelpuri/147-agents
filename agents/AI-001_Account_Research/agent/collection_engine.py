"""Collection engine — multi-source data collection across 12 intelligence domains."""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from .models import (
    ResearchDomain, VerifiedClaim, Confidence, CollectionJob,
    FirmographicData, FinancialData, TechnologyStack,
)
from .source_registry import SourceRegistry


class CollectionEngine:
    def __init__(self, source_registry: SourceRegistry):
        self.sources = source_registry
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "RevenueOS-AI-001/1.0 Account Research Agent",
        })

    def collect(self, domain: ResearchDomain, account_name: str, account_domain: str = "") -> CollectionJob:
        job = CollectionJob(domain=domain, account_name=account_name)
        job.started_at = datetime.now()

        dispatcher = {
            ResearchDomain.FIRMOGRAPHIC: self._collect_firmographic,
            ResearchDomain.FINANCIAL: self._collect_financial,
            ResearchDomain.TECHNOGRAPHIC: self._collect_technographic,
            ResearchDomain.NEWS: self._collect_news,
            ResearchDomain.ORGANIZATIONAL: self._collect_organizational,
            ResearchDomain.JOBS: self._collect_jobs,
            ResearchDomain.CULTURAL: self._collect_cultural,
        }

        collector = dispatcher.get(domain)
        if collector:
            try:
                job.results = collector(account_name, account_domain)
                job.status = "completed"
            except Exception as e:
                job.errors.append(str(e))
                job.status = "failed"
        else:
            job.status = "skipped"
            job.errors.append(f"No collector implemented for {domain.value}")

        job.completed_at = datetime.now()
        return job

    def _collect_firmographic(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []

        try:
            resp = self._session.get(f"https://api.crunchbase.com/api/v4/entities/organizations/{name.lower()}", timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                props = data.get("properties", {})
                if props.get("revenue"):
                    claims.append(VerifiedClaim(
                        domain="firmographic", key="revenue",
                        value=props["revenue"],
                        sources=["crunchbase"], source_count=1,
                        confidence=Confidence.MEDIUM,
                    ))
                if props.get("num_employees"):
                    claims.append(VerifiedClaim(
                        domain="firmographic", key="employees",
                        value=props["num_employees"],
                        sources=["crunchbase"], source_count=1,
                        confidence=Confidence.MEDIUM,
                    ))
                self.sources.log_claim("crunchbase")
        except Exception as e:
            self.sources.log_error("crunchbase", str(e))

        if domain:
            try:
                resp = self._session.get(f"https://{domain}", timeout=15)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    text = soup.get_text()[:5000]
                    for line in text.split("\n"):
                        line = line.strip()
                        rev_match = re.search(r"(\$\d[\d,.]*\s*(million|billion|M|B))", line, re.IGNORECASE)
                        if rev_match and not any(c.key == "revenue" for c in claims):
                            claims.append(VerifiedClaim(
                                domain="firmographic", key="revenue",
                                value=rev_match.group(1),
                                sources=["company_website"], source_count=1,
                                confidence=Confidence.LOW,
                            ))
                            self.sources.log_claim("company_website")
                            break
            except Exception:
                pass

        return claims

    def _collect_financial(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []

        if name.endswith(("Inc", "Corp", "Ltd", "PLC")):
            tickers = {"microsoft": "MSFT", "salesforce": "CRM", "oracle": "ORCL", "sap": "SAP"}
            ticker = None
            for key, val in tickers.items():
                if key in name.lower():
                    ticker = val
                    break
            if ticker:
                try:
                    resp = self._session.get(
                        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{ticker}.json",
                        timeout=15,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        claims.append(VerifiedClaim(
                            domain="financial", key="sec_data_available",
                            value=True, sources=["sec_edgar"],
                            source_count=1, confidence=Confidence.HIGH,
                        ))
                        self.sources.log_claim("sec_edgar")
                except Exception as e:
                    self.sources.log_error("sec_edgar", str(e))

        return claims

    def _collect_technographic(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []

        if not domain:
            domain = f"{name.lower().replace(' ', '')}.com"

        try:
            resp = self._session.get(
                f"https://api.builtwith.com/v21/api.json?LOOKUP={domain}",
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                tech_groups = []
                for group in data.get("Groups", []):
                    for tech in group.get("Technologies", []):
                        tech_groups.append(tech.get("Name", ""))
                if tech_groups:
                    claims.append(VerifiedClaim(
                        domain="technographic", key="technologies",
                        value=tech_groups[:20],
                        sources=["builtwith"], source_count=1,
                        confidence=Confidence.MEDIUM,
                    ))
                    self.sources.log_claim("builtwith")
        except Exception as e:
            self.sources.log_error("builtwith", str(e))

        try:
            resp = self._session.get(
                f"https://wappalyzer.com/lookup/{domain}",
                timeout=15,
            )
            if resp.status_code == 200:
                claims.append(VerifiedClaim(
                    domain="technographic", key="wappalyzer_check",
                    value=True, sources=["wappalyzer"],
                    source_count=1, confidence=Confidence.MEDIUM,
                ))
                self.sources.log_claim("wappalyzer")
        except Exception as e:
            self.sources.log_error("wappalyzer", str(e))

        return claims

    def _collect_news(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []

        try:
            resp = self._session.get(
                "https://newsapi.org/v2/everything",
                params={"q": name, "pageSize": 10, "sortBy": "publishedAt", "language": "en"},
                timeout=15,
            )
            if resp.status_code == 200:
                articles = resp.json().get("articles", [])
                if articles:
                    claims.append(VerifiedClaim(
                        domain="news", key="recent_articles",
                        value=[a["title"] for a in articles[:5]],
                        sources=["newsapi"], source_count=len(articles),
                        confidence=Confidence.HIGH,
                    ))
                    self.sources.log_claim("newsapi")
        except Exception as e:
            self.sources.log_error("newsapi", str(e))

        return claims

    def _collect_organizational(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []
        try:
            resp = self._session.get(
                f"https://{domain}/about/leadership" if domain else f"https://{name.lower().replace(' ', '')}.com/about",
                timeout=15,
            )
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                text = soup.get_text()[:10000]
                leadership_pattern = re.findall(
                    r"([A-Z][a-z]+\s[A-Z][a-z]+)\s*[,|-]\s*(CEO|CTO|CFO|COO|CMO|President|VP|SVP|EVP|Chief|Head\sof|Director)",
                    text
                )
                if leadership_pattern:
                    claims.append(VerifiedClaim(
                        domain="organizational", key="executives_found",
                        value=[f"{p[0]} ({p[1]})" for p in leadership_pattern[:10]],
                        sources=["company_website"], source_count=len(leadership_pattern),
                        confidence=Confidence.MEDIUM,
                    ))
                    self.sources.log_claim("company_website")
        except Exception:
            pass

        return claims

    def _collect_jobs(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []
        try:
            careers_url = f"https://{domain}/careers" if domain else ""
            if careers_url:
                resp = self._session.get(careers_url, timeout=15)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    text = soup.get_text()[:5000]
                    tech_roles = ["engineer", "developer", "architect", "data", "cloud", "digital", "transformation", "AI", "ML"]
                    found_roles = [r for r in tech_roles if r.lower() in text.lower()]
                    if found_roles:
                        claims.append(VerifiedClaim(
                            domain="jobs", key="tech_job_postings",
                            value=found_roles, sources=["careers_page"],
                            source_count=len(found_roles),
                            confidence=Confidence.MEDIUM,
                        ))
                        self.sources.log_claim("careers_page")
        except Exception:
            pass

        return claims

    def _collect_cultural(self, name: str, domain: str) -> list[VerifiedClaim]:
        claims = []
        try:
            resp = self._session.get(
                f"https://www.glassdoor.com/Reviews/{name.replace(' ', '-')}-Reviews-E100000.htm",
                timeout=15,
            )
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                rating = soup.select_one(".ratingNumber")
                if rating:
                    claims.append(VerifiedClaim(
                        domain="cultural", key="glassdoor_rating",
                        value=rating.text.strip(),
                        sources=["glassdoor"], source_count=1,
                        confidence=Confidence.MEDIUM,
                    ))
                    self.sources.log_claim("glassdoor")
        except Exception:
            pass

        return claims
