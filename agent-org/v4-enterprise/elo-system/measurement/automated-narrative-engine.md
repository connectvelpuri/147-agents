# ELO Automated Narrative Engine V2.0
**Status:** COMPLETE (9.5+)
**Pattern:** "What happened → Why it matters → What to do"
**Standard:** Enterprise executive briefing quality

## Narrative Templates

### Template 1: Weekly L&D Executive Briefing
```
This week, {domain_count} domains delivered {cycle_count} learning cycles
to {agent_count} agents with {completion_pct}% completion rate.

{highlights_section}

Quality: Overall score {q_score}/100 ({q_delta} vs last week).
{quality_detail}

Gaming: {gaming_count} flags detected ({gaming_trend}).
{gaming_detail}

Prediction: Next month LHI forecast at {lhi_forecast} ({forecast_direction}).

{recommendation_section}
```

### Template 2: Domain Health Alert
```
{domain} quality score dropped {delta} pts to {current}/100.
Driven by: {primary_factor} (weight: {weight}%),
           {secondary_factor} (weight: {weight}%).
Action: T2 {domain_lead} notified. Suggested focus: {suggested_focus}.
```

### Template 3: Anomaly Highlight
```
Anomaly detected in {domain}: {agent_count} agents show {pattern}
pattern. Likely cause: {probable_cause}. Confidence: {confidence}%.
Recommended: {action}.
```

### Template 4: Benchmark Gap Analysis
```
{domain} ranks {ranking}/{peer_count} among peer domains.
Primary gap: {gap_metric} ({actual} vs target {target}).
Catch-up ETA at current velocity: {eta_weeks} weeks.
```

## Narrative Generation Rules
1. **Fact-first, narrative-second:** Every claim is backed by a metric reference
2. **No speculation beyond confidence bands:** Predictions are qualified with "forecast" or "projected"
3. **Uncertainty > 30%:** Narrative says "trend unclear" or "insufficient data"
4. **Signal → Insight → Action:** Every observation maps to a recommended action
5. **Tone:** Professional, concise, direct. No adjectives without data support
6. **Length:** 75-150 words for executive summary, <300 words for full briefing

## Output Formats
| Format | Use Case | Length |
|--------|----------|--------|
| Executive Summary | Dashboard panel, 3 sentences | 75-100 words |
| Full Briefing | Weekly report, all domains | 200-300 words |
| Alert Notification | Domain health change | 50-100 words |
| Voice Briefing | Audio summary for T1 | 50-75 words |

## Quality Gates
| Gate | Check | Pass criteria |
|------|-------|---------------|
| Fact-check | All metrics cross-referenced | Zero unverified claims |
| Actionability | Every observation has recommendation | Zero "something should be done" |
| Consistency | Narrative matches KPI tiles | No contradictory statements |
| Readability | Flesch-Kincaid grade | Grade 8-12 (professional but accessible) |
