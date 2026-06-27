#!/usr/bin/env python3
"""
ELO Source Credibility Scorer
Scores every source entering ELO using CRAAP+ framework.

Run on: new source ingestion
"""
import json
import os
from datetime import datetime, date

ELO_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORE_CACHE = os.path.join(ELO_HOME, "knowledge-intelligence", "source-registry.json")
AUDIT_DIR = os.path.join(ELO_HOME, "logs", "audit")

def craap_plus_score(source):
    """
    Multi-factor credibility scoring.
    source dict must have: type, age_days, relevance_domain, authority, accuracy, purpose, transparency, provenance
    """
    scores = {}
    
    # Currency (1-10)
    age = source.get("age_days", 365)
    if age < 7:
        scores["currency"] = 10
    elif age < 30:
        scores["currency"] = 9
    elif age < 90:
        scores["currency"] = 7
    elif age < 180:
        scores["currency"] = 5
    elif age < 365:
        scores["currency"] = 3
    else:
        scores["currency"] = 1
    
    # Relevance (1-10)
    rel_map = {"exact": 10, "high": 8, "medium": 6, "low": 3, "none": 1}
    scores["relevance"] = rel_map.get(source.get("relevance_domain", "low"), 3)
    
    # Authority (1-10) based on source type
    authority_map = {
        "peer_reviewed": 10, "official_docs": 9, "expert_blog": 8,
        "industry_report": 8, "tech_news": 7, "general_news": 7,
        "wiki": 5, "personal_blog": 3, "social_media": 2, "ai_generated": 1
    }
    scores["authority"] = authority_map.get(source.get("type", "unknown"), 3)
    
    # Accuracy (1-10)
    scores["accuracy"] = source.get("accuracy", 5)
    
    # Purpose (1-10)
    purpose_map = {"inform": 10, "educate": 9, "analyze": 8, "persuade": 4, "sell": 2, "mislead": 0}
    scores["purpose"] = purpose_map.get(source.get("purpose", "inform"), 5)
    
    # Transparency (1-10)
    scores["transparency"] = source.get("transparency", 5)
    
    # Provenance (1-10)
    scores["provenance"] = source.get("provenance", 5)
    
    # Weighted total
    total = (
        scores["currency"] * 1.5 +
        scores["relevance"] * 1.5 +
        scores["authority"] * 2.5 +
        scores["accuracy"] * 3.0 +
        scores["purpose"] * 0.5 +
        scores["transparency"] * 0.5 +
        scores["provenance"] * 0.5
    )
    
    return round(total, 1), scores

def bias_assessment(source):
    """Detect bias across 5 dimensions."""
    bias = {}
    bias["political"] = source.get("bias_political", 0)
    bias["commercial"] = source.get("bias_commercial", 0)
    bias["selection"] = source.get("bias_selection", 0)
    bias["framing"] = source.get("bias_framing", 0)
    bias["cultural"] = source.get("bias_cultural", 0)
    
    total_bias = sum(bias.values())
    bias_score = 10 - total_bias
    
    if bias_score >= 8:
        classification = "Low Bias"
    elif bias_score >= 5:
        classification = "Moderate Bias"
    else:
        classification = "High Bias"
    
    return {"score": bias_score, "classification": classification, "dimensions": bias}

def freshness_score(last_verified, half_life_days=90):
    """Calculate content freshness using exponential decay."""
    if isinstance(last_verified, str):
        last_verified = datetime.strptime(last_verified, "%Y-%m-%d").date()
    delta_days = (date.today() - last_verified).days
    freshness = 1.0 * (2 ** (-delta_days / half_life_days))
    return round(freshness, 3)

def register_source(source):
    """Register a source with credibility scoring."""
    score, dimensions = craap_plus_score(source)
    bias = bias_assessment(source)
    
    source_record = {
        "url": source.get("url"),
        "title": source.get("title"),
        "type": source.get("type"),
        "domain": source.get("domain"),
        "credibility_score": score,
        "credibility_dimensions": dimensions,
        "bias_assessment": bias,
        "registered": datetime.now().isoformat(),
        "last_verified": datetime.now().strftime("%Y-%m-%d"),
        "approved": score >= 60 and bias["score"] >= 5,
    }
    
    # Persist to registry
    os.makedirs(os.path.dirname(SCORE_CACHE), exist_ok=True)
    registry = []
    if os.path.exists(SCORE_CACHE):
        with open(SCORE_CACHE, "r") as f:
            registry = json.load(f)
    registry.append(source_record)
    with open(SCORE_CACHE, "w") as f:
        json.dump(registry, f, indent=2)
    
    return source_record

if __name__ == "__main__":
    # Example
    test_source = {
        "url": "https://example.com/new-framework-2026",
        "title": "New Framework for Scalable Systems",
        "type": "industry_report",
        "domain": "architecture",
        "age_days": 15,
        "relevance_domain": "high",
        "accuracy": 8,
        "purpose": "inform",
        "transparency": 7,
        "provenance": 9,
    }
    result = register_source(test_source)
    print(f"Source: {result['title']}")
    print(f"Credibility: {result['credibility_score']}/100")
    print(f"Bias: {result['bias_assessment']['classification']} ({result['bias_assessment']['score']}/10)")
    print(f"Approved: {result['approved']}")
