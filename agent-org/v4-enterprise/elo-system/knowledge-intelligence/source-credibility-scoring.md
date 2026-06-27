# ELO KNOWLEDGE: SOURCE CREDIBILITY SCORING SYSTEM
# Enterprise Learning Operations — Multi-Factor Source Evaluation V1.0

## Purpose
Every source that enters ELO is scored on credibility before its content is used.
Sources below threshold are rejected. Scores inform quality rubric and content lifecycle.

---

## CREDIBILITY FRAMEWORK: CRAAP+ (Extended)

### 7 Factors

| Factor | Weight | Description | Scoring Range |
|---|---|---|---|
| Currency | 15% | How recent is the information? Is it still current? | 1-10 |
| Relevance | 15% | Does the information directly relate to the domain? | 1-10 |
| Authority | 25% | Who is the author/publisher? Are they credible? | 1-10 |
| Accuracy | 30% | Is the information supported by evidence? Verifiable? | 1-10 |
| Purpose | 5% | Why does the information exist? Inform? Persuade? Sell? | 1-10 |
| Transparency | 5% | Is the source open about methods, funding, conflicts? | 1-10 |
| Provenance | 5% | Can the original source/claim be traced? | 1-10 |

### Formula
```
Credibility_Score = (C x 1.5) + (R x 1.5) + (A x 2.5) + (Ac x 3.0) + (P x 0.5) + (T x 0.5) + (Pr x 0.5)
Max possible = 100
```

### Source Authority Scoring (25% weight)
| Source Type | Base Score | Notes |
|---|---|---|
| Peer-reviewed academic paper | 10 | Top-tier |
| Official documentation (vendor/government) | 9 | Current version only |
| Recognized expert blog | 8 | Check author credentials |
| Industry report (Gartner, Forrester, etc.) | 8 | Check recency |
| Tech news (The Register, Ars Technica, etc.) | 7 | Verify against primary |
| General news (Reuters, AP, Bloomberg) | 7 | Verify against primary |
| Community wiki/forum | 5 | Use for context only |
| Personal blog (anonymous) | 3 | Cross-verify all claims |
| Social media (X/Twitter, LinkedIn post) | 2 | Reference check required |
| AI-generated content (no human review) | 1 | Never use as primary source |

### Currency Scoring (15% weight)
| Age | Score | Action |
|---|---|---|
| < 7 days | 10 | Best for breaking news/tools |
| 7-30 days | 9 | Standard timeliness |
| 30-90 days | 7 | Acceptable for most domains |
| 90-180 days | 5 | Flag for review |
| 180-365 days | 3 | Use only if domain changes slowly |
| > 365 days | 1 | Retire unless historical reference |

---

## BIAS DETECTION SYSTEM

### Bias Assessment Dimensions
1. **Political/Partisan Bias:** Does the source favor a political frame?
2. **Commercial Bias:** Does the source favor a vendor/product/framework?
3. **Selection Bias:** Does the source present only confirming evidence?
4. **Framing Bias:** Does the headline/presentation skew information?
5. **Cultural/Geographic Bias:** Does the source assume one cultural context?

### Bias Detection Pipeline
```
Source URL -> Domain Authority Check -> Known Bias Database Lookup ->
NLP Bias Classifier (multi-label) -> Cross-Source Diversity Check ->
Bias Score (1-10, < 4 = Acceptable, < 2 = Excellent)
```

### Bias Score Formula
```
Bias_Score = 10 - (Political_Bias + Commercial_Bias + Selection_Bias + Framing_Bias + Cultural_Bias)
Where each sub-dimension is 0-2 (0=none, 1=moderate, 2=heavy)
Score 8-10: Low bias, 5-7: Moderate bias (flag), <5: High bias (reject)
```

### Cross-Source Diversity Check
- For each claim: verify against 2+ independent sources
- For each domain cycle: ensure > 6 unique sources
- For each source type: limit dominant type to < 40% of any cycle
- Source diversity score: Shannon entropy of source types per cycle (target > 1.5)

---

## HALLUCINATION PREVENTION SYSTEM

### 4-Layer Defense

**Layer 1: Retrieval Quality Gate**
- Source document relevance score >= 7/10 before content generation
- Multiple sources retrieved for each claim
- Source document must be < 90 days old (or flagged)

**Layer 2: Grounding Check**
- Every factual claim references a specific source
- Source references are verifiable (URL, DOI, document ID)
- Claims are categorized: Direct Quote, Paraphrase, Inference, Opinion

**Layer 3: Faithfulness Scoring**
- NLP entailment check: Does the generated content follow from the source?
- Contradiction flag: Generated content contradicts source?
- Score: Supported = 3, Neutral = 1, Contradicted = -1 (per claim)
- Fact Consistency Score (FCS) = % claims supported

**Layer 4: Cross-Validation**
- Every cycle: Random 10% of packs get secondary LLM verification
- If secondary LLM flags > 2 issues: Full audit of that T3 feeder
- For high-impact claims: Triple verification required

### Hallucination Detection Thresholds
| FCS Score | Classification | Action |
|---|---|---|
| > 95% | Excellent | No action |
| 85-95% | Good | Flag low-scoring claims for review |
| 70-84% | Marginal | T2 review required before delivery |
| < 70% | Failed | Content rejected. T3 alerted. |

---

## INFORMATION AGING / DECAY DETECTION

### Adaptive Decay Framework
**Core Formula:**
```
Freshness_Score = e^(-lambda * delta_t)
Where:
  lambda = f(v, sigma) - adaptive decay constant
  v = velocity (how frequently concept is referenced)
  sigma = volatility (magnitude of change between observations)
  delta_t = days since last verification
```

### Domain-Specific Half-Lives:
| Domain Category | Half-Life (T1/2) | Example |
|---|---|---|
| Technology/Software | 30 days | New frameworks, tools, security patches |
| Methodology | 90 days | Best practices, design patterns |
| Business/Strategy | 120 days | Market analysis, competitive intel |
| Compliance/Regulation | 180 days | Legal requirements, standards |
| Fundamentals | 365+ days | Programming concepts, design principles |

### Content Action by Freshness:
| Freshness Score | Classification | Action |
|---|---|---|
| > 0.9 | Current | No action needed |
| 0.7 - 0.9 | Acceptable | Schedule re-verification |
| 0.5 - 0.7 | Stale | Flag for renewal or archival |
| < 0.5 | Expired | Auto-retire. Notify domain lead. |

### Implementation Summary
**Data Flow:**
```
Source Entered -> Credibility Score (CRAAP+) >= 60? [No -> Reject]
  -> Yes -> Bias Assessment (Score > 5?) [No -> Flag for review]
    -> Yes -> Hallucination Prevention (FCS > 85%?)
      -> No -> T2 Review
      -> Yes -> Content Created -> Freshness Date Stamped
        -> Aging Clock Starts -> Pack enters Lifecycle
```
