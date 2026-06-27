# RevenueOS Agent Specifications

> **System:** AI-Powered Revenue Operating System
> **Total Agents:** 108
> **Divisions:** 27
> **Version:** 1.0
> **Last Updated:** 2026-06-24

---

## Overview

This document defines every specialized AI agent in the RevenueOS. Each agent is a purpose-built LLM instance with a specific prompt pattern, trigger conditions, data sources, training corpus, and criticality level. Agents operate autonomously within their domain and communicate via typed events on the RevenueOS message bus.

### Agent Naming Convention

- RCC- = Revenue Command Center
- MO- = Meeting Observer
- SDR- = SDR Team
- QL- = Qualification Team
- BP- = Buyer Psychology Team
- VE- = Value Engineering Team
- DC- = Discovery Team
- CT- = Content Team
- DS- = Deal Strategy Team
- NG- = Negotiation Team
- RI- = Relationship Intelligence
- RO- = Revenue Operations
- CS- = Customer Success
- ABM- = ABM Team
- PL- = Procurement/Legal Team
- EA- = Executive Advisory Team
- PA- = Partner/Alliance Team
- SC- = Security/Compliance Team
- DLC- = Delivery Confidence Team
- RFP- = RFP/RFQ Team
- KL- = Knowledge & Learning Team
- AG- = AI Governance Team
- AI- = Account Intelligence Team
- SPR- = Sales Psychology Research
- CV- = Customer Voice
- DSV- = Data Services
- SP- = Security & Privacy

### LLM Tier Definitions

| Tier | Class | Use Case | Example Model |
|------|-------|----------|--------------|
| **Complex Reasoning** | Opus-class | Multi-step reasoning, debate, legal analysis, strategy | Claude Opus 4.5, GPT-4.5 |
| **Moderate** | Sonnet-class | Classification, extraction, summarization, generation | Claude Sonnet 4.5, GPT-4o |
| **Simple** | Haiku-class | Single-step classification, formatting, simple routing | Claude Haiku 3.5, GPT-4o-mini |

### Prompt Patterns

| Pattern | Description | Typical LLM Tier |
|---------|-------------|-----------------|
| **Classification** | Assign input to predefined category | Simple |
| **Extraction** | Pull structured fields from unstructured text | Simple/Moderate |
| **Summarization** | Condense longer content preserving key information | Moderate |
| **Generation** | Produce new text (email, proposal, contract clause) | Moderate |
| **Analysis** | Evaluate against criteria, produce judgment | Moderate/Complex |
| **Debate** | Two agents argue opposing positions then synthesize | Complex |
| **Chain-of-thought** | Step-by-step reasoning with visible intermediate steps | Complex |
| **RAG** | Retrieve relevant chunks then answer/generate | Moderate |
| **Routing** | Classify then dispatch to downstream handler | Simple |
| **Scoring** | Numeric or ordinal scoring against rubric | Simple/Moderate |

### Agent Field Definitions

Each agent specification includes the following fields. Fields marked **NEW** were added for Phase A readiness.

| Field | Type | Description | Phase |
|-------|------|-------------|-------|
| **Agent ID** | Code | Unique identifier (e.g., MO-003) | Design |
| **Division** | String | Parent division from the 27-division org | Design |
| **Primary Function** | Text | One-line description of the agent's purpose | Design |
| **Triggers** | List | Events or conditions that activate the agent | Design |
| **Outputs** | List | Events the agent emits | Design |
| **Data Sources** | List | Internal data stores the agent reads | Design |
| **Training Corpus** | Text | Books, frameworks, web sources used for training | Design |
| **LLM Tier** | Tier | Complex/Moderate/Simple reasoning tier | Design |
| **Criticality** | P-level | P0 (system-fatal) to P3 (nice-to-have) | Design |
| **Why Dedicated** | Text | Rationale for having this as a separate agent | Design |
| **Prompt Pattern** | List | LLM prompt patterns used by this agent | Design |
| **Business Outcome** | Text | **NEW** Measurable business impact this agent drives; the "so what" behind its existence | Phase A |
| **Functions (Detailed)** | List | **NEW** Discrete callable operations with input/output signatures | Phase A |
| **Tools/APIs** | List | **NEW** Specific tools, APIs, MCP servers this agent invokes | Phase A |
| **KPIs & Metrics** | Table | **NEW** Quantitative performance indicators tracked per invocation | Phase A |
| **Performance Score** | Text | **NEW** Composite quality rubric (Red/Amber/Green thresholds) | Phase A |
| **Feedback Loop** | Text | **NEW** How the agent learns from human corrections and outcome data | Phase A |

---

## Tier 1 — Core Revenue Engine

---

### Division 1: REVENUE COMMAND CENTER

The central nervous system of RevenueOS. Orchestrates agent workflows, manages human-in-the-loop gates, monitors system health, and coordinates A/B experiments.

---

## Agent RCC-001: Revenue Orchestrator

**Division:** Revenue Command Center
**Primary Function:** Routes every revenue event to the correct agent chain, manages execution dependencies, and ensures end-to-end deal workflows complete.
**Triggers:**
- 
ew_lead_created - routes to SDR + Qualification pipeline
- deal_stage_changed - routes to appropriate next-stage agents
- meeting_completed - triggers Meeting Observer then Discovery/Qualification
- contract_sent - triggers Procurement/Legal + Negotiation
- lost_deal - triggers Win/Loss analysis + Knowledge capture
- won_deal - triggers Customer Success handoff + testimonial request
**Outputs:**
- gent_chain_started - event with chain ID, agent list, expected duration
- gent_chain_completed - event with summary of all agent outputs
- gent_chain_failed - event with failure reason and escalation path
- human_gate_required - event requesting human approval before proceeding
**Data Sources:** Message bus (all agent events), deal CRM schema, workflow DAG definitions, agent capability registry
**Training Corpus:** RevenueOS workflow DAG definitions, Salesforce workflow documentation, Zapier/Workato orchestration patterns, Temporal.io workflow engine docs
**LLM Tier:** Complex Reasoning (Opus class)
**Criticality:** P0 - without this agent, no work flows between agents
**Why dedicated:** Central orchestration requires global system state awareness that no single domain agent possesses. Must resolve conflicts between competing agent recommendations.
**Prompt Pattern:** Routing + Chain-of-thought for dependency resolution

**Business Outcome:** 95% workflow completion rate across all agent chains; human gate latency <30 min for P0 workflows; end-to-end deal processing time reduced by 40%.

**Functions (Detailed):**
- route_event(event: RevenueEvent) -> AgentChain
- resolve_dependencies(chain: AgentChain) -> ExecutionPlan
- handle_chain_failure(chain_id: String, error: String) -> EscalationAction
- gate_human_approval(action: Action, risk: Float) -> ApprovalRequest

**Tools/APIs:**
- NATS JetStream (pub/sub for all agent events)
- LLM inference API (Complex Reasoning tier)
- Workflow DAG store
- Agent capability registry
- Dashboard API

**KPIs & Metrics:**
- workflow_completion_rate: target >0.95
- chain_resolution_latency_p95: target <500ms
- human_gate_response_time_p0: target <30min
- agent_chain_failure_rate: target <0.05

**Performance Score:**
- **Red (<70):** completion rate <0.80 or gate response >60min — escalation to RCC-005
- **Amber (70-85):** completion rate 0.80-0.90 or gate response 30-60min
- **Green (>85):** completion rate >0.95 with gate response <15min — fully autonomous orchestration

**Feedback Loop:**
Human routing corrections logged per event → KL-005 weekly batch retrain adjusts DAG priority weights. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for routing accuracy drift. Source: Continuous updates from web ingestion pipeline (YouTube, blogs, LinkedIn, Gong Labs).

---

## Agent RCC-002: Human-in-the-Loop Gatekeeper

**Division:** Revenue Command Center
**Primary Function:** Evaluates whether an agent action requires human approval based on risk level, deal size, and organizational policy, then manages the approval workflow.
**Triggers:**
- gent_action_proposed with risk_score > threshold
- discount_exceeds_authority from Deal Strategy agent
- contract_term_change from Negotiation agent
- irst_outreach_to_executive from SDR agent
- pricing_deviation > 15% from Value Engineering agent
- security_exception_requested from Security/Compliance agent
**Outputs:**
- pproval_requested - notification to designated approver with context summary
- pproval_granted - event releasing the blocked agent chain
- pproval_denied - event with reason, routes to alternative path
- pproval_escalated - if no response within SLA, escalates up chain
**Data Sources:** Approval policy matrix, org chart (approver hierarchy), deal record (value, region, product), user availability calendar, approval SLA definitions
**Training Corpus:** Enterprise approval workflow patterns (DocuSign, Coupa), delegation theory, risk-based access control literature
**LLM Tier:** Moderate (Sonnet class)
**Criticality:** P0 - compliance and governance depend on this gate
**Why dedicated:** Approval routing is cross-divisional and policy-driven. Separating it from the Orchestrator prevents policy logic from coupling to workflow logic.
**Prompt Pattern:** Classification (risk level) + Routing (approver selection)

**Business Outcome:** 100% of high-risk actions gated; average human approval response <15 min during business hours; zero compliance bypass incidents.

**Functions (Detailed):**
- classify_risk(proposed_action: Action, deal_context: Deal) -> RiskLevel
- route_approver(risk_level: RiskLevel, deal: Deal) -> Approver
- manage_approval_workflow(request: ApprovalRequest) -> ApprovalResult
- escalate_timeout(request: ApprovalRequest) -> EscalationPath

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Approval policy matrix KV
- Org chart DB (approver hierarchy)
- Calendar API

**KPIs & Metrics:**
- approval_sla_compliance: target >0.95
- false_positive_gate_rate: target <0.10
- escalation_rate: target <0.05
- avg_approval_time: target <15min

**Performance Score:**
- **Red (<70):** SLA compliance <0.80 or false positives >0.20 — escalation to RCC-005
- **Amber (70-85):** compliance 0.80-0.90 or false positives 0.10-0.20
- **Green (>85):** compliance >0.95 with avg approval time <10min

**Feedback Loop:**
Misclassified risk levels corrected → KL-005 weekly batch retrain updates risk policy weights. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for policy drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent RCC-003: Performance Dashboard Agent

**Division:** Revenue Command Center
**Primary Function:** Continuously computes and surfaces real-time revenue KPIs, agent effectiveness metrics, pipeline health indicators, and team performance trends.
**Triggers:**
- 	ick_15_minutes - routine metric refresh
- deal_stage_changed - updates pipeline velocity metrics
- meeting_completed - updates conversion metrics
- daily_rollover - generates daily executive summary
- nomaly_detected in any KPI - generates alert
**Outputs:**
- dashboard_updated - new metric values pushed to UI
- kpi_alert - threshold breach notification with context
- weekly_report_generated - formatted report for leadership
- 	rend_detected - significant change in metric direction
- orecast_vs_actual_delta - prediction accuracy report
**Data Sources:** CRM (pipeline, closed won/lost), activity log (emails, calls, meetings), meeting observer metrics, forecast snapshots, historical KPI database
**Training Corpus:** Revenue operations KPI definitions (SaaStr, Pavilion), dashboard design principles (Tableau, Looker), sales metric standard definitions
**LLM Tier:** Simple (Haiku class) - primarily data aggregation and formatting
**Criticality:** P1 - team can operate without dashboard but decision quality degrades
**Why dedicated:** Continuous metric computation is computationally expensive and should not compete with decision-making agents for LLM context.
**Prompt Pattern:** Classification (metric type) + Generation (natural-language insight from numbers)

**Business Outcome:** Leadership decisions informed by <5min stale data; anomaly detection within 15min of KPI deviation; 99.9% dashboard uptime.

**Functions (Detailed):**
- refresh_metrics(interval: Schedule) -> MetricSnapshot
- detect_anomaly(kpi_stream: Stream[Metric]) -> AnomalyAlert
- generate_report(period: TimeRange, audience: Role) -> FormattedReport
- compute_trend(metric: Metric, window: TimeRange) -> TrendDirection

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Simple tier)
- CRM DB (pipeline, closed won/lost)
- Activity log store
- Historical KPI database
- Dashboard API

**KPIs & Metrics:**
- data_freshness_latency: target <5min
- anomaly_detection_recall: target >0.90
- report_generation_time: target <30s
- dashboard_uptime: target >0.999

**Performance Score:**
- **Red (<70):** freshness >15min or recall <0.70
- **Amber (70-85):** freshness 5-15min or recall 0.70-0.90
- **Green (>85):** freshness <5min with recall >0.90

**Feedback Loop:**
Metric misaggregation corrections → KL-005 weekly batch retrain. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for metric drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent RCC-004: A/B Testing Coordinator

**Division:** Revenue Command Center
**Primary Function:** Designs, deploys, and analyzes A/B experiments across email sequences, call scripts, pricing pages, proposals, and outreach timing.
**Triggers:**
- experiment_design_requested by human operator or agent
- 
ew_template_created by Content team - suggests experiment
- sample_size_achieved - automatically concludes experiment and analyzes
- 	est_duration_exceeded - auto-ends inconclusive tests
**Outputs:**
- experiment_proposal - design with hypothesis, variants, sample size, duration
- experiment_started - event activating variant routing
- experiment_result - statistical significance report with recommendation
- meta_analysis - cross-experiment pattern discovery
**Data Sources:** A/B test configuration store, variant assignment table, outcome events (open, click, reply, meeting-booked, deal-won), statistical model parameters
**Training Corpus:** Statistical hypothesis testing (Neyman-Pearson), multi-armed bandit algorithms (Thompson sampling), conversion rate optimization literature (CRO), Peep Laja experimentation frameworks
**LLM Tier:** Complex Reasoning (Opus class) - statistical interpretation and experimental design
**Criticality:** P2 - nice to have for systematic optimization
**Why dedicated:** Experimental design requires statistical reasoning that is absent from other agents.
**Prompt Pattern:** Analysis (statistical significance) + Generation (experiment design)

**Business Outcome:** 2x improvement in conversion rates through systematic experimentation; statistical significance achieved within 95% confidence for all concluded tests.

**Functions (Detailed):**
- design_experiment(hypothesis: Hypothesis, variants: List[Variant]) -> ExperimentPlan
- compute_significance(results: ExperimentData) -> SignificanceResult
- conclude_experiment(experiment: Experiment) -> Recommendation
- run_meta_analysis(experiments: List[Experiment]) -> CrossPattern

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- Experiment config store
- Variant assignment table
- Outcome event store (open, click, reply, meeting-booked, deal-won)

**KPIs & Metrics:**
- experiment_conclusion_rate: target >0.90
- statistical_significance_accuracy: target >0.95
- false_positive_rate: target <0.05
- time_to_conclusion: target <expected_duration

**Performance Score:**
- **Red (<70):** conclusion rate <0.70 or false positives >0.10
- **Amber (70-85):** conclusion rate 0.70-0.85 or false positives 0.05-0.10
- **Green (>85):** conclusion rate >0.90 with false positives <0.03

**Feedback Loop:**
Incorrect significance classifications → KL-005 weekly batch retrain. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for statistical methodology drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent RCC-005: Escalation Manager

**Division:** Revenue Command Center
**Primary Function:** Detects stalled workflows, agent failures, or critical path blockers and routes them to the appropriate human or automated resolver.
**Triggers:**
- gent_timeout - agent exceeded its execution SLA
- gent_chain_stalled - no progress in a workflow for defined period
- deal_stagnation - deal inactive for >N days at a stage
- customer_complaint_received - high-severity feedback
- epeated_agent_failure - same agent fails twice on same input
- cross_agent_conflict - two agents produce contradictory recommendations
**Outputs:**
- escalation_ticket_created - structured issue with severity, context, recommendation
- uto_resolution_attempted - automated retry with modified parameters
- human_assigned - escalation routed to specific person with briefing
- post_mortem_generated - RCA document after resolution
- system_health_alert - broadcast if systemic issue detected
**Data Sources:** Agent execution logs, SLA definitions, on-call schedules, deal timeline, error classification taxonomy, resolution history database
**Training Corpus:** ITIL incident management framework, PagerDuty escalation patterns, site reliability engineering principles (Google SRE), root cause analysis methodologies
**LLM Tier:** Complex Reasoning (Opus class) - root cause diagnosis across multiple possible sources
**Criticality:** P0 - without escalation, system failures go unnoticed
**Why dedicated:** Escalation requires cross-system awareness and RCA capability distinct from the Orchestrator's forward-routing responsibility.
**Prompt Pattern:** Analysis (root cause) + Generation (remediation plan) + Classification (severity)

**Business Outcome:** P0 escalations resolved within 1 hour; systemic issue detection before revenue impact; escalation recurrence rate reduced by 60%.

**Functions (Detailed):**
- detect_stalled_workflow(chain: AgentChain, sla: SLA) -> StalledAlert
- diagnose_root_cause(incident: Incident) -> RootCause
- route_escalation(incident: Incident, severity: Severity) -> Assignment
- generate_post_mortem(incident: Incident, resolution: Resolution) -> RCADocument

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- Agent execution log store
- SLA definitions KV
- On-call schedule DB
- Error classification taxonomy KV

**KPIs & Metrics:**
- p0_escalation_response_time: target <60min
- systemic_issue_detection_recall: target >0.90
- escalation_recurrence_rate: target <0.20
- rca_completion_time: target <24h

**Performance Score:**
- **Red (<70):** P0 response >120min or recurrence >0.35 — manual escalation override
- **Amber (70-85):** P0 response 60-120min or recurrence 0.20-0.35
- **Green (>85):** P0 response <60min with recurrence <0.15

**Feedback Loop:**
Incorrect severity classifications or routing → KL-005 weekly batch retrain. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for SLA drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent RCC-006: Capacity and Cost Governor

**Division:** Revenue Command Center
**Primary Function:** Monitors LLM token consumption, API costs, and agent execution frequency per deal, and enforces budget policies across the agent fleet.
**Triggers:**
- 	oken_quota_exceeded for any LLM tier
- cost_per_deal_above_threshold - alerts on anomalous spend
- monthly_budget_approaching_limit - warning at 80%, 95%, 100%
- inefficient_agent_detected - agent using expensive model for simple task
**Outputs:**
- udget_alert - notification with spend breakdown
- model_downgrade_recommendation - suggest cheaper LLM for specific agent
- gent_throttle_command - reduce execution frequency for low-value agents
- cost_optimization_report - weekly/monthly spend analysis with recommendations
**Data Sources:** LLM API usage logs, per-agent cost tracking, budget policy configuration, deal stage (early-stage deals get cheaper agents), token counters
**Training Corpus:** Cloud cost optimization (AWS Cost Explorer patterns), LLM pricing models (OpenAI, Anthropic), FinOps practice frameworks
**LLM Tier:** Simple (Haiku class) - primarily numeric computation and rule enforcement
**Criticality:** P1 - cost runaway is possible but not immediately revenue-critical
**Why dedicated:** Cost governance is a cross-cutting concern requiring separate attention from revenue-focused agents.
**Prompt Pattern:** Classification (cost tier) + Routing (throttle/downgrade decisions)

**Business Outcome:** Monthly LLM API costs within budget ±5%; cost per deal reduced by 30% through intelligent model tiering; zero budget overrun incidents.

**Functions (Detailed):**
- monitor_token_usage(agent_id: String, tier: Tier) -> UsageReport
- detect_cost_anomaly(spend: SpendData, threshold: Threshold) -> AnomalyAlert
- recommend_model_downgrade(agent: AgentProfile, task: TaskType) -> TierRecommendation
- throttle_agent(agent_id: String, reason: String) -> ThrottleCommand

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Simple tier)
- LLM API usage log store
- Per-agent cost tracking KV
- Budget policy configuration KV
- Token counter stream

**KPIs & Metrics:**
- budget_variance: target <0.05
- cost_per_deal_reduction: target >0.30
- false_throttle_rate: target <0.05
- anomaly_detection_latency: target <5min

**Performance Score:**
- **Red (<70):** budget variance >0.15 or false throttle >0.15 — cost overrun alert to RCC-005
- **Amber (70-85):** variance 0.05-0.15 or false throttle 0.05-0.15
- **Green (>85):** variance <0.05 with zero budget overruns

**Feedback Loop:**
Incorrect tier recommendations or throttle decisions → KL-005 weekly batch retrain. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for cost model drift. Source: Continuous updates from web ingestion pipeline.

---

### Division 2: MEETING OBSERVER

Real-time meeting intelligence. Every sales call, discovery session, demo, and negotiation is transcribed, analyzed, and mined for signals.

---

## Agent MO-001: Real-Time Transcription and Speaker Diarization

**Division:** Meeting Observer
**Primary Function:** Converts meeting audio to timestamped, speaker-labeled transcript in real time, with formatting optimized for downstream analysis agents.
**Triggers:**
- meeting_scheduled - pre-allocates processing resources
- meeting_started - begins real-time ingestion
- udio_chunk_received - continuous processing during meeting
- meeting_ended - finalizes transcript, triggers analysis pipeline
**Outputs:**
- 	ranscript_chunk - incremental transcript during meeting (every 5 seconds)
- ull_transcript - complete speaker-labeled transcript with timestamps
- 	ranscript_summary - condensed version for quick review
- speaker_segments - speaker identity, duration, and turn count
- meeting_metadata - duration, participant list, talk time breakdown
**Data Sources:** Meeting platform API (Zoom, Meet, Teams), audio stream, speaker enrollment profiles, meeting calendar event (participant list)
**Training Corpus:** DeepSpeech/Whisper ASR models, speaker diarization literature (Butterworth, PyAnnote), meeting transcription best practices (Otter.ai, Gong.io), Gong Labs YouTube transcription best practices, Otter.ai engineering blog, DeepSpeech GitHub discussion threads
**LLM Tier:** Simple (Haiku class) - post-processing cleanup and formatting; ASR handled by dedicated ML model
**Criticality:** P0 - all downstream meeting agents depend on this output
**Why dedicated:** ASR + diarization is a specialized ML pipeline, not a text LLM task.
**Prompt Pattern:** Extraction (cleanup of ASR output, punctuation restoration)

**Business Outcome:** Transcript accuracy >95% WER-adjusted for clean audio; diarization accuracy >90%; downstream analysis pipeline triggered within 5s of meeting end.

**Functions (Detailed):**
- transcribe_chunk(audio: AudioChunk) -> TranscriptChunk
- diarize_speakers(transcript: FullTranscript, enrollments: SpeakerProfiles) -> SpeakerSegments
- finalize_transcript(chunks: List[TranscriptChunk]) -> FullTranscript
- generate_summary(transcript: FullTranscript) -> TranscriptSummary

**Tools/APIs:**
- NATS JetStream (pub/sub)
- Whisper/DeepSpeech ASR API
- Transcript store KV
- Speaker enrollment profile store
- Meeting platform API (Zoom, Meet, Teams)

**KPIs & Metrics:**
- word_error_rate: target <0.05
- diarization_accuracy: target >0.90
- end_to_analysis_latency: target <5s
- speaker_segmentation_accuracy: target >0.85

**Performance Score:**
- **Red (<70):** WER >0.15 or diarization <0.70 — fallback to vendor ASR API
- **Amber (70-85):** WER 0.05-0.15 or diarization 0.70-0.90
- **Green (>85):** WER <0.05 with diarization >0.90 — fully autonomous

**Feedback Loop:**
Transcription correction edits → KL-005 weekly batch retrain fine-tunes ASR language model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for WER drift. Source: Continuous updates from web ingestion pipeline (YouTube, blogs, Gong Labs).

---

## Agent MO-002: Sentiment and Emotion Analyst

**Division:** Meeting Observer
**Primary Function:** Tracks emotional trajectory of all meeting participants over time, detecting frustration, excitement, confusion, skepticism, and engagement shifts.
**Triggers:**
- 	ranscript_chunk_available - real-time sentiment during live meeting
- ull_transcript_available - comprehensive post-meeting analysis
- sentiment_anomaly_detected - sudden emotional shift in a participant
**Outputs:**
- sentiment_timeline - per-participant sentiment over meeting duration
- emotion_highlights - key moments of strong emotional reaction
- engagement_score - aggregate participant engagement metric
- rustration_alert - if frustration exceeds threshold, triggers real-time SDR alert
- confusion_markers - sections where participant appeared confused
**Data Sources:** Speaker-labeled transcript chunks, acoustic features (tone, pace, volume), historical sentiment baselines per contact
**Training Corpus:** Ekman's basic emotions framework, affect recognition literature (MIT Media Lab), sentiment analysis in sales contexts (Gong.io research), emotional intelligence in negotiation, Gong Labs sentiment research blog, MIT Media Lab YouTube channel, Hume AI emotion recognition research
**LLM Tier:** Moderate (Sonnet class) - nuanced sentiment requires contextual understanding
**Criticality:** P1 - valuable but call recordings can be manually reviewed
**Why dedicated:** Sentiment analysis requires temporal tracking (emotional arcs, not point judgments) distinct from discrete classification tasks.
**Prompt Pattern:** Analysis (temporal sentiment trajectory) + Classification (emotion labels)

**Business Outcome:** Sentiment trajectory detection within 30s of emotional shift; frustration detection recall >90%; coaching interventions triggered by sentiment improve win rates by 15%.

**Functions (Detailed):**
- analyze_sentiment_timeline(transcript: TranscriptChunk, participant: ParticipantId) -> SentimentPoint
- detect_emotion_shift(sentiment_stream: Stream[SentimentPoint]) -> EmotionHighlight
- compute_engagement_score(participants: List[ParticipantData]) -> EngagementMetric
- alert_frustration(sentiment: SentimentData, threshold: Threshold) -> FrustrationAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Transcript chunk stream
- Acoustic feature store (tone, pace, volume)
- Historical sentiment baselines KV
- Sentiment model API

**KPIs & Metrics:**
- sentiment_shift_detection_latency: target <30s
- frustration_detection_recall: target >0.90
- emotion_classification_accuracy: target >0.85
- false_positive_alert_rate: target <0.10

**Performance Score:**
- **Red (<70):** recall <0.70 or latency >60s — fallback to post-meeting batch analysis
- **Amber (70-85):** recall 0.70-0.90 or latency 30-60s
- **Green (>85):** recall >0.90 with latency <30s

**Feedback Loop:**
Incorrect emotion classifications → KL-005 weekly batch retrain updates sentiment model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for sentiment labeling drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent MO-003: Objection Detector and Classifier

**Division:** Meeting Observer
**Primary Function:** Identifies, classifies, and timestamps every objection raised during a meeting, then recommends the optimal response strategy.
**Triggers:**
- 	ranscript_chunk_available - real-time objection flagging
- ull_transcript_available - comprehensive objection catalog
- objection_pattern_detected - similar objection across multiple meetings with same account
**Outputs:**
- objection_log - timestamped list of all objections with speaker, category, severity
- objection_category - price, timing, authority, need, competing priority, competitor, security, fit
- objection_severity - blocking, significant, minor
- ecommended_response - suggested rebuttal strategy from training corpus
- unaddressed_objection_alert - objection raised but not responded to
**Data Sources:** Transcript chunks, objection taxonomy, rebuttal playbook library, historical objection-outcome correlation data
**Training Corpus:** SPIN selling objection handling, Challenger Sale teaching framework, Command of the Message objection taxonomy, MEDDIC objection categories, Gong Labs objection taxonomy blog series, Challenger Sale YouTube teaching demos, SalesHacker objection handling articles
**LLM Tier:** Moderate (Sonnet class) - objection classification requires nuanced understanding of buyer language
**Criticality:** P0 - unaddressed objections directly cause lost deals
**Why dedicated:** Objection detection requires a specialized classification taxonomy distinct from general sentiment or content summarization.
**Prompt Pattern:** Classification (objection type/severity) + RAG (response retrieval)

**Business Outcome:** 95% of objections detected in real time; objection response effectiveness improved by 25%; unaddressed objections reduced by 80%.

**Functions (Detailed):**
- detect_objection(transcript: TranscriptChunk) -> ObjectionEvent
- classify_objection(objection: ObjectionEvent) -> ObjectionCategory
- score_severity(objection: ObjectionEvent) -> SeverityScore
- retrieve_response(objection: ObjectionEvent, playbook: RebuttalLibrary) -> RecommendedResponse
- flag_unaddressed(objection: ObjectionEvent, transcript: FullTranscript) -> UnaddressedAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Transcript chunk stream
- Objection taxonomy KV
- Rebuttal playbook store
- Objection-outcome correlation DB

**KPIs & Metrics:**
- objection_detection_recall: target >0.95
- objection_classification_accuracy: target >0.90
- unaddressed_alert_recall: target >0.95
- response_relevance_score: target >0.85

**Performance Score:**
- **Red (<70):** recall <0.75 or accuracy <0.70 — manual review required
- **Amber (70-85):** recall 0.75-0.90 or accuracy 0.70-0.90
- **Green (>85):** recall >0.95 with accuracy >0.90

**Feedback Loop:**
Missed or misclassified objections → KL-005 weekly batch retrain updates objection taxonomy. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for classification drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent MO-004: Commitment Tracker

**Division:** Meeting Observer
**Primary Function:** Extracts, categorizes, and tracks all commitments made during meetings and follows up on completion.
**Triggers:**
- 	ranscript_chunk_available - detects commitments in real time
- ull_transcript_available - comprehensive commitment audit
- commitment_overdue - commitment past its due date triggers reminder
- meeting_ends_without_commitments - alerts SDR to secure next steps
**Outputs:**
- commitment_log - structured list: who, what, deadline, status
- uyer_commitment_summary - what the buyer agreed to do
- seller_commitment_summary - what the seller must do
- commitment_reminder - automated nudge before deadline
- commitment_missed_alert - buyer commitment not fulfilled, suggests action
**Data Sources:** Transcript, CRM task records, calendar (for deadline dates), email follow-up thread, historical commitment compliance per contact
**Training Corpus:** Commitment-based sales methodologies, Sandler selling principles, getting commitments frameworks (Jeffrey Gitomer), influence and commitment theory (Cialdini), Sandler Selling YouTube channel, Jeffrey Gitomer LinkedIn posts, Cialdini Consistency articles
**LLM Tier:** Moderate (Sonnet class) - detecting implicit commitments requires nuanced language understanding
**Criticality:** P0 - deals advance only through commitments; untracked commitments stall
**Why dedicated:** Commitment tracking is a discrete extraction task with temporal follow-up, distinct from objection or sentiment analysis.
**Prompt Pattern:** Extraction (commitment entities: who/what/when) + Classification (commitment type/severity)

**Business Outcome:** 95% of commitments extracted and tracked; commitment fulfillment rate increased by 30%; deals with tracked commitments close 20% faster.

**Functions (Detailed):**
- extract_commitment(transcript: TranscriptChunk) -> Commitment
- classify_commitment_type(commitment: Commitment) -> CommitmentType
- track_deadline(commitment: Commitment, calendar: CalendarData) -> ReminderEvent
- alert_missed(commitment: Commitment, status: FulfillmentStatus) -> MissedAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Transcript chunk stream
- CRM task records API
- Calendar API
- Email follow-up thread store

**KPIs & Metrics:**
- commitment_extraction_recall: target >0.95
- commitment_classification_accuracy: target >0.90
- reminder_timeliness: target >0.95
- missed_commitment_alert_recall: target >0.95

**Performance Score:**
- **Red (<70):** recall <0.75 or accuracy <0.70 — manual commitment audit required
- **Amber (70-85):** recall 0.75-0.90 or accuracy 0.70-0.90
- **Green (>85):** recall >0.95 with accuracy >0.90

**Feedback Loop:**
Missed or misclassified commitments → KL-005 weekly batch retrain updates extraction model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for extraction drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent MO-005: Question Quality Scorer

**Division:** Meeting Observer
**Primary Function:** Analyzes every question asked by the seller during a meeting, scoring them for open/closed ratio, discovery depth, diagnostic value, and control of conversation flow.
**Triggers:**
- ull_transcript_available - post-meeting question audit
- seller_question_asked - real-time question quality feedback
- consecutive_poor_questions - alerts seller to adjust approach
**Outputs:**
- question_quality_score - aggregate metric per meeting
- open_vs_closed_ratio - percentage breakdown with ideal target
- discovery_depth_map - questions mapped to needs hierarchy layers
- improvement_suggestion - specific coaching feedback
- question_trend_over_time - improvement/decline across meetings with same rep
**Data Sources:** Transcript with speaker labels, question classification taxonomy, meeting role, seller historical performance data
**Training Corpus:** SPIN selling questioning framework (Situation, Problem, Implication, Need-Payoff), Challenger Sale teaching questions, diagnostic questioning literature, active listening frameworks, SPIN Selling LinkedIn articles, Challenger Sale YouTube question techniques, Mike Bosworth diagnostic questioning blog
**LLM Tier:** Moderate (Sonnet class) - question classification requires understanding question intent
**Criticality:** P1 - valuable coaching tool but not directly deal-blocking
**Why dedicated:** Question analysis requires a specialized pedagogical lens unrelated to sentiment or objection tracking.
**Prompt Pattern:** Classification (question type) + Scoring (quality rubric) + Generation (coaching feedback)

**Business Outcome:** Seller question quality score improves 40% over 3 months through coaching; discovery depth doubled; qualification accuracy improves 20%.

**Functions (Detailed):**
- classify_question(question: Utterance, speaker: SpeakerId) -> QuestionType
- compute_open_closed_ratio(questions: List[Question]) -> RatioMetric
- map_discovery_depth(questions: List[Question], hierarchy: NeedsHierarchy) -> DepthMap
- generate_coaching(score: QualityScore, trend: TrendData) -> CoachingFeedback

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Transcript with speaker labels store
- Question classification taxonomy KV
- Seller historical performance DB
- Coaching feedback store

**KPIs & Metrics:**
- question_classification_accuracy: target >0.85
- coaching_relevance_score: target >0.80
- seller_score_improvement_90d: target >0.30
- open_question_ratio_target: target >0.60

**Performance Score:**
- **Red (<70):** accuracy <0.65 or improvement <0.10 — human coaching intervention required
- **Amber (70-85):** accuracy 0.65-0.85 or improvement 0.10-0.30
- **Green (>85):** accuracy >0.85 with improvement >0.30

**Feedback Loop:**
Incorrect question classifications → KL-005 weekly batch retrain updates taxonomy. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for scoring drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent MO-006: Talk Ratio and Conversation Dynamics Analyst

**Division:** Meeting Observer
**Primary Function:** Measures who is speaking and for how long, analyzing turn-taking patterns, interruptions, silence length, and conversation control dynamics.
**Triggers:**
- meeting_started - begins talk time tracking
- 	ranscript_chunk_available - incremental talk ratio update
- meeting_ended - final talk ratio report
- 	alk_ratio_threshold_exceeded - seller speaking >70% triggers alert
- wkward_silence_detected - pause >5 seconds flagged
**Outputs:**
- 	alk_ratio_report - percentage per participant with benchmark comparison
- interruption_log - each interruption event with context
- silence_analysis - frequency and duration of pauses
- coaching_recommendation - specific behavioral feedback
- ideal_ratio_deviation - how actual ratio differs from stage-appropriate ideal
**Data Sources:** Speaker-labeled transcript, participant role tags, meeting stage classification, talk ratio benchmarks per meeting type
**Training Corpus:** Conversational dynamics research (Harvard Business Review), active listening literature, sales conversation analysis (Challenger, Gong.io), Gong Labs conversation research YouTube channel, HBR conversational dynamics articles, Sales Insights Lab YouTube
**LLM Tier:** Simple (Haiku class) - primarily quantitative with simple rule-based classification
**Criticality:** P2 - valuable coaching input but not revenue-critical in isolation
**Why dedicated:** Talk ratio is a quantitative signal best handled by a lightweight model rather than competing for context in a complex reasoning agent.
**Prompt Pattern:** Classification (interruption vs natural turn) + Scoring (ratio computation)

**Business Outcome:** Seller talk ratio within ideal range (30-50%) for 80% of meetings; silence management improved 25%; interruption frequency reduced 30%.

**Functions (Detailed):**
- compute_talk_ratio(segments: SpeakerSegments) -> TalkRatioReport
- classify_interruption(event: TurnEvent) -> InterruptionType
- analyze_silence(transcript: FullTranscript, threshold: Duration) -> SilenceAnalysis
- generate_behavioral_coaching(metrics: DynamicsMetrics, benchmark: Benchmark) -> CoachingRecommendation

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Simple tier)
- Speaker-labeled transcript store
- Participant role tags KV
- Meeting stage classifier
- Talk ratio benchmark DB

**KPIs & Metrics:**
- talk_ratio_accuracy: target >0.95
- interruption_classification_accuracy: target >0.85
- silence_detection_recall: target >0.90
- coaching_recommendation_uptake: target >0.60

**Performance Score:**
- **Red (<70):** ratio accuracy <0.80 or silence recall <0.70 — data quality alert
- **Amber (70-85):** accuracy 0.80-0.90 or recall 0.70-0.90
- **Green (>85):** accuracy >0.95 with recall >0.90

**Feedback Loop:**
Misclassified interruptions or incorrect ratio boundaries → KL-005 weekly batch retrain. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for metric drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent MO-007: Real-Time Coach

**Division:** Meeting Observer (Division 2)
**Primary Function:** Provides live, real-time coaching suggestions to sales reps during active meetings based on buyer sentiment, talk ratio, objection patterns, and deal stage context
**Triggers:** `meeting.started`, `meeting.transcript.chunk_available` (every 30s during active meeting)
**Outputs:** `meeting.coaching.suggestion_generated`, `meeting.coaching.alert_triggered`
**Data Sources:** Real-time transcript stream, deal context (stage, value, stakeholders), historical win/loss patterns, buyer persona profile
**Training Corpus:** Gong Labs conversation data, Challenger Sale (teaching moments), Never Split the Difference (tactical empathy, mirroring), SPIN Selling (question quality), Fanatical Prospecting, Gong Labs coaching research, Chris Voss YouTube tactical empathy demos, Josh Braun YouTube objection handling
**LLM Tier:** Sonnet (low-latency required for real-time feedback within meeting flow)
**Criticality:** P2 (nice to have — meetings can proceed without coaching)
**LLM Pattern:** Streaming analysis + generation — reads transcript chunks, classifies moment type (objection, commitment, discovery gap), generates 1-3 sentence coaching suggestion
**Degrade Path:** Falls back to post-meeting summary (no real-time) if latency >5s

**Business Outcome:** Real-time coaching improves meeting win rates by 20%; coach suggestion acceptance rate >75%; reps close 2x more deals with live coaching.

**Functions (Detailed):**
- classify_moment(transcript_chunk: String, deal_context: Deal) -> MomentType
- generate_suggestion(moment_type: MomentType, buyer_sentiment: Sentiment) -> CoachingSuggestion
- alert_trigger(alert_type: AlertType, context: String) -> CoachingAlert
- fallback_to_post_meeting(meeting_id: String) -> PostMeetingSummary

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Sonnet low-latency tier)
- Real-time transcript stream
- Deal context store (stage, value, stakeholders)
- Historical win/loss patterns DB
- Buyer persona profile store

**KPIs & Metrics:**
- suggestion_acceptance_rate: target >0.75
- suggestion_generation_latency: target <3s
- meeting_win_rate_improvement: target >0.20
- false_alert_rate: target <0.10

**Performance Score:**
- **Red (<70):** acceptance <0.55 or latency >5s — triggers degrade path to post-meeting
- **Amber (70-85):** acceptance 0.55-0.75 or latency 3-5s
- **Green (>85):** acceptance >0.75 with latency <3s — real-time coaching active

**Feedback Loop:**
Ignored or incorrect coaching suggestions → KL-005 weekly batch retrain updates suggestion model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for suggestion quality drift. Source: Continuous updates from web ingestion pipeline (YouTube, blogs, Gong Labs).

---

### Division 3: SDR TEAM

Multi-channel prospecting, outreach, and pipeline generation. These agents find, research, and engage prospects across email, LinkedIn, phone, and other channels.

---

## Agent SDR-001: Multi-Channel Prospector

**Division:** SDR Team
**Primary Function:** Continuously scans external data sources for in-market buyers matching the ICP, enriches their profiles, and prioritizes them for outreach.
**Triggers:**
- 	ick_6_hours - routine scan of intent and firmographic sources
- icp_updated - re-scans with new ICP criteria
- lookalike_requested - finds accounts similar to a won deal
- event_signal_received - conference attendee list, webinar registration
**Outputs:**
- prospect_discovered - new person matching ICP with enrichment data
- ccount_discovered - new company matching ICP
- outreach_priority_queue - ranked list of who to contact next
- intent_alert - prospect showing buying intent
- icp_violation_alert - SDR attempting to prospect outside ICP
**Data Sources:** ZoomInfo, LinkedIn Sales Navigator, Apollo.io, Clearbit, 6sense intent data, G2 buyer intent, CrunchBase, BuiltWith
**Training Corpus:** Modern sales prospecting frameworks (Predictable Revenue, Fanatical Prospecting), multi-channel outreach best practices (SalesLoft, Outreach.io), Josh Braun YouTube cadence design, Matt Easton YouTube cold calling, Close.com blog outreach patterns, Mailshake blog multi-channel strategies, Steli Efti LinkedIn cold email threads
**LLM Tier:** Moderate (Sonnet class) - enrichment and prioritization require reasoning about fit
**Criticality:** P0 - without prospect discovery, pipeline never starts
**Why dedicated:** Continuous external data ingestion is a scan-loop pattern, distinct from the event-triggered message-passing of other agents.
**Prompt Pattern:** Extraction (enrichment fields) + Classification (ICP fit scoring) + Routing (priority assignment)

**Business Outcome:** 3x more ICP-matching prospects discovered per week; enrichment accuracy >95%; outreach priority queue improves conversion by 25%.

**Functions (Detailed):**
- scan_intent_sources(sources: List[DataSource], icp: ICPDefinition) -> List[Prospect]
- enrich_profile(prospect: Prospect, enrichment_sources: List[Source]) -> EnrichedProfile
- score_icp_fit(prospect: EnrichedProfile, icp: ICPDefinition) -> FitScore
- prioritize_outreach(prospects: List[ScoredProspect]) -> PriorityQueue

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- ZoomInfo API
- LinkedIn Sales Navigator API
- Apollo.io API
- Clearbit API
- 6sense intent data API

**KPIs & Metrics:**
- prospects_discovered_per_week: target >200
- icp_fit_accuracy: target >0.90
- enrichment_completeness: target >0.95
- queue_conversion_rate_improvement: target >0.25

**Performance Score:**
- **Red (<70):** discovery rate <50/week or fit accuracy <0.70 — escalate to SDR manager
- **Amber (70-85):** discovery rate 50-200/week or accuracy 0.70-0.90
- **Green (>85):** discovery rate >200/week with accuracy >0.90

**Feedback Loop:**
Incorrect ICP fit scores → KL-005 weekly batch retrain updates ICP model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for fit accuracy drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent SDR-002: Intent Signal Monitor

**Division:** SDR Team
**Primary Function:** Continuously tracks and aggregates buying intent signals across the web and scores prospects on buying readiness.
**Triggers:**
- 	ick_24_hours - daily scan across all intent sources
- job_change_detected for a known contact
- unding_announcement for a target account
- 	echnology_added to a target account's stack
- content_consumed - prospect viewed pricing page, case study
- competitor_lost_deal - prospect evaluated competitor and did not buy
**Outputs:**
- intent_signal_event - structured: contact, signal type, source, timestamp, strength
- uying_readiness_score - aggregate readiness metric
- outreach_trigger_recommendation - suggested outreach based on signal
- signal_aggregation_report - weekly summary of all signals per account
- intent_trend_alert - sudden spike in intent signals from an account
**Data Sources:** LinkedIn API, CrunchBase/PitchBook, BuiltWith/Stackshare, G2/Capterra, company blog/news RSS, competitor communities
**Training Corpus:** Intent-based selling frameworks (6sense, Bombora methodology), predictive lead scoring literature, buyer intent signal taxonomy, 6sense blog intent signals, Bombora blog content interest, LinkedIn Sales Blog buying signals, UserGems blog trigger events
**LLM Tier:** Moderate (Sonnet class) - distinguishing genuine buying intent from noise requires nuanced reasoning
**Criticality:** P1 - prospecting can happen without intent data but is less efficient
**Why dedicated:** Intent monitoring is a continuous scan pattern distinct from event-triggered prospecting.
**Prompt Pattern:** Classification (signal type/strength) + Scoring (readiness)

**Business Outcome:** Buying intent detected within 24h of signal appearance; signal-to-noise ratio improved 3x; intent-triggered outreach converts 40% better.

**Functions (Detailed):**
- scan_intent_signals(sources: List[IntentSource]) -> List[IntentSignal]
- score_buying_readiness(signals: List[IntentSignal], prospect: Prospect) -> ReadinessScore
- recommend_outreach_trigger(signal: IntentSignal, prospect: Prospect) -> OutreachRecommendation
- aggregate_signals(account: Account, window: TimeRange) -> SignalAggregationReport
- detect_intent_trend(signal_stream: Stream[IntentSignal]) -> TrendAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- LinkedIn API
- CrunchBase/PitchBook API
- BuiltWith/Stackshare API
- G2/Capterra API
- RSS feed reader

**KPIs & Metrics:**
- signal_detection_latency: target <24h
- signal_classification_accuracy: target >0.85
- false_positive_rate: target <0.15
- intent_triggered_conversion_rate: target >0.40

**Performance Score:**
- **Red (<70):** detection latency >72h or false positives >0.30 — manual intent review
- **Amber (70-85):** latency 24-72h or false positives 0.15-0.30
- **Green (>85):** latency <24h with false positives <0.15

**Feedback Loop:**
Misclassified intent signals → KL-005 weekly batch retrain updates signal taxonomy. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for classification drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent SDR-003: Personalized Outreach Generator

**Division:** SDR Team
**Primary Function:** Crafts individualized, multi-channel outreach sequences using prospect research, intent signals, and proven templates.
**Triggers:**
- outreach_triggered - prospect moved to outreach queue
- ollow_up_due - prospect did not respond within N days
- eply_received - generates contextual follow-up based on reply content
- ounce_detected - email bounced, switches channel
- unsubscribe_event - removes from sequence, logs reason
**Outputs:**
- email_draft - personalized email with subject line, body, CTA
- linkedin_message - personalized InMail or connection request note
- call_script - talking points for phone outreach
- multi_channel_sequence - timed sequence across channels
- ollow_up_variant - A/B variant for testing
**Data Sources:** Prospect profile (ZoomInfo, LinkedIn), intent signals, email template library, personalization rules, A/B test results
**Training Corpus:** AIDA copywriting framework, Predictable Revenue outreach templates, SalesLoft/Outreach cadence design, cold email best practices (Close.com, Mailshake), Lavender blog email personalization data, Close.com blog A/B testing results, Mailshake blog copywriting templates, Steli Efti LinkedIn cold email examples
**LLM Tier:** Moderate (Sonnet class) - personalization requires blending prospect research with messaging strategy
**Criticality:** P0 - without personalized outreach, engagement rates collapse
**Why dedicated:** Outreach generation is a content creation task with specific channel constraints distinct from analysis or classification agents.
**Prompt Pattern:** Generation (multichannel copy) + RAG (personalization from prospect research)

**Business Outcome:** Email reply rates >15%; meeting booked rate >8%; multi-channel sequences outperform single-channel by 2x.

**Functions (Detailed):**
- generate_email(prospect: Prospect, intent: IntentSignal, template: Template) -> EmailDraft
- generate_linkedin_message(prospect: Prospect, context: ResearchBrief) -> LinkedInMessage
- generate_call_script(prospect: Prospect, sequence: Sequence) -> CallScript
- design_sequence(prospect: Prospect, channels: List[Channel]) -> MultiChannelSequence
- create_variant(sequence: Sequence, variant_rules: ABTestRules) -> FollowUpVariant

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- CRM API (REST)
- Email API
- LinkedIn API
- Prospect profile store (ZoomInfo)
- Template library KV

**KPIs & Metrics:**
- email_reply_rate: target >0.15
- meeting_booked_rate: target >0.08
- personalization_relevance_score: target >0.85
- multi_channel_lift: target >2.0x

**Performance Score:**
- **Red (<70):** reply rate <0.08 or booked rate <0.03 — template rotation required
- **Amber (70-85):** reply rate 0.08-0.15 or booked rate 0.03-0.08
- **Green (>85):** reply rate >0.15 with booked rate >0.08

**Feedback Loop:**
Low-performing outreach variants → KL-005 weekly batch retrain updates template weights. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for message effectiveness drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent SDR-004: Follow-Up Sequencing Engine

**Division:** SDR Team
**Primary Function:** Designs and executes timed multi-touch follow-up sequences that adapt based on prospect behavior and engagement signals.
**Triggers:**
- initial_outreach_sent - starts follow-up timer
- email_opened but no reply - adjusts timing/message
- link_clicked - sequences to relevant content
- eply_received - hands off to qualification or adjusts sequence
- meeting_booked - pauses sequence, hands to Meeting Observer
- opt_out - stops all communications
**Outputs:**
- sequence_plan - timeline of touches: channel, content, interval
- 	ouch_executed - notification that a touch was sent
- sequence_adjusted - behavior adapted the sequence
- sequence_paused - awaiting human input or external event
- sequence_completed - final disposition (engaged, nurtured, archived)
**Data Sources:** Email engagement events, LinkedIn interaction data, sequence template library, A/B test results per persona, timezone/calendar data
**Training Corpus:** Sales cadence design (SalesLoft, Outreach), multi-touch sequencing theory (Josh Braun, Steli Efti), email timing optimization research, Outreach blog cadence design, SalesLoft blog sequencing, Josh Braun YouTube multi-touch sequences, Sales Pipeline Radio podcast cadence episodes
**LLM Tier:** Moderate (Sonnet class) - adaptive sequencing requires reasoning about behavior signals
**Criticality:** P0 - sequences drive the entire outbound motion
**Why dedicated:** Sequencing is a stateful, time-dependent operation fundamentally different from one-shot generation tasks.
**Prompt Pattern:** Routing (behavior branch) + Generation (adapted message) + Classification (engagement level)

**Business Outcome:** Sequence completion rate >70%; meetings booked per sequence >15%; opt-out rate <2% per sequence.

**Functions (Detailed):**
- start_sequence(prospect: Prospect, sequence: Sequence) -> SequencePlan
- execute_touch(sequence: Sequence, step: Step) -> TouchExecuted
- adjust_sequence(sequence: Sequence, behavior: BehaviorSignal) -> SequenceAdjusted
- pause_sequence(sequence: Sequence, reason: PauseReason) -> SequencePaused
- complete_sequence(sequence: Sequence) -> SequenceDisposition

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- CRM API (REST)
- Email API
- LinkedIn API
- Sequence template library KV
- A/B test results DB
- Timezone/calendar data store

**KPIs & Metrics:**
- sequence_completion_rate: target >0.70
- meetings_booked_per_sequence: target >0.15
- opt_out_rate: target <0.02
- sequence_to_qualification_rate: target >0.25

**Performance Score:**
- **Red (<70):** completion <0.50 or opt-out >0.05 — sequence design review
- **Amber (70-85):** completion 0.50-0.70 or opt-out 0.02-0.05
- **Green (>85):** completion >0.70 with opt-out <0.02

**Feedback Loop:**
Ineffective sequence branches → KL-005 weekly batch retrain updates decision tree. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for sequencing logic drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent SDR-005: Account Researcher

**Division:** SDR Team
**Primary Function:** Produces deep account research briefs before any outreach, covering company, industry, technology stack, recent news, and personal context.
**Triggers:**
- prospect_assigned_to_sdr - triggers full research
- ccount_first_contact_approaching - preps research for upcoming outreach
- meeting_scheduled_with_account - updates research brief
- 
ews_event_for_account - appends to research brief
**Outputs:**
- ccount_research_brief - company overview, recent news, tech stack, funding, competitors, growth signals
- contact_research_brief - role, tenure, career path, education, social activity, shared connections, interests
- personalization_levers - specific hooks for outreach
- conversation_starters - 3-5 researched opening lines
- mutual_connection_report - shared network paths
**Data Sources:** LinkedIn, CrunchBase, company website, news RSS, SEC filings, job boards, Twitter/X, blog posts, conference history
**Training Corpus:** Sales research methodologies (MemSQL, Salesforce), account-based research practices (Terminus, Demandbase), competitive intelligence gathering, LinkedIn Sales Navigator best practices, CrunchBase blog research methods, SEC filings analysis guides, UserGems blog account intelligence
**LLM Tier:** Moderate (Sonnet class) - synthesizing multiple sources into a coherent brief requires reasoning
**Criticality:** P1 - outreach without research is possible but significantly less effective
**Why dedicated:** Account research is a batch data-collection task with different latency requirements than real-time outreach generation.
**Prompt Pattern:** Extraction (entity and relationship extraction) + Summarization (research brief)

**Business Outcome:** Research briefs produced in <30min per account; personalization hook relevance >90%; conversation starter success rate >40%.

**Functions (Detailed):**
- research_account(account: Account, sources: List[Source]) -> AccountResearchBrief
- research_contact(contact: Contact, sources: List[Source]) -> ContactResearchBrief
- extract_personalization_levers(briefs: ResearchBriefs) -> List[PersonalizationLever]
- generate_conversation_starters(brief: ResearchBrief, persona: Persona) -> List[ConversationStarter]
- find_mutual_connections(contact: Contact, network: SocialGraph) -> MutualConnectionReport

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- LinkedIn API
- CrunchBase API
- Company website scraper
- News RSS reader
- SEC filings parser
- Twitter/X API

**KPIs & Metrics:**
- research_brief_production_time: target <30min
- personalization_hook_relevance: target >0.90
- conversation_starter_success_rate: target >0.40
- research_completeness_score: target >0.85

**Performance Score:**
- **Red (<70):** production time >60min or hook relevance <0.70 — SDR manually researches
- **Amber (70-85):** time 30-60min or relevance 0.70-0.90
- **Green (>85):** time <30min with relevance >0.90

**Feedback Loop:**
Inaccurate research data → KL-005 weekly batch retrain updates source extraction model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for data accuracy drift. Source: Continuous updates from web ingestion pipeline.

---

### Division 4: QUALIFICATION TEAM

These agents assess deal quality, score opportunities against qualification frameworks, and identify disqualifying signals early.

---

## Agent QL-001: BANT/MEDDPICC Scorer

**Division:** Qualification Team
**Primary Function:** Automatically scores every opportunity against BANT and MEDDPICC frameworks from conversation and CRM data.
**Triggers:**
- 
ew_opportunity_created - initial qualification score
- meeting_completed - re-score based on new information
- email_thread_analyzed - extracts qualification signals from email
- demo_completed - updates technical qualification
- deal_stage_changed - re-validates qualification at stage transition
**Outputs:**
- ant_score - structured with confidence per dimension
- meddpicc_score - structured with evidence snippets per dimension
- qualification_gap_report - missing information that needs to be gathered
- deal_quality_index - composite score
- disqualification_recommendation - if score below threshold
- 
ext_qualification_questions - what to ask in next meeting to fill gaps
**Data Sources:** Meeting transcripts, email threads, CRM opportunity fields, calendar, proposal/quote data, competitive landscape notes
**Training Corpus:** BANT framework (IBM), MEDDIC/MEDDPICC (Dick Dunkel, Command of the Message), MEDDPICC (Andy Whyte, Winning by Design), MEDDICC blog Andy Whyte posts, Dick Dunkel LinkedIn MEDDIC insights, Nabeel Abdulla LinkedIn MEDDPICC examples
**LLM Tier:** Complex Reasoning (Opus class) - qualification scoring requires evaluating evidence quality
**Criticality:** P0 - without qualification, teams waste time on unwinable deals
**Why dedicated:** Qualification requires multi-dimensional scoring with evidence verification, a distinct reasoning pattern.
**Prompt Pattern:** Analysis (evidence-based scoring) + Extraction (evidence snippets)

**Business Outcome:** Qualification scoring accuracy >95% vs human audit; deals entering pipeline score-validated; disqualification catch rate >90% within first 30 days.

**Functions (Detailed):**
- score_bant(deal: Deal, transcripts: List[Transcript]) -> BANTScore
- score_meddpicc(deal: Deal, transcripts: List[Transcript]) -> MEDDPICCScore
- identify_gaps(scores: QualificationScores) -> GapReport
- compute_deal_quality(scores: QualificationScores) -> DealQualityIndex
- recommend_disqualification(score: DealQualityIndex, threshold: Threshold) -> DisqualificationRecommendation
- generate_next_questions(gaps: GapReport) -> List[Question]

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- CRM API (REST)
- Scoring rubric KV
- Deal history DB
- Meeting transcript store
- Email thread store

**KPIs & Metrics:**
- scoring_accuracy_vs_human: target >0.95
- disqualification_precision: target >0.85
- gap_coverage_rate: target >0.90
- scoring_latency: target <30s

**Performance Score:**
- **Red (<70):** accuracy <0.80 or precision <0.65 — escalation to QL-007 degraded mode
- **Amber (70-85):** accuracy 0.80-0.95 or precision 0.65-0.85
- **Green (>85):** accuracy >0.95 with precision >0.85

**Feedback Loop:**
Incorrect dimension scores → KL-005 weekly batch retrain updates scoring rubric weights. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for scoring calibration drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent QL-002: Deal Inspector

**Division:** Qualification Team
**Primary Function:** Performs a forensic audit of every deal before it advances, identifying pipeline hygiene issues, missing fields, and data quality problems.
**Triggers:**
- deal_stage_change_attempted - inspects before allowing transition
- 	ick_7_days - periodic inspection of all active deals
- deal_set_to_close_won - pre-close inspection
- pipeline_review_requested - on-demand audit
**Outputs:**
- inspection_report - passed/failed checks with details
- deal_health_score - composite of all inspection dimensions
- missing_fields_alert - required CRM fields that are empty
- stalled_deal_alert - deal inactive longer than stage-appropriate duration
- data_inconsistency_detected - conflicting information across CRM fields
- stage_advancement_blocked - gate preventing advancement
**Data Sources:** CRM deal records, activity history, email threads, meeting transcripts, qualification scores, historical deal data
**Training Corpus:** Salesforce pipeline management best practices, revenue operations hygiene standards (Pavilion), SOX compliance for sales processes, Pavilion blog pipeline hygiene, Salesforce pipeline management articles, Revenue Ops LinkedIn discussions
**LLM Tier:** Simple (Haiku class) - primarily rule-based checks
**Criticality:** P0 - data quality directly impacts forecast accuracy
**Why dedicated:** Deal inspection is a compliance/audit function with a different operational cadence than qualification scoring.
**Prompt Pattern:** Classification (pass/fail per check item) + Generation (inspection summary)

**Business Outcome:** 100% of deals pass pre-stage hygiene gate; missing fields reduced to <5 per deal; data inconsistency detected within 1h of creation.

**Functions (Detailed):**
- inspect_deal(deal: Deal, checks: InspectionChecklist) -> InspectionReport
- score_deal_health(report: InspectionReport) -> DealHealthScore
- detect_missing_fields(deal: Deal, required_fields: List[Field]) -> MissingFieldsAlert
- detect_stalled_deal(deal: Deal, stage: Stage, threshold: Duration) -> StalledDealAlert
- detect_data_inconsistency(deal: Deal, crm_fields: CRMFields) -> InconsistencyAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Simple tier)
- CRM API (REST)
- Pipeline rules KV
- Stage duration policy store
- Deal history DB

**KPIs & Metrics:**
- inspection_completion_rate: target >0.99
- missing_fields_per_deal: target <5
- false_positive_alert_rate: target <0.10
- inspection_latency: target <10s

**Performance Score:**
- **Red (<70):** completion <0.90 or false positives >0.20 — pipeline freeze risk
- **Amber (70-85):** completion 0.90-0.99 or false positives 0.10-0.20
- **Green (>85):** completion >0.99 with false positives <0.10

**Feedback Loop:**
Incorrect inspection results → KL-005 weekly batch retrain updates rule base. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for inspection rule drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent QL-003: Disqualification Engine

**Division:** Qualification Team
**Primary Function:** Proactively identifies deals that should be disqualified based on ICP mismatch, budget inadequacy, timeline misalignment, or champion weakness.
**Triggers:**
- qualification_score_drops_below_threshold
- icp_fit_score_drops - company changed significantly
- competitive_loss_to_known_rival - prospect with strong competitor relationship
- udget_discrepancy_detected - actual budget < required by >50%
- champion_leave_detected - internal champion left the company
- evaluation_timeline_exceeded - past expected decision date with no movement
**Outputs:**
- disqualification_recommendation - structured: reason, evidence, confidence
- disqualification_approved - deal moved to closed-lost
- eshape_recommendation - recast as pilot, not full purchase
- salvage_path - conditions to re-qualify later
- 
egative_signal_log - all disqualifying signals with timestamps
**Data Sources:** Qualification scores, ICP definition, CRM deal data, competitor CRM entries, LinkedIn (champion employment), email/meeting transcripts, CrunchBase
**Training Corpus:** Sales disqualification frameworks (MEDDIC triggers, Brent Keltner), win/loss analysis, ICP definition methodologies, Brent Keltner LinkedIn win/loss insights, MEDDICC disqualification criteria blog, SalesHacker disqualification articles
**LLM Tier:** Complex Reasoning (Opus class) - distinguishing salvageable from hopeless requires sophisticated judgment
**Criticality:** P1 - disqualification prevents resource waste but teams can identify obvious mismatches
**Why dedicated:** Disqualification requires a pessimistic, critical lens separate from optimistic generation agents to prevent bias contamination.
**Prompt Pattern:** Analysis (evidence-weighted disqualification) + Debate (salvage vs disqualify)

**Business Outcome:** Resource wasted on unwinable deals reduced by 40%; disqualification accuracy >90% vs post-mortem; salvage path success rate >15%.

**Functions (Detailed):**
- detect_disqualification_signal(deal: Deal, signals: List[Signal]) -> DisqualificationEvent
- recommend_disqualify(reasons: List[DisqualificationReason], evidence: Evidence) -> DisqualificationRecommendation
- propose_reshape(deal: Deal, conditions: DealConditions) -> ReshapeRecommendation
- define_salvage_path(deal: Deal, conditions: DealConditions) -> SalvagePath
- log_negative_signals(deal: Deal, signals: List[Signal]) -> NegativeSignalLog

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- CRM API (REST)
- ICP definition KV
- Competitor CRM entries
- LinkedIn API
- CrunchBase API
- Email/meeting transcript store

**KPIs & Metrics:**
- disqualification_accuracy: target >0.90
- false_disqualification_rate: target <0.10
- resource_savings: target >0.40
- salvage_path_success_rate: target >0.15

**Performance Score:**
- **Red (<70):** accuracy <0.70 or false disqualifications >0.20 — human review all disqualified
- **Amber (70-85):** accuracy 0.70-0.90 or false rate 0.10-0.20
- **Green (>85):** accuracy >0.90 with false rate <0.10

**Feedback Loop:**
Incorrect disqualification decisions → KL-005 weekly batch retrain updates disqualification model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for disqualification drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent QL-004: Champion Validator

**Division:** Qualification Team
**Primary Function:** Assesses the strength, access, credibility, and motivation of internal champions.
**Triggers:**
- champion_named in CRM or meeting transcript
- meeting_with_champion_completed - re-assesses champion strength
- org_change_detected - champion role/team changed
- deal_needs_champion - advanced without identified champion
**Outputs:**
- champion_power_index - score based on seniority, influence, relationship to DM
- champion_motivation_profile - why champion advocates
- champion_weakness_alert - lacks access to DM or budget authority
- champion_cultivation_plan - actions to strengthen relationship
- champion_verification_question - validate champion claims
**Data Sources:** Meeting transcripts, email threads, org chart, communication frequency, CRM opportunity history, relationship health scores
**Training Corpus:** MEDDIC champion qualification (Dick Dunkel), The Challenger Sale champion development, Champion's Code, influence without authority literature, MEDDICC blog champion qualification, Challenger Sale LinkedIn champion articles, Dick Dunkel champion validation videos
**LLM Tier:** Complex Reasoning (Opus class) - assessing political capital requires sophisticated social reasoning
**Criticality:** P0 - weak champions are the #1 cause of forecasted deals slipping
**Why dedicated:** Champion validation requires social network analysis and influence assessment distinct from other qualification dimensions.
**Prompt Pattern:** Analysis (champion strength assessment) + Generation (cultivation plan)

**Business Outcome:** Champion weakness detected in 90% of slip-risk deals; champion strength score correlates with win rate at r>0.5; champion cultivation improves win rate by 25%.

**Functions (Detailed):**
- compute_champion_power(champion: Contact, org_chart: OrgChart) -> ChampionPowerIndex
- profile_champion_motivation(champion: Contact, transcripts: List[Transcript]) -> MotivationProfile
- detect_champion_weakness(champion: Contact, power_index: ChampionPowerIndex) -> WeaknessAlert
- generate_cultivation_plan(champion: Contact, weakness: WeaknessAlert) -> CultivationPlan
- verify_champion(champion: Contact, questions: List[Question]) -> VerificationResult

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- CRM API (REST)
- Meeting transcript store
- Org chart DB
- Relationship health score store
- Email thread store

**KPIs & Metrics:**
- champion_weakness_detection_recall: target >0.90
- champion_power_score_win_correlation: target >0.50
- champion_identification_accuracy: target >0.85
- cultivation_plan_uptake: target >0.60

**Performance Score:**
- **Red (<70):** recall <0.70 or correlation <0.30 — manual champion audit
- **Amber (70-85):** recall 0.70-0.90 or correlation 0.30-0.50
- **Green (>85):** recall >0.90 with correlation >0.50

**Feedback Loop:**
Incorrect champion assessments → KL-005 weekly batch retrain updates champion model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for champion scoring drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent QL-005: Budget Verification Agent

**Division:** Qualification Team
**Primary Function:** Validates that the prospect has committed budget, verifies the amount, identifies budget sources, and flags budget risks.
**Triggers:**
- udget_amount_entered in CRM
- udget_discussed in meeting transcript
- iscal_year_change - re-verifies budget availability
- discount_requested - cross-references budget vs proposed price
**Outputs:**
- udget_verified - confirmation with evidence
- udget_unverified - missing evidence, flags for discovery
- udget_type_classification - new, reallocation, remaining, no budget
- udget_adequacy_score - budget vs estimated total cost
- udget_approval_chain - who needs to approve
- udget_timing_risk - budget lapse concerns
**Data Sources:** Meeting transcripts, email threads, CRM budget fields, procurement documentation, fiscal calendar, proposed quote/price
**Training Corpus:** MEDDIC budget verification, procurement budget cycles, enterprise budget planning, value-based pricing
**LLM Tier:** Moderate (Sonnet class) - budget verification involves evidence quality assessment
**Criticality:** P0 - unverified budget is the leading cause of late-stage deal death
**Why dedicated:** Budget verification requires evidence-verification across multiple data sources distinct from general qualification.
**Prompt Pattern:** Extraction (budget figures) + Classification (verification confidence)

**Business Outcome:** 95% of budgets verified before stage 3; budget-related deal death reduced by 60%; budget adequacy flagged for 100% of underfunded deals.

**Functions (Detailed):**
- verify_budget(deal: Deal, evidence: List[Evidence]) -> BudgetVerificationResult
- classify_budget_type(deal: Deal, transcripts: List[Transcript]) -> BudgetType
- score_budget_adequacy(budget: Budget, total_cost: Cost) -> BudgetAdequacyScore
- map_approval_chain(deal: Deal, org_chart: OrgChart) -> ApprovalChain
- assess_timing_risk(budget: Budget, fiscal_calendar: FiscalCalendar) -> TimingRisk

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- CRM API (REST)
- Meeting transcript store
- Email thread store
- Procurement documentation store
- Fiscal calendar API

**KPIs & Metrics:**
- budget_verification_rate: target >0.95
- budget_death_reduction: target >0.60
- verification_accuracy: target >0.90
- budget_type_classification_accuracy: target >0.85

**Performance Score:**
- **Red (<70):** verification rate <0.75 or accuracy <0.70 — manual budget validation
- **Amber (70-85):** rate 0.75-0.90 or accuracy 0.70-0.90
- **Green (>85):** rate >0.95 with accuracy >0.90

**Feedback Loop:**
Incorrect budget verifications → KL-005 weekly batch retrain updates verification model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for budget accuracy drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent QL-006: Timeline Assessment Agent

**Division:** Qualification Team
**Primary Function:** Evaluates the prospect's stated timeline against organizational buying process reality and historical deal velocity.
**Triggers:**
- 	imeline_stated in CRM or meeting
- meeting_completed - extracts timeline references
- stage_duration_exceeded - deal slower than expected
- quarter_end_approaching - re-validates close date
- deal_slipped - analyzes reason for slip
**Outputs:**
- 	imeline_credibility_score - how realistic the stated timeline is
- 	imeline_to_close_prediction - predicted close date range
- critical_path_alert - identified bottleneck
- cceleration_recommendations - shorten the timeline
- quarter_commit_confidence - probability of closing in current quarter
**Data Sources:** CRM close dates, meeting transcripts, historical deal velocity by segment, buying process templates, fiscal calendar
**Training Corpus:** Sales cycle analysis (Salesforce benchmark), buying process frameworks (Gartner, Forrester), deal velocity analysis (Clari, Gong)
**LLM Tier:** Moderate (Sonnet class) - timeline assessment requires pattern matching against historical data
**Criticality:** P1 - valuable for forecasting but historical data can substitute
**Why dedicated:** Timeline assessment combines predictive modeling with process knowledge, a specialized reasoning task.
**Prompt Pattern:** Analysis (timeline vs historical pattern) + Scoring (credibility)

**Business Outcome:** Timeline credibility score predicts slip with >85% accuracy; quarter commit confidence within 10% of actual; acceleration recommendations shorten cycles by 15%.

**Functions (Detailed):**
- score_timeline_credibility(deal: Deal, stated_close: Date) -> TimelineCredibilityScore
- predict_close_date(deal: Deal, historical_velocity: VelocityData) -> PredictedCloseRange
- detect_critical_path(deal: Deal, process_map: ProcessMap) -> CriticalPathAlert
- recommend_acceleration(deal: Deal, bottlenecks: List[Bottleneck]) -> AccelerationRecommendations
- compute_quarter_confidence(deal: Deal, prediction: PredictedCloseRange) -> QuarterCommitConfidence

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- CRM API (REST)
- Meeting transcript store
- Historical deal velocity DB
- Buying process templates KV
- Fiscal calendar API

**KPIs & Metrics:**
- timeline_prediction_accuracy: target >0.85
- quarter_commit_error: target <0.10
- slip_detection_recall: target >0.90
- cycle_time_reduction: target >0.15

**Performance Score:**
- **Red (<70):** prediction accuracy <0.65 or slip recall <0.70 — human forecast override
- **Amber (70-85):** accuracy 0.65-0.85 or recall 0.70-0.90
- **Green (>85):** accuracy >0.85 with recall >0.90

**Feedback Loop:**
Incorrect timeline assessments → KL-005 weekly batch retrain updates velocity model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for prediction accuracy drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent QL-007: Degraded-Mode Scorer

**Division:** Qualification Team
**Primary Function:** Scores deal confidence when primary qualification data is incomplete, outdated, or contradictory, enabling reliable decision-making under uncertainty.
**Triggers:**
- qualification_data_gap_detected
- stale_qualification_score - last updated beyond threshold
- conflicting_signals_across_sources
- deal_progressing_with_incomplete_meddpicc
- manual_fallback_requested_by_rep
**Outputs:**
- degraded_confidence_score - with uncertainty range
- data_gap_inventory - specific missing qualification fields
- confidence_erosion_factors - what degrades reliability
- recommended_data_collection_priority - what to fix first
- decision_boundary_advice - which decisions are safe with current data
- escalation_to_human - when confidence falls below threshold
**Data Sources:** Available CRM fields, meeting transcript snippets, email signals, historical deal patterns for similar segments, partial qualification data
**Training Corpus:** Decision-making under uncertainty (Kahneman, Gigerenzer), confidence calibration, partial information decision frameworks, Bayesian reasoning for sales
**LLM Tier:** Complex Reasoning (Opus class) - uncertainty quantification requires calibrated judgment under ambiguity
**Criticality:** P1 - valuable when data is sparse, but deals can proceed without it
**Why dedicated:** Degraded-mode scoring requires uncertainty quantification absent from standard qualification agents that assume clean data.
**Prompt Pattern:** Scoring (confidence) + Analysis (gaps) + Classification (decision safety)

**Business Outcome:** Reliable decisions possible with 40% less data; confidence calibration within 10% of actual accuracy; escalation rate reduced by 50%.

**Functions (Detailed):**
- compute_degraded_score(deal: Deal, available_data: PartialData) -> DegradedConfidenceScore
- inventory_data_gaps(deal: Deal, required_fields: List[Field]) -> DataGapInventory
- identify_erosion_factors(deal: Deal, gaps: DataGapInventory) -> ErosionFactorList
- prioritize_data_collection(gaps: DataGapInventory, impact: ImpactScore) -> CollectionPriority
- advise_decision_boundary(confidence: DegradedConfidenceScore) -> DecisionBoundaryAdvice
- escalate_low_confidence(confidence: DegradedConfidenceScore, threshold: Threshold) -> Escalation

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- CRM API (REST)
- Meeting transcript store
- Email signal store
- Historical deal patterns DB
- Partial qualification data store

**KPIs & Metrics:**
- confidence_calibration_error: target <0.10
- decision_accuracy_at_degraded: target >0.80
- escalation_rate_reduction: target >0.50
- gap_inventory_completeness: target >0.90

**Performance Score:**
- **Red (<70):** calibration error >0.20 or decision accuracy <0.60 — force human-in-loop
- **Amber (70-85):** error 0.10-0.20 or accuracy 0.60-0.80
- **Green (>85):** error <0.10 with accuracy >0.80

**Feedback Loop:**
Incorrect confidence scores → KL-005 weekly batch retrain updates uncertainty model. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for calibration drift. Source: Continuous updates from web ingestion pipeline.

---

### Division 5: BUYER PSYCHOLOGY TEAM

These agents apply cognitive and behavioral science to understand buyer decision-making, adapt communication, and influence purchase behavior ethically.

---

## Agent BP-001: Cognitive Bias Detector

**Division:** Buyer Psychology Team
**Primary Function:** Identifies which cognitive biases are active in buyer decision-making and recommends ethically applied influence strategies.
**Triggers:**
- meeting_transcript_available - scan for bias indicators
- objection_raised - classify objection through bias lens
- pricing_discussion - detect anchoring effects
- competitor_mentioned - detect social proof effects
**Outputs:**
- ctive_biases_report - list of detected biases with evidence quotes
- ias_lever_recommendations - ethical application of identified biases
- nchoring_alert - prospect anchored on competitor price
- status_quo_burden - how much inertia must be overcome
- loss_aversion_framing - frame gains as avoiding losses
- ias_ethics_check - ensure recommendations do not exploit vulnerable biases
**Data Sources:** Meeting transcripts, email threads, negotiation history, pricing discussions, competitor references
**Training Corpus:** Kahneman and Tversky - Judgment under Uncertainty, Cialdini - Influence, Thaler and Sunstein - Nudge, Kahneman - Thinking Fast and Slow, Gigerenzer - Gut Feelings, Cialdini LinkedIn behavioral insights, Predictably Irrational blog (Dan Ariely), Nudge blog (Thaler), Behavioral Economics YouTube channel
**LLM Tier:** Complex Reasoning (Opus class) - bias detection requires nuanced psychological insight and ethical judgment
**Criticality:** P1 - powerful but experienced reps can handle without it
**Why dedicated:** Cognitive bias detection requires specialized psychological knowledge absent from general-purpose sales agents.
**Prompt Pattern:** Analysis (bias identification) + Generation (ethical influence recommendations)

**Business Outcome:** Bias-influenced deal losses reduced by 30%; anchoring effects identified in 90% of pricing discussions; ethical influence recommendation adoption >70%.

**Functions (Detailed):**
- detect_biases(transcript: TranscriptChunk, context: MeetingContext) -> ActiveBiasesReport
- classify_objection_through_bias(objection: ObjectionEvent) -> BiasLensClassification
- detect_anchoring(pricing_discussion: TranscriptSegment) -> AnchoringAlert
- assess_status_quo_burden(meeting: MeetingData) -> StatusQuoBurdenScore
- generate_influence_recommendation(bias: BiasType, context: DealContext) -> InfluenceRecommendation
- audit_ethics(recommendations: List[Recommendation]) -> EthicsCheckResult

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- Meeting transcript store
- Email thread store
- Bias taxonomy KV
- Personality profile store

**KPIs & Metrics:**
- bias_detection_recall: target >0.85
- anchoring_identification_recall: target >0.90
- ethics_compliance_rate: target >0.99
- recommendation_adoption_rate: target >0.70

**Performance Score:**
- **Red (<70):** recall <0.65 or ethics <0.95 — ethics compliance review triggered
- **Amber (70-85):** recall 0.65-0.85 or ethics 0.95-0.99
- **Green (>85):** recall >0.85 with ethics >0.99

**Feedback Loop:**
Misidentified biases → KL-005 weekly batch retrain updates bias taxonomy. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for bias detection drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent BP-002: Buyer Personality Profiler

**Division:** Buyer Psychology Team
**Primary Function:** Constructs a psychological profile of each buyer and adapts all communication accordingly.
**Triggers:**
- irst_meeting_transcript_available - initial profile construction
- 
ew_email_reply_received - refines profile based on writing style
- meeting_completed - updates profile with new observations
- profile_inconsistency_detected - behavior contradicts current profile
**Outputs:**
- personality_profile - DISC or Big Five approximation with confidence
- communication_style_guide - formality, detail density, directness, pace
- isk_tolerance_assessment - risk profile in purchase decisions
- alue_language_mapping - which values resonate
- daptation_violation_alert - message misaligned with profile
**Data Sources:** Meeting transcripts, email style, social media presence, role/industry base rates, interaction history
**Training Corpus:** DISC assessment framework (Marston), Myers-Briggs Type Indicator, Big Five personality model, Social Styles (Tracom), Miller and Steinberg - communication adaptation theory, DISC profiles LinkedIn articles, Social Styles blog Tracom, HBR personality assessment articles
**LLM Tier:** Complex Reasoning (Opus class) - personality profiling requires interpreting subtle behavioral cues
**Criticality:** P1 - improves conversion but not deal-blocking
**Why dedicated:** Personality profiling requires longitudinal behavioral pattern recognition across multiple interaction channels.
**Prompt Pattern:** Analysis (behavioral pattern extraction) + Classification (personality type) + Generation (adaptation guide)

**Business Outcome:** Personality profile accuracy >85% after 3 interactions; communication adaptation improves response rates by 30%; profile consistency maintained across >90% of interactions.

**Functions (Detailed):**
- construct_initial_profile(transcript: MeetingTranscript) -> PersonalityProfile
- refine_profile(profile: PersonalityProfile, new_data: InteractionData) -> UpdatedProfile
- assess_risk_tolerance(profile: PersonalityProfile, deal_context: DealContext) -> RiskToleranceAssessment
- map_value_language(profile: PersonalityProfile, interactions: List[Interaction]) -> ValueLanguageMapping
- detect_profile_inconsistency(behavior: BehaviorData, profile: PersonalityProfile) -> AdaptationViolationAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- Meeting transcript store
- Email style analyzer
- Social media API
- Personality profile KV
- Interaction history DB

**KPIs & Metrics:**
- profile_accuracy_3_interactions: target >0.85
- response_rate_improvement: target >0.30
- profile_consistency_score: target >0.90
- profile_build_latency: target <5min

**Performance Score:**
- **Red (<70):** accuracy <0.65 or consistency <0.70 — fallback to base persona defaults
- **Amber (70-85):** accuracy 0.65-0.85 or consistency 0.70-0.90
- **Green (>85):** accuracy >0.85 with consistency >0.90

**Feedback Loop:**
Incorrect profile classifications → KL-005 weekly batch retrain updates personality model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for profiling accuracy drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent BP-003: Communication Style Adapter

**Division:** Buyer Psychology Team
**Primary Function:** Takes any outbound communication draft and adapts its language, tone, structure, and length to match the recipient's communication style.
**Triggers:**
- email_draft_ready from SDR or Content agent
- proposal_draft_ready - adapts executive summary
- call_script_ready - adapts language for buyer's style
- uyer_profile_updated - re-adapts pending communications
**Outputs:**
- dapted_email - style-aligned version of draft
- dapted_proposal - executive summary in buyer's preferred framing
- dapted_script - call script tuned to buyer style
- multi_stakeholder_adaptation - same content in N versions for N stakeholders
**Data Sources:** Buyer personality profile, original draft content, style adaptation rules per type, past adaptation performance data
**Training Corpus:** Social Styles communication adaptation, DISC communication strategies, Neuro-Linguistic Programming, HBR on communication flexibility, Crucial Conversations (Patterson et al.)
**LLM Tier:** Moderate (Sonnet class) - style adaptation is a rewrite task with clear parameters
**Criticality:** P1 - significantly improves engagement but unadapted messages can still work
**Why dedicated:** Style adaptation is a batch rewrite post-processing step that should not couple to generation logic.
**Prompt Pattern:** Generation (style-adapted rewrite) + Classification (apply correct adaptation rules)

**Business Outcome:** Adapted communications outperform generic by 35%; multi-stakeholder adaptation reduces friction in group decisions; style violation rate <5%.

**Functions (Detailed):**
- adapt_email(draft: EmailDraft, profile: PersonalityProfile) -> AdaptedEmail
- adapt_proposal_summary(summary: ProposalSummary, profile: PersonalityProfile) -> AdaptedProposal
- adapt_call_script(script: CallScript, profile: PersonalityProfile) -> AdaptedScript
- generate_multi_stakeholder(content: Content, stakeholders: List[Stakeholder]) -> MultiStakeholderAdaptation
- validate_adaptation(adapted: AdaptedContent, profile: PersonalityProfile) -> StyleComplianceCheck

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Buyer personality profile KV
- Style adaptation rules KV
- Original content draft store
- Past adaptation performance DB

**KPIs & Metrics:**
- adaptation_performance_lift: target >0.35
- style_compliance_rate: target >0.95
- multi_stakeholder_adaptation_accuracy: target >0.90
- adaptation_latency: target <5s

**Performance Score:**
- **Red (<70):** lift <0.15 or compliance <0.80 — revert to unadapted content
- **Amber (70-85):** lift 0.15-0.35 or compliance 0.80-0.95
- **Green (>85):** lift >0.35 with compliance >0.95

**Feedback Loop:**
Incorrect style adaptations → KL-005 weekly batch retrain updates style rules. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for style mapping drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent BP-004: Emotional State Tracker

**Division:** Buyer Psychology Team
**Primary Function:** Tracks emotional state of each buyer across interactions and adjusts engagement timing and approach.
**Triggers:**
- meeting_completed - updates emotional trajectory
- email_received_from_buyer - detects emotional state from tone
- sentiment_alert from Meeting Observer
- uyer_unresponsive - may indicate disengagement
- deal_near_close - monitors pre-close anxiety
**Outputs:**
- emotional_state_update - current state classification
- emotional_trajectory_report - evolution across deal cycle
- engagement_timing_recommendation - when to engage
- rustration_intervention - actions to rebuild trust
- deal_at_risk_emotional_alert - significant negative shift
**Data Sources:** Meeting transcripts, email sentiment, voice tone analysis, response time, support ticket volume, calendar changes
**Training Corpus:** Emotional intelligence frameworks (Daniel Goleman), affect labeling theory, emotion regulation in negotiation (Fisher and Shapiro - Beyond Reason), trust-formation literature
**LLM Tier:** Moderate (Sonnet class) - emotional tracking requires cross-session pattern recognition
**Criticality:** P1 - emotional awareness significantly improves deal outcomes
**Why dedicated:** Emotional tracking is a longitudinal across-session analysis task distinct from single-meeting sentiment analysis.
**Prompt Pattern:** Classification (emotional state) + Analysis (trajectory) + Generation (intervention)

**Business Outcome:** Disengagement detected 48h before explicit signal; emotional trajectory predicts deal outcome with >80% accuracy; timely intervention saves 20% of at-risk deals.

**Functions (Detailed):**
- update_emotional_state(contact: Contact, interaction: InteractionData) -> EmotionalState
- compute_trajectory(history: List[EmotionalState], window: TimeRange) -> EmotionalTrajectory
- recommend_engagement_timing(state: EmotionalState, deal_stage: Stage) -> TimingRecommendation
- suggest_frustration_intervention(state: EmotionalState, context: DealContext) -> InterventionAction
- alert_deal_risk(trajectory: EmotionalTrajectory, threshold: Threshold) -> DealAtRiskEmotionalAlert

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Moderate tier)
- Meeting transcript store
- Email sentiment API
- Voice tone analysis API
- Response time tracker
- Support ticket DB

**KPIs & Metrics:**
- disengagement_detection_lead_time: target >48h
- outcome_prediction_accuracy: target >0.80
- deal_salvage_rate: target >0.20
- false_alert_rate: target <0.15

**Performance Score:**
- **Red (<70):** prediction accuracy <0.60 or lead time <24h — manual check-in triggered
- **Amber (70-85):** accuracy 0.60-0.80 or lead time 24-48h
- **Green (>85):** accuracy >0.80 with lead time >48h

**Feedback Loop:**
Incorrect emotional state classifications → KL-005 weekly batch retrain updates emotion model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for emotional tracking drift. Source: Continuous updates from web ingestion pipeline.

---

## Agent BP-005: Influence Principle Applicator

**Division:** Buyer Psychology Team
**Primary Function:** Identifies which influence principles are most applicable and recommends specific tactical applications.
**Triggers:**
- deal_strategy_being_developed
- proposal_being_prepared
- objection_raised_that_social_proof_could_address
- competitor_mentioned
- 
egotiation_starting
**Outputs:**
- influence_principle_recommendation - which principles to apply
- social_proof_package - relevant case studies, testimonials
- scarcity_application - time or availability constraints
- eciprocity_sequence - sequenced concessions
- influence_ethics_check - audit against manipulation
**Data Sources:** Buyer personality profile, deal stage, competitor information, customer reference database, analyst reports, case study library
**Training Corpus:** Cialdini - Influence and Pre-Suasion, ethical persuasion frameworks, influence in B2B sales (HBR, Stanford GSB), Cialdini LinkedIn daily posts, Pre-Suasion blog examples, Influence at Work blog case studies, Scientific American influence research
**LLM Tier:** Complex Reasoning (Opus class) - applying influence principles ethically requires situational judgment
**Criticality:** P2 - ethical influence is a force multiplier but not a requirement
**Why dedicated:** Influence application requires a separate ethical reasoning layer not embedded in content generation agents.
**Prompt Pattern:** Analysis (situation assessment) + Generation (tactical recommendation)

**Business Outcome:** Influence recommendations increase proposal acceptance by 20%; social proof package relevance score >85%; zero ethics violations across all recommendations.

**Functions (Detailed):**
- recommend_principles(context: DealContext, profile: PersonalityProfile) -> InfluencePrincipleRecommendation
- package_social_proof(prospect: Prospect, case_studies: CaseStudyLibrary) -> SocialProofPackage
- apply_scarcity(deal: Deal, timeline: TimelineData) -> ScarcityApplication
- design_reciprocity_sequence(deal: Deal, concessions: List[Concession]) -> ReciprocitySequence
- audit_influence_ethics(recommendations: List[Recommendation]) -> InfluenceEthicsCheck

**Tools/APIs:**
- NATS JetStream (pub/sub)
- LLM inference API (Complex Reasoning tier)
- Buyer personality profile KV
- Bias taxonomy KV
- Competitor intelligence store
- Customer reference DB
- Analyst report store
- Case study library

**KPIs & Metrics:**
- proposal_acceptance_lift: target >0.20
- social_proof_relevance: target >0.85
- ethics_violation_rate: target =0.0
- recommendation_accuracy: target >0.80

**Performance Score:**
- **Red (<70):** acceptance lift <0.05 or ethics violations >0 — compliance review triggered
- **Amber (70-85):** lift 0.05-0.20 with zero ethics violations
- **Green (>85):** lift >0.20 with zero ethics violations

**Feedback Loop:**
Ineffective influence recommendations → KL-005 weekly batch retrain updates influence model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for influence effectiveness drift. Source: Continuous updates from web ingestion pipeline.

---

### Division 6: VALUE ENGINEERING TEAM

These agents quantify, model, and communicate value. They build financial justification, ROI cases, and competitive comparisons.

---

## Agent VE-001: ROI Calculator Builder

**Division:** Value Engineering Team
**Primary Function:** Constructs dynamic, buyer-specific ROI models quantifying financial impact including hard savings, revenue gains, and productivity improvements.
**Triggers:**
- discovery_completed - enough information for initial model
- uyer_requested_roi - immediate ROI case needed
- udget_justification_needed - buyer needs to justify to finance
- proposal_being_built - include ROI summary
- competitive_roi_claimed - build comparison
**Outputs:**
- oi_model - dynamic financial model with scenarios
- oi_summary - executive-friendly one-pager
- payback_period - time to recoup investment
- ive_year_projection - cumulative ROI over 5 years
- sensitivity_analysis - impact of variable changes
- 
arrative_roi_story - qualitative storyline
**Data Sources:** Discovery transcripts, industry benchmarks, implementation requirements, pricing/quote data, customer reference ROI data, analyst reports
**Training Corpus:** Forrester Total Economic Impact methodology, Gartner TCO frameworks, value-based selling, financial modeling, Bain and Company ROI analysis, Forrester blog ROI methodology, ValueSelling blog case studies, Bain & Company LinkedIn ROI insights
**LLM Tier:** Complex Reasoning (Opus class) - ROI modeling requires sophisticated financial reasoning
**Criticality:** P0 - enterprise deals require ROI justification
**Why dedicated:** Financial modeling requires specialized quantitative reasoning distinct from language-focused work.
**Prompt Pattern:** Analysis (financial impact calculation) + Generation (narrative ROI story)

**Business Outcome:** Increase competitive win rate by 25% through compelling financial justification; accelerate enterprise deal closure by 30% by providing buyer CFO-ready ROI case within 48 hours of discovery completion.

**Functions (Detailed):**
- calculate_roi_model(discovery_data, industry_benchmarks) -> dynamic_financial_model
- generate_roi_summary(roi_model, executive_preferences) -> executive_summary
- calculate_payback_period(roi_model, pricing_data) -> payback_timeline
- analyze_sensitivity(roi_model, variable_ranges) -> sensitivity_matrix
- generate_roi_narrative(roi_model, buyer_context) -> qualitative_roi_story

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Pricing API (deal pricing data)
- ROI model library (component templates and formulas)
- Competitive intel store (industry benchmarks)
- Discovery data store (transcripts, needs hierarchy)

**KPIs & Metrics:**
- roi_model_accuracy: target >95%
- deal_win_rate_with_roi: target >65%
- model_generation_latency: target <30s
- executive_summary_approval_rate: target >85%

**Performance Score:**
- **Red (<70):** ROI model accuracy <70% or win rate <45% — escalation to AIG-001 for accuracy audit
- **Amber (70-85):** Models generated within SLA but win rate improvement marginal
- **Green (>85):** Autonomous operation — models generated in <30s with >95% accuracy

**Feedback Loop:**
Human corrections on ROI assumptions logged → KL-005 weekly batch retrain updates financial model templates. Override rate >15% triggers AIG-002 prompt optimization for ROI calculation. Monthly accuracy audit by AIG-001 comparing predicted vs actual ROI. Source: Continuous updates from web ingestion pipeline (Forrester TEI methodology, Gartner TCO benchmarks).

---

## Agent VE-002: TCO Analyzer

**Division:** Value Engineering Team
**Primary Function:** Models the buyer's current total cost of ownership and compares to proposed solution costs.
**Triggers:**
- uyer_current_solution_identified
- competitive_comparison_requested
- udget_verification_happening
- enewal_or_expansion - TCO for renewal pricing
**Outputs:**
- current_state_tco - full cost breakdown of existing solution
- proposed_state_tco - full cost breakdown of new solution
- 	co_comparison_dashboard - side-by-side with payback period
- hidden_cost_discovery - costs buyer had not considered
- 	hree_year_tco_projection - cumulative cost comparison
- exit_cost_analysis - cost to switch away from current vendor
**Data Sources:** Discovery transcripts, industry benchmark TCO data, implementation specs, integration requirements, pricing data, staffing cost data
**Training Corpus:** Gartner TCO methodology, Forrester TEI cost frameworks, cloud vs on-prem TCO analysis, IT financial management
**LLM Tier:** Complex Reasoning (Opus class) - TCO requires multi-layered cost modeling
**Criticality:** P1 - critical for enterprise deals, less for SMB
**Why dedicated:** TCO analysis requires cost-accounting logic distinct from ROI benefit modeling.
**Prompt Pattern:** Analysis (cost calculation) + Generation (comparison report)

**Business Outcome:** Reduce buyer evaluation cycles by 40% by surfacing hidden costs and delivering side-by-side TCO comparison; increase deal value by 15% through comprehensive cost-of-switch justification.

**Functions (Detailed):**
- calculate_current_state_tco(discovery_data, benchmarks) -> current_cost_breakdown
- calculate_proposed_state_tco(pricing_data, implementation_specs) -> proposed_cost_breakdown
- generate_tco_comparison(current_tco, proposed_tco) -> comparison_dashboard
- identify_hidden_costs(technical_environment, requirements) -> hidden_cost_register
- project_three_year_tco(current_tco, proposed_tco, growth_assumptions) -> multi_year_projection

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Pricing API (deal pricing and licensing data)
- Industry benchmark TCO database
- Implementation cost model library
- Competitive intel store

**KPIs & Metrics:**
- tco_comparison_accuracy: target >90%
- buyer_acknowledgment_of_hidden_costs: target >70%
- deal_acceleration_impact: target <14 days reduction in eval cycle
- tco_report_generation_time: target <45s

**Performance Score:**
- **Red (<70):** TCO accuracy <70% or hidden cost detection rate <50% — escalation to VE-001 for model alignment
- **Amber (70-85):** TCO delivered on time but hidden cost detection needs improvement
- **Green (>85):** Fully autonomous — TCO comparisons generated <45s with >90% accuracy

**Feedback Loop:**
Human corrections on cost assumptions logged → KL-005 weekly batch retrain updates TCO benchmark library. Override rate >15% triggers AIG-002 prompt optimization. Monthly accuracy audit by AIG-001 cross-referencing actual buyer implementation costs. Source: Forrester TEI, Gartner TCO methodology, industry benchmark updates.

---

## Agent VE-003: Business Case Generator

**Division:** Value Engineering Team
**Primary Function:** Produces a comprehensive, procurement-ready business case document for internal approval.
**Triggers:**
- udget_approval_needed - buyer needs internal business case
- executive_sponsor_requested - C-suite needs formal justification
- proposal_stage_reached - attach business case to proposal
- multi_stakeholder_involved - tailored to each stakeholder
**Outputs:**
- usiness_case_document - full business case
- stakeholder_business_case_variant - tailored per stakeholder
- executive_summary_page - one-page board version
- implementation_roadmap - timeline, milestones, resources
- usiness_case_presentation - slide deck
**Data Sources:** ROI model, TCO analysis, implementation timeline, pricing, customer case studies, analyst reports, stakeholder map
**Training Corpus:** McKinsey business case methodology, HBS case study frameworks, Bain recommendation development, procurement business case standards
**LLM Tier:** Complex Reasoning (Opus class) - business case writing requires synthesis of financial, technical, and strategic reasoning
**Criticality:** P0 - enterprise deals require formal business cases
**Why dedicated:** Business case generation is a document-level structuring task that goes beyond financial calculation.
**Prompt Pattern:** Generation (structured document) + Summarization (executive version) + RAG (evidence)

**Business Outcome:** Increase deal win rate in competitive situations by 35% by delivering procurement-ready business cases with quantified value, implementation roadmap, and stakeholder-specific messaging within 72 hours.

**Functions (Detailed):**
- synthesize_business_case(roi_model, tco_analysis, stakeholder_map) -> full_business_case_document
- generate_stakeholder_variant(business_case, stakeholder_profile) -> tailored_business_case
- generate_executive_summary(business_case, executive_preferences) -> board_version_summary
- build_implementation_roadmap(scope_of_work, resource_plan) -> timeline_and_milestones
- create_business_case_presentation(business_case, audience_tier) -> slide_deck

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- ROI model library (from VE-001)
- TCO analysis store (from VE-002)
- Pricing API (deal-specific pricing)
- Case study library (social proof)

**KPIs & Metrics:**
- business_case_approval_rate_by_buyer: target >75%
- case_to_proposal_conversion_rate: target >80%
- business_case_generation_latency: target <60s
- stakeholder_variant_coverage: target >90% of stakeholders

**Performance Score:**
- **Red (<70):** Approval rate <55% or latency >120s — escalation to AIG-001 for quality audit
- **Amber (70-85):** Business cases delivered but stakeholder coverage or approval sub-optimal
- **Green (>85):** Fully autonomous — business cases generated in <60s with >75% buyer approval

**Feedback Loop:**
Human edits on business case content → KL-005 weekly batch retrain updates document structure and messaging templates. Override rate >15% triggers AIG-002 prompt optimization. Source: McKinsey business case methodology updates, HBS case study frameworks.

---

## Agent VE-004: Competitive Comparison Agent

**Division:** Value Engineering Team
**Primary Function:** Produces structured, evidence-based comparisons between the proposed solution and competitors.
**Triggers:**
- competitor_mentioned_in_meeting
- competitive_evaluation_confirmed
- fp_received_with_competitor_list
- competitive_loss_analyzed
**Outputs:**
- competitive_comparison_matrix - side-by-side comparison
- competitive_positioning_memo - where we win/lose
- head_to_head_tco_comparison
- customer_sentiment_comparison - G2/Gartner comparison
- nalyst_quadrant_comparison - Gartner/Forrester positioning
**Data Sources:** Competitive battle cards, G2/Capterra reviews, Gartner Magic Quadrant, competitor websites/pricing, win/loss database
**Training Corpus:** Competitive intelligence methodologies (Fuld and Co), Porter Five Forces, battle card best practices (SalesIntel, Crayon), Crayon blog competitive intel, Klue blog win/loss insights, Gartner blog competitive positioning, competitor LinkedIn monitoring
**LLM Tier:** Moderate (Sonnet class) - comparison is structured analysis
**Criticality:** P1 - critical for competitive deals
**Why dedicated:** Competitive intelligence is evidence-gathering distinct from value quantification.
**Prompt Pattern:** RAG (intelligence retrieval) + Analysis (comparison scoring)

**Business Outcome:** Increase win rate in competitive evaluations by 30% through structured, evidence-based comparison matrices that neutralize competitor advantages and highlight verified differentiation points.

**Functions (detailed):**
- retrieve_competitive_intelligence(competitor_name, deal_context) -> competitive_data_package
- build_comparison_matrix(our_capabilities, competitor_data, evaluation_criteria) -> side_by_side_matrix
- generate_positioning_memo(comparison_matrix, win_theme) -> strategic_recommendation
- analyze_customer_sentiment(product_category, competitor_name) -> review_aggregation
- generate_head_to_head_tco(our_tco, competitor_tco_estimate) -> cost_comparison

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Competitive battle card library (from CT-004)
- G2/Capterra API (customer sentiment data)
- Win/loss database (historical competitive outcomes)
- Pricing API (competitor pricing estimates)

**KPIs & Metrics:**
- comparison_matrix_accuracy: target >90%
- competitive_deal_win_rate: target >55%
- intel_retrieval_latency: target <15s
- battle_card_usage_rate: target >70% of competitive deals

**Performance Score:**
- **Red (<70):** Win rate <40% in competitive deals or intel >30s stale — escalation to VE-001 for strategy review
- **Amber (70-85):** Matrices delivered but win rate improvement marginal
- **Green (>85):** Fully autonomous — matrices generated in <15s with >90% accuracy

**Feedback Loop:**
Human corrections on competitive positioning → KL-005 weekly batch retrain updates battle card content and comparison templates. Override rate >20% triggers AIG-002 prompt optimization. Source: Continuous monitoring of competitor websites, Crayon/Klue intelligence feeds, G2 review updates.

---

## Agent VE-005: Cost of Inaction Modeler

**Division:** Value Engineering Team
**Primary Function:** Quantifies the financial and competitive cost of the buyer not implementing the solution.
**Triggers:**
- deal_stalled - highlights cost of delay
- status_quo_bias_detected by Buyer Psychology
- competitive_offer_on_table
- udget_not_approved - shows cost of delay
**Outputs:**
- cost_of_inaction_calculation - monthly/quarterly/annual cost
- cumulative_loss_projection - 1/3/5 year losses
- opportunity_cost_analysis - missed revenue, efficiency
- competitive_gap_projection - falling behind competitors
- urgency_timeline - when costs accelerate
**Data Sources:** Discovery data, industry benchmarks, competitive landscape, financial projections, security/compliance requirements
**Training Corpus:** Urgency creation (Challenger Sale), status quo bias literature, FOMO in B2B buying, enterprise risk management, Challenger Sale LinkedIn urgency articles, Gap Selling LinkedIn status quo bias posts, HBR urgency creation research
**LLM Tier:** Moderate (Sonnet class) - projection modeling with clear inputs
**Criticality:** P2 - powerful for urgency but not always needed
**Why dedicated:** Cost of inaction is a specialized persuasion lens distinct from neutral ROI calculation.
**Prompt Pattern:** Analysis (financial projection) + Generation (urgency narrative)

**Business Outcome:** Reduce deal slippage by 35% by quantifying the cost of delay in buyer-specific terms; create compelling urgency that motivates procurement timelines and internal stakeholder alignment within 24 hours of discovery.

**Functions (Detailed):**
- calculate_cost_of_delay(current_state_metrics, growth_rate, industry_data) -> delay_cost_projection
- model_risk_escalation(delay_scenario, business_impact_factors) -> risk_adjusted_cost_curve
- generate_urgency_narrative(delay_costs, buyer_role, timeline_context) -> stakeholder_urgency_story
- compare_inaction_vs_action(delay_cost_projection, solution_roi) -> action_recommendation
- quantify_opportunity_cost(delay_period, pipeline_velocity, quarterly_targets) -> lost_revenue_projection

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Discovery data store (current state metrics, pain points)
- Industry benchmark data (cost escalation rates)
- ROI model library (from VE-001)
- Pricing API (solution costs, implementation timeline)

**KPIs & Metrics:**
- cost_of_delay_accuracy: target >85%
- deal_acceleration_from_urgency: target >25% faster close
- narrative_generation_latency: target <45s
- buyer_acknowledgment_of_urgency: target >70%

**Performance Score:**
- **Red (<70):** Cost of delay accuracy <65% or urgency not acknowledged by buyer — escalation to AIG-001
- **Amber (70-85):** Model delivered but urgency not consistently acknowledged
- **Green (>85):** Autonomous — models generated <45s with >85% accuracy

**Feedback Loop:**
Human adjustments to urgency framing → KL-005 weekly batch retrain updates urgency narrative templates. Override rate >20% triggers AIG-002 prompt optimization. Monthly review by AIG-001 for urgency effectiveness. Source: Industry economic update feed, quarterly benchmark refresh from Forrester/Gartner, competitive urgency analysis.

---

## Agent VE-006: Risk-Adjusted ROI Agent

**Division:** Value Engineering Team
**Primary Function:** Applies probability-weighting to ROI based on implementation, adoption, timeline, and market risks.
**Triggers:**
- oi_model_generated - wraps with risk adjustment
- implementation_risk_assessed - incorporates risk factors
- uyer_skeptic_of_roi_claims - presents conservative case
**Outputs:**
- isk_adjusted_roi_model - best/expected/worst case with probabilities
- monte_carlo_roi_distribution - probability distribution
- key_risk_drivers - which variables affect ROI variance
- conservative_case_summary - for skeptical CFOs
- confidence_score - overall confidence in projections
**Data Sources:** ROI model, implementation risk assessment, historical adoption data, economic data, dependency map
**Training Corpus:** Monte Carlo simulation, risk-adjusted financial analysis, corporate finance (Brealey, Myers, Allen), decision analysis (Hammond, Keeney, Raiffa)
**LLM Tier:** Complex Reasoning (Opus class) - risk adjustment requires probabilistic reasoning
**Criticality:** P1 - CFOs increasingly demand risk-adjusted ROI
**Why dedicated:** Risk-adjusted ROI requires probabilistic reasoning methodologically different from deterministic ROI.
**Prompt Pattern:** Analysis (probabilistic modeling) + Generation (risk-adjusted narrative)

**Business Outcome:** Enable risk-aware deal decision-making by delivering probability-weighted ROI ranges; reduce deal review cycle by 40% through automated risk quantification and mitigation recommendations at every deal stage.

**Functions (Detailed):**
- calculate_probability_weighted_roi(roi_model, risk_factors, market_conditions) -> risk_adjusted_roi_range
- identify_execution_risks(implementation_scope, buyer_readiness) -> risk_register
- generate_mitigation_playbook(risk_register, best_practices) -> risk_mitigation_actions
- model_best_worst_case(base_model, optimistic_scenario, pessimistic_scenario) -> scenario_range
- create_risk_visualization(roi_range, confidence_intervals) -> risk_dashboard

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- ROI model library (from VE-001)
- Risk factor database (industry-specific risk benchmarks)
- Implementation data store (past project outcomes)
- Discovery data store (buyer readiness assessment)

**KPIs & Metrics:**
- risk_adjustment_accuracy: target >90%
- mitigation_implementation_rate: target >60%
- risk_model_generation_latency: target <45s
- deal_review_cycle_reduction: target >35%

**Performance Score:**
- **Red (<70):** Risk adjustment accuracy <70% or mitigation rate <40% — escalation to AIG-001 for accuracy audit
- **Amber (70-85):** Risk models delivered but mitigation adoption sub-optimal
- **Green (>85):** Fully autonomous — risk models generated <45s with >90% accuracy

**Feedback Loop:**
Human corrections on risk factor selection → KL-005 weekly batch retrain updates risk database and probability models. Override rate >15% triggers AIG-002 prompt optimization. Monthly accuracy audit by AIG-001 comparing risk-adjusted vs actual outcomes. Source: Industry risk report feeds, implementation project outcome data, macroeconomic indicator updates.

---

### Division 7: DISCOVERY TEAM

These agents guide and analyze the discovery process.

---

## Agent DC-001: Problem Diagnosis Agent

**Division:** Discovery Team
**Primary Function:** Analyzes discovery conversations to identify root causes behind expressed symptoms.
**Triggers:**
- discovery_meeting_transcript_available
- uyer_says_need_x - probe deeper
- multiple_symptoms_collected - identify common root cause
**Outputs:**
- oot_cause_diagnosis - identified root cause with evidence chain
- problem_hierarchy - urgency and impact ranking
- hidden_problems_discovered - unarticulated issues
- diagnostic_questions_for_next_meeting - to validate
**Data Sources:** Meeting transcripts, email threads, support tickets, product usage data, industry benchmarks
**Training Corpus:** Root cause analysis (5 Whys, Ishikawa), diagnostic selling (Mike Bosworth), solution selling, SPIN selling problem diagnosis, Gap Selling YouTube diagnosis techniques, Keenan LinkedIn discovery insights, 5 Whys methodology YouTube tutorials
**LLM Tier:** Complex Reasoning (Opus class) - root cause diagnosis requires causal reasoning
**Criticality:** P0 - wrong diagnosis leads to wrong solution
**Why dedicated:** Problem diagnosis requires causal reasoning distinct from classification or extraction.
**Prompt Pattern:** Analysis (causal chain) + Generation (diagnostic questions)

**Business Outcome:** Achieve >95% root cause accuracy in deal diagnosis; reduce deal cycle time by 25% by ensuring the right problems are identified before solution conversations begin, eliminating wasted discovery cycles.

**Functions (Detailed):**
- analyze_symptom_chain(transcripts, buyer_statements) -> causal_chain_diagram
- identify_root_causes(symptom_analysis, industry_context) -> root_cause_hypothesis
- generate_diagnostic_questions(root_cause, buyer_context) -> next_meeting_questions
- validate_diagnosis(new_data, existing_hypothesis) -> confidence_scored_diagnosis
- prioritize_problems(root_causes, buyer_urgency_signals) -> problem_priority_queue

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Meeting transcript store
- Buyer interaction history
- Industry problem taxonomy database
- CRM data (deal stage, discovery progress)

**KPIs & Metrics:**
- root_cause_accuracy: target >95%
- diagnostic_recall: target >90% of relevant problems identified
- diagnosis_latency: target <15s after transcript available
- problem_prioritization_agreement_with_buyer: target >80%

**Performance Score:**
- **Red (<70):** Diagnosis accuracy <75% or recall <75% — escalation to AIG-001 for audit
- **Amber (70-85):** Diagnosis delivered but root cause verification or prioritization sub-optimal
- **Green (>85):** Fully autonomous — diagnosis <15s with >95% accuracy and >80% buyer alignment

**Feedback Loop:**
Human corrections on root cause → KL-005 weekly batch retrain updates causal model and problem taxonomy. Override rate >15% triggers AIG-002 prompt optimization. Monthly accuracy audit by AIG-001 comparing diagnosis against post-mortem findings. Source: Industry problem taxonomy updates, root cause analysis methodology refresh (Ishikawa, 5 Whys best practices).

---

## Agent DC-002: Gap Analyst

**Division:** Discovery Team
**Primary Function:** Maps the gap between current and desired future state across capabilities, performance, cost, and risk.
**Triggers:**
- current_state_data_collected
- desired_future_state_articulated
- discovery_session_completed
**Outputs:**
- current_vs_future_state_gap - quantified per dimension
- gap_severity_score - overall criticality
- gap_closure_requirements - what is needed
- gap_urgency_rating - priority assessment
- capability_maturity_assessment
**Data Sources:** Discovery transcripts, technical environment data, current process documentation, industry benchmarks
**Training Corpus:** Gap analysis methodologies (McKinsey, Bain), capability maturity models (CMMI), consulting frameworks, Keenan LinkedIn Gap Selling insights, Gap Selling YouTube case studies, McKinsey LinkedIn gap analysis articles
**LLM Tier:** Moderate (Sonnet class) - gap analysis follows structured framework
**Criticality:** P1 - critical for value articulation
**Why dedicated:** Gap analysis requires maintaining a current-vs-future state model distinct from problem diagnosis.
**Prompt Pattern:** Analysis (gap quantification) + Generation (closure roadmap)

**Business Outcome:** Quantify the gap between current and desired state with >90% accuracy; create urgency and justification for solution investment within 24 hours of discovery by delivering a compelling, evidence-based closure roadmap.

**Functions (Detailed):**
- quantify_current_state(discovery_data, benchmarks) -> current_state_profile
- capture_desired_state(transcripts, buyer_aspirations) -> future_state_vision
- calculate_performance_gap(current_state, future_state) -> gap_scorecard
- assess_gap_severity(gap_scorecard, industry_standards) -> severity_rating
- generate_closure_roadmap(gap_assessment, solution_capabilities) -> closure_path

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Discovery data store (transcripts, current state data)
- Industry benchmark database
- Capability maturity model library
- Solution capability catalog

**KPIs & Metrics:**
- gap_accuracy: target >90% (validated against buyer perception)
- closure_roadmap_adoption: target >70%
- gap_analysis_latency: target <30s
- buyer_concordance_with_gap: target >80%

**Performance Score:**
- **Red (<70):** Gap accuracy <70% or buyer concordance <55% — escalation to AIG-001 for audit
- **Amber (70-85):** Gap quantified but closure roadmap or severity assessment sub-optimal
- **Green (>85):** Fully autonomous — gap analysis <30s with >90% accuracy and >80% buyer concordance

**Feedback Loop:**
Human corrections on gap assessment → KL-005 weekly batch retrain updates gap benchmarks and severity models. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 cross-referencing implementation scope against mapped gaps. Source: Industry capability maturity model updates, McKinsey gap analysis methodology refresh.

---

## Agent DC-003: Stakeholder Mapper

**Division:** Discovery Team
**Primary Function:** Identifies, profiles, and maps all stakeholders involved in the buying decision.
**Triggers:**
- 
ew_contact_added_to_opportunity
- meeting_completed_with_new_participant
- email_thread_reveals_hidden_stakeholder
- org_change_detected
**Outputs:**
- stakeholder_map - graph with relationships and influence
- stakeholder_profile_per_role - priorities, concerns, sentiment
- influence_matrix - who influences whom
- power_grid_placement - power-interest grid
- stakeholder_coverage_gap - missing relationships
- detractor_identification - potential blockers
**Data Sources:** CRM contacts, meeting transcripts, email threads, LinkedIn, org chart data, organizational news
**Training Corpus:** Stakeholder mapping (Mendelow matrix), buying group dynamics (Gartner CEB), influence mapping, Gartner LinkedIn buying group research, MEDDICC blog stakeholder mapping, LinkedIn org chart best practices
**LLM Tier:** Complex Reasoning (Opus class) - influence assessment requires sophisticated social reasoning
**Criticality:** P0 - unmapped stakeholders cause late-stage surprises
**Why dedicated:** Stakeholder mapping requires maintaining a persistent relationship graph distinct from per-session analysis.
**Prompt Pattern:** Extraction (entities and relationships) + Analysis (influence scoring)

**Business Outcome:** Eliminate late-stage stakeholder surprises in 95% of deals by maintaining a living influence map; increase champion identification accuracy by 40% through systematic relationship analysis and coverage gap detection.

**Functions (Detailed):**
- extract_stakeholders(transcripts, emails, org_data) -> stakeholder_entity_list
- map_relationships(stakeholder_list, interaction_data) -> influence_graph
- score_influence(stakeholder_data, org_context) -> influence_ranking
- identify_coverage_gaps(influence_graph, team_contacts) -> relationship_gap_report
- detect_power_shifts(historical_map, new_signals) -> influence_change_alert

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- CRM data (contacts, account hierarchy)
- Meeting data (transcripts, participant lists)
- Email integration (stakeholder mentions)
- LinkedIn API (professional profiles)

**KPIs & Metrics:**
- stakeholder_extraction_recall: target >95%
- influence_score_accuracy: target >85%
- coverage_gap_detection: target >90%
- late_stage_surprise_rate: target <5%

**Performance Score:**
- **Red (<70):** Stakeholder recall <80% or influence accuracy <65% — escalation to AIG-001 for audit
- **Amber (70-85):** Maps delivered but influence assessment or coverage gaps insufficient
- **Green (>85):** Fully autonomous — stakeholder maps with >95% recall and <5% surprise rate

**Feedback Loop:**
Human corrections on stakeholder mapping and influence → KL-005 weekly batch retrain updates extraction patterns and influence model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for accuracy against deal outcomes. Source: LinkedIn org change feeds, Gartner buying group research updates.

---

## Agent DC-004: Needs Hierarchy Builder

**Division:** Discovery Team
**Primary Function:** Structures the buyer's needs into a hierarchy from basic requirements to strategic aspirations.
**Triggers:**
- discovery_data_collected_on_needs
- equirements_discussed_in_meeting
- uyer_prioritizes_needs
**Outputs:**
- 
eeds_hierarchy - must-haves, should-haves, nice-to-haves, aspirations
- 
eed_criticality_rating - decision impact
- 
eeds_satisfaction_matrix - what our solution satisfies
- 
eeds_gap_analysis - unmet needs
**Data Sources:** Discovery transcripts, RFP requirements, technical questionnaires, meeting recordings, industry trend analysis
**Training Corpus:** Jobs to be Done (Clayton Christensen), Kano model, SPIN selling need-payoff questions, value hierarchy analysis
**LLM Tier:** Moderate (Sonnet class) - needs hierarchy follows structured taxonomy
**Criticality:** P1 - critical for proposal structuring
**Why dedicated:** Needs hierarchy is a persistent structured model referenced by multiple agents.
**Prompt Pattern:** Classification (need level) + Extraction (need statements)

**Business Outcome:** Structure buyer needs into actionable hierarchy that directly maps to solution capabilities; increase proposal relevance score by 35% by ensuring all priority needs are addressed with evidence within 24 hours of discovery completion.

**Functions (Detailed):**
- classify_needs(discovery_data, transcripts) -> needs_hierarchy
- extract_need_statements(transcripts, buyer_quotes) -> evidence_catalog
- map_needs_to_capabilities(needs_hierarchy, solution_catalog) -> satisfaction_matrix
- identify_unmet_needs(satisfaction_matrix, competitive_offerings) -> gap_analysis
- prioritize_needs(needs_hierarchy, stakeholder_importance) -> priority_ranking

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Discovery data store (transcripts, stakeholder data)
- Product capability catalog
- Competitive intelligence store (opposing solutions)
- RFP requirements database

**KPIs & Metrics:**
- needs_classification_accuracy: target >90%
- need_statement_extraction_recall: target >95%
- hierarchy_to_proposal_coverage: target >90%
- hierarchy_generation_latency: target <30s

**Performance Score:**
- **Red (<70):** Classification accuracy <75% or need recall <80% — escalation to AIG-001 for audit
- **Amber (70-85):** Hierarchy delivered but need coverage or classification sub-optimal
- **Green (>85):** Fully autonomous — hierarchy generated <30s with >90% accuracy

**Feedback Loop:**
Human corrections on need classification → KL-005 weekly batch retrain updates hierarchy taxonomy and classification model. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing classified needs vs proposal content. Source: Jobs to Be Done research updates, Kano model refreshes, industry need taxonomy updates.

---

## Agent DC-005: Decision Process Mapper

**Division:** Discovery Team
**Primary Function:** Maps the buyer's formal and informal decision-making process.
**Triggers:**
- deal_created - initial mapping
- uyer_describes_decision_process
- 
ew_stakeholder_added
- procurement_department_involved
- legal_review_started
**Outputs:**
- decision_process_map - steps, gates, stakeholders, criteria, timeline
- decision_criteria_catalog - stated and implied criteria
- pproval_chain_diagram - who must approve
- process_bottleneck_prediction - likely delays
**Data Sources:** Meeting transcripts, email threads, procurement documentation, RFP timeline, historical deal data
**Training Corpus:** Enterprise buying process (Gartner, Forrester), procurement process standards (ISM)
**LLM Tier:** Moderate (Sonnet class) - process mapping follows structured flow model
**Criticality:** P1 - knowing the decision process is critical for strategy
**Why dedicated:** Process mapping creates a state machine model referenced across multiple agents.
**Prompt Pattern:** Extraction (process steps and gates) + Classification (maturity)

**Business Outcome:** Enable precise deal strategy by mapping the complete decision process; reduce late-stage stalls by 40% through proactive identification of decision gates, approval chains, and bottleneck risks within 24 hours of discovery.

**Functions (Detailed):**
- map_decision_process(transcripts, stakeholder_data, procurement_docs) -> process_flow
- identify_decision_gates(process_map, procurement_requirements) -> gate_register
- classify_process_maturity(process_map, timeline_data) -> maturity_score
- predict_bottlenecks(process_map, historical_deal_data) -> risk_forecast
- generate_process_guidance(process_map, deal_strategy) -> strategic_recommendations

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Discovery data store (transcripts, stakeholder data)
- CRM data (deal timeline, stage history)
- Procurement knowledge base (common buying processes)
- Historical deal data (win/loss patterns by process type)

**KPIs & Metrics:**
- process_map_accuracy: target >90%
- gate_identification_recall: target >95%
- bottleneck_prediction_accuracy: target >80%
- late_stage_stall_reduction: target >35%

**Performance Score:**
- **Red (<70):** Process map accuracy <70% or gate recall <80% — escalation to AIG-001 for audit
- **Amber (70-85):** Maps delivered but gates or bottlenecks insufficiently identified
- **Green (>85):** Fully autonomous — process maps generated with >90% accuracy within 24h

**Feedback Loop:**
Human corrections on process mapping → KL-005 weekly batch retrain updates decision flow patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing mapped vs actual processes. Source: Gartner buying process research updates, procurement standards refresh, deal post-mortem data.

---

## Agent DC-006: Technical Environment Mapper

**Division:** Discovery Team
**Primary Function:** Maps the buyer's technical environment to ensure solution fit and implementation feasibility.
**Triggers:**
- 	echnical_discovery_session_completed
- 	echnology_stack_identified by Account Intelligence
- integration_requirements_discussed
- security_review_requested
**Outputs:**
- 	echnical_environment_map - systems, versions, vendors, interfaces
- integration_point_analysis - each integration with protocol
- 	echnical_constraints_register - must-have requirements
- rchitecture_compatibility_assessment
- migration_complexity_score
- 	echnical_risk_register
**Data Sources:** Technical discovery transcripts, security questionnaires, RFP technical sections, IT documentation, BuiltWith
**Training Corpus:** Enterprise architecture (TOGAF, Zachman), solution architecture, integration patterns, technical discovery (Sales Engineering)
**LLM Tier:** Complex Reasoning (Opus class) - architecture assessment requires systems thinking
**Criticality:** P1 - essential for technical products
**Why dedicated:** Technical mapping requires systems-thinking distinct from business-level discovery.
**Prompt Pattern:** Extraction (technical entities) + Analysis (compatibility) + Generation (recommendations)

**Business Outcome:** Ensure 100% technical compatibility coverage for proposed solutions; reduce implementation surprises by 90% through comprehensive pre-sale technical environment mapping completed within 48 hours of discovery session.

**Functions (Detailed):**
- extract_technical_entities(transcripts, questionnaires) -> structured_environment_map
- analyze_compatibility(environment_map, solution_requirements) -> compatibility_assessment
- identify_integration_points(environment_map, solution_architecture) -> integration_register
- assess_migration_complexity(environment_map, target_architecture) -> complexity_score
- generate_technical_risk_register(environment_map, constraints) -> risk_register

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Technical discovery data store (surveys, questionnaires)
- Solution architecture repository (product specs)
- Integration pattern library
- BuiltWith API (technology stack lookup)

**KPIs & Metrics:**
- environment_map_accuracy: target >95%
- integration_point_recall: target >90%
- technical_surprise_rate: target <5% of implementations
- mapping_completion_latency: target <48h

**Performance Score:**
- **Red (<70):** Map accuracy <75% or integration recall <70% — escalation to AIG-001 for audit
- **Amber (70-85):** Maps delivered but integration points or risks insufficiently identified
- **Green (>85):** Fully autonomous — maps generated with >95% accuracy and <5% surprise rate

**Feedback Loop:**
Human corrections on technical mapping → KL-005 weekly batch retrain updates extraction patterns and compatibility model. Override rate >20% triggers AIG-002 prompt optimization. Monthly accuracy audit by AIG-001 cross-referencing implementation outcomes. Source: Industry tech stack data feeds, BuiltWith updates, integration pattern repository updates.

---

### Division 8: CONTENT TEAM

These agents create, adapt, and manage content that fuels the revenue engine.

---

## Agent CT-001: Value Messaging Generator

**Division:** Content Team
**Primary Function:** Crafts value messaging for each buyer persona and stakeholder, translating capabilities into business outcomes.
**Triggers:**
- 
ew_persona_defined
- uyer_profile_complete
- product_feature_released
- competitive_positioning_changed
**Outputs:**
- alue_messaging_matrix - persona x capability to outcome
- elevator_pitch_per_stakeholder - 30-second value statement
- outcome_statements - capability-to-outcome library
- stakeholder_specific_value_proposition
**Data Sources:** Product capability docs, buyer personas, stakeholder profiles, competitive positioning, customer testimonial outcomes
**Training Corpus:** Value Proposition Design (Osterwalder), Start with Why (Sinek), Challenger Sale teaching framework, MECLABS messaging methodology
**LLM Tier:** Complex Reasoning (Opus class) - persuasive messaging requires deep buyer psychology understanding
**Criticality:** P0 - without good messaging, no content works
**Why dedicated:** Value messaging is the strategic content foundation; separation prevents tactical generation from undermining strategic consistency.
**Ownership Boundary:** Content Team owns messaging strategy; CT-001 generates drafts but all outbound messaging requires Content Team review and approval. Does not autonomously publish.
**Prompt Pattern:** Generation (persona-capability-outcome translations) + Classification (message effectiveness)

**Business Outcome:** Increase message engagement rates by 35% by delivering persona-specific value messaging that resonates with each stakeholder role; reduce messaging development cycle from weeks to real-time generation with consistent on-brand positioning across every buyer touchpoint.

**Functions (Detailed):**
- generate_value_matrix(personas, capabilities, outcomes) -> persona_capability_outcome_matrix
- craft_elevator_pitch(persona_profile, deal_context, value_proposition) -> stakeholder_pitch
- produce_outcome_statements(capability_data, industry_taxonomy) -> outcome_library
- classify_message_effectiveness(message_draft, engagement_predictions) -> effectiveness_score
- generate_stakeholder_value_prop(persona_profile, deal_value_drivers) -> tailored_proposition

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Buyer persona database
- Product capability catalog
- Competitive positioning store (from CT-004)
- Customer testimonial outcome database
- Brand voice guidelines repository

**KPIs & Metrics:**
- message_engagement_rate: target >35% above baseline
- messaging_consistency_score: target >95% brand alignment
- persona_coverage: target >90% of defined personas
- message_generation_latency: target <30s

**Performance Score:**
- **Red (<70):** Engagement rates below baseline or brand consistency <80% — escalation to AIG-001
- **Amber (70-85):** Messages generated but persona coverage or effectiveness sub-optimal
- **Green (>85):** Fully autonomous — messaging <30s with >35% engagement improvement

**Feedback Loop:**
Human edits on value messaging → KL-005 weekly batch retrain updates messaging patterns and persona profiles. Override rate >15% triggers AIG-002 prompt optimization. Monthly effectiveness audit by AIG-001 measuring message engagement against persona baselines. Source: MECLABS messaging research updates, Value Proposition Design methodology refresh.

---

## Agent CT-002: Proposal Generator

**Division:** Content Team
**Primary Function:** Assembles comprehensive, personalized proposals from modular components.
**Triggers:**
- deal_stage_reaches_proposal
- proposal_requested_by_buyer
- pricing_approved
- legal_terms_finalized
**Outputs:**
- ull_proposal_document - comprehensive proposal
- proposal_executive_summary - one-page version
- 	echnical_proposal_attachment
- pricing_schedule - breakdown with options
- proposal_engagement_tracking - who viewed what
**Data Sources:** Deal CRM data, pricing/quoting tool, value messaging library, case study library, legal terms database, proposal templates
**Training Corpus:** Proposal writing (Winning by Design, Shipley), APMP response standards, persuasive writing for enterprise sales, Command of the Message LinkedIn examples, Corporate Visions YouTube value messaging, HBR case study structure articles
**LLM Tier:** Complex Reasoning (Opus class) - proposal assembly requires complex document structuring
**Criticality:** P0 - proposals are the primary closing document
**Why dedicated:** Proposal generation is complex document assembly with version management, distinct from other content generation.
**Prompt Pattern:** Generation (structured document) + RAG (case study retrieval)

**Business Outcome:** Increase proposal win rate by 30% through personalized, evidence-rich proposals delivered within 24 hours of request; reduce proposal assembly time from days to <10 minutes by modular composition with intelligent content matching.

**Functions (Detailed):**
- assemble_proposal(deal_context, value_messaging, pricing) -> full_proposal_document
- generate_executive_summary(proposal, executive_priorities) -> one_page_summary
- incorporate_case_studies(proposal_draft, relevant_case_studies) -> evidence_enriched_proposal
- create_pricing_schedule(pricing_data, deal_terms) -> pricing_breakdown
- track_proposal_engagement(proposal_id, viewer_analytics) -> engagement_report

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Value messaging library (from CT-001)
- Proposal template repository
- Case study library (from CT-003)
- Pricing API (deal pricing and quoting)
- Legal terms database

**KPIs & Metrics:**
- proposal_win_rate: target >45%
- proposal_assembly_time: target <10min
- proposal_personalization_score: target >85%
- executive_summary_read_rate: target >80%

**Performance Score:**
- **Red (<70):** Win rate <30% or assembly time >30min — escalation to AIG-001 for quality audit
- **Amber (70-85):** Proposals delivered but win rate or personalization sub-optimal
- **Green (>85):** Fully autonomous — proposals <10min with >45% win rate

**Feedback Loop:**
Human edits on proposal content → KL-005 weekly batch retrain updates proposal structure and content selection. Override rate >20% triggers AIG-002 prompt optimization. Monthly win/loss analysis by AIG-001 cross-referencing proposal quality against outcomes. Source: APMP response standard updates, Winning by Design methodology refresh.

---

## Agent CT-003: Case Study Adapter

**Division:** Content Team
**Primary Function:** Adapts existing customer success stories to match a specific prospect's context.
**Triggers:**
- prospect_needs_relevant_case_study
- social_proof_requested by Influence Applicator
- 
ew_customer_success_story_available
- objection_raised_that_case_study_could_address
**Outputs:**
- dapted_case_study - rewritten for prospect context
- case_study_summary - one-paragraph version
- case_study_quote_snippet - extracted testimonial
- case_study_relevance_score - match quality
- case_study_gap_alert - missing case studies for key segments
**Data Sources:** Case study library, prospect profile, CRM deal data, customer reference database, testimonial database
**Training Corpus:** Case study writing (Content Marketing Institute), B2B storytelling (Andy Raskin, Donald Miller), narrative transportation theory
**LLM Tier:** Moderate (Sonnet class) - case study adaptation is structured rewrite
**Criticality:** P1 - social proof is important but generic studies can substitute
**Why dedicated:** Case study adaptation requires RAG-intensive library search distinct from other content generation.
**Prompt Pattern:** RAG (case study retrieval) + Generation (context-adapted rewrite)

**Business Outcome:** Increase case study engagement relevance by 40% by delivering prospect-contextualized success stories; reduce case study adaptation time from hours to <30 seconds, enabling personalized social proof at every deal stage.

**Functions (Detailed):**
- retrieve_relevant_case_studies(prospect_profile, deal_context) -> ranked_case_studies
- adapt_case_study(case_study, prospect_context) -> personalized_version
- extract_testimonial_snippet(case_study, relevance_points) -> quote_snippet
- score_case_study_relevance(prospect_data, case_study_tags) -> relevance_score
- detect_case_study_gaps(prospect_segment, library_coverage) -> content_gap_alert

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Case study library (tagged and indexed)
- Prospect profile store (from DC agents)
- CRM deal context
- Customer reference database

**KPIs & Metrics:**
- adaptation_generation_latency: target <30s
- case_study_relevance_score: target >85%
- prospect_engagement_with_adapted_study: target >60%
- library_coverage_gap_detection: target >90% of unserved segments

**Performance Score:**
- **Red (<70):** Relevance score <65% or latency >60s — escalation to AIG-001
- **Amber (70-85):** Adaptations delivered but relevance or engagement sub-optimal
- **Green (>85):** Fully autonomous — adaptations <30s with >85% relevance score

**Feedback Loop:**
Human edits on case study adaptations → KL-005 weekly batch retrain updates relevance scoring and adaptation patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing case study usage against deal progression. Source: Content Marketing Institute case study best practices, narrative transportation research updates.

---

## Agent CT-004: Battle Card Updater

**Division:** Content Team
**Primary Function:** Maintains a living library of competitive battle cards updated continuously from win/loss data and intelligence.
**Triggers:**
- competitive_win_analyzed
- competitive_loss_analyzed
- product_feature_released
- competitor_pricing_changed
- competitor_launched_new_feature
**Outputs:**
- attle_card - overview, positioning, strengths, weaknesses, rebuttals
- attle_card_update - incremental update
- attle_card_refresh_needed - older than 90 days
- competitor_tracking_report - weekly landscape changes
- winning_positioning_statement - proven positioning
**Data Sources:** Win/loss database, competitive intelligence feeds, product release notes, competitor website/pricing, analyst reports
**Training Corpus:** Competitive intelligence (Crayon, Klue), battle card development (SalesIntel, Gong), win/loss analysis
**LLM Tier:** Moderate (Sonnet class) - battle cards follow structured templates
**Criticality:** P1 - important for competitive deals
**Why dedicated:** Battle card maintenance requires continuous monitoring, a different pattern from per-deal content generation.
**Prompt Pattern:** Extraction (competitive intelligence) + Generation (battle card content)

**Business Outcome:** Increase competitive deal win rate by 30% by maintaining continuously updated battle cards; reduce competitive intelligence staleness to <7 days through automated monitoring and real-time battle card updates.

**Functions (Detailed):**
- extract_competitive_intel(win_loss_reports, web_data, analyst_notes) -> intelligence_brief
- generate_battle_card(competitor_profile, positioning_strategy) -> structured_battle_card
- update_battle_card(existing_card, new_intelligence) -> incremental_update
- detect_stale_cards(battle_card_library, freshness_threshold) -> refresh_alert
- produce_competitor_tracking_report(intel_feeds, period) -> landscape_report

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Win/loss database (from DS-003)
- Competitive intelligence feeds (web monitoring)
- Product release notes store
- Battle card library
- Analyst report repository

**KPIs & Metrics:**
- battle_card_freshness: target <7 days staleness
- competitive_deal_win_rate: target >55%
- intel_extraction_accuracy: target >90%
- battle_card_coverage: target >95% of known competitors

**Performance Score:**
- **Red (<70):** Card freshness >30 days or win rate <40% — escalation to AIG-001
- **Amber (70-85):** Cards updated but extraction accuracy or coverage sub-optimal
- **Green (>85):** Fully autonomous — cards refreshed <7 days with >90% accuracy

**Feedback Loop:**
Human corrections on battle card content → KL-005 weekly batch retrain updates competitive intelligence extraction patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing battle card usage rates against win rates. Source: Crayon/Klue intelligence feeds, competitor website monitoring, analyst report updates.

---

## Agent CT-005: Presentation Builder

**Division:** Content Team
**Primary Function:** Assembles personalized, stage-appropriate presentation decks from modular slides.
**Triggers:**
- meeting_scheduled_with_prospect
- demo_scheduled
- executive_briefing_scheduled
- presentation_template_updated
**Outputs:**
- presentation_deck - full deck with speaker notes
- presentation_outline - agenda and flow
- custom_slide - one-off slide
- presentation_script - speaker notes
- presentation_timing_estimate
**Data Sources:** Slide library, deal-specific content, stakeholder map, competitive battle cards, product screenshots, brand assets
**Training Corpus:** Presentation design (Garr Reynolds, Nancy Duarte), pitch deck structure (Andy Raskin), storytelling with data (Cole Nussbaumer Knaflic)
**LLM Tier:** Moderate (Sonnet class) - presentation assembly is modular composition
**Criticality:** P1 - important meetings need decks
**Why dedicated:** Presentation assembly requires slide library access and brand consistency rules distinct from document generation.
**Prompt Pattern:** Routing (template selection) + Generation (slide content and notes)

**Business Outcome:** Increase meeting win rate by 20% through personalized, stage-appropriate presentation decks; reduce presentation creation time by 70% by intelligently composing from a brand-compliant modular slide library.

**Functions (Detailed):**
- select_presentation_template(meeting_type, audience, deal_stage) -> slide_template
- generate_slide_content(template_section, deal_data, messaging) -> slide_with_notes
- assemble_presentation(selected_slides, ordering_rules) -> complete_deck
- add_speaker_notes(slide_content, speaker_preferences) -> presentation_script
- estimate_presentation_timing(slide_count, content_depth) -> timing_estimate

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Modular slide library (brand templates)
- Value messaging library (from CT-001)
- Stakeholder map (from DC-003)
- Competitive battle cards (from CT-004)
- Brand asset repository

**KPIs & Metrics:**
- presentation_build_latency: target <60s
- meeting_win_rate_with_deck: target >55%
- slide_reuse_efficiency: target >70% template usage
- brand_compliance_rate: target >99%

**Performance Score:**
- **Red (<70):** Build latency >120s or brand compliance <90% — escalation to AIG-001
- **Amber (70-85):** Decks delivered but personalization or timing sub-optimal
- **Green (>85):** Fully autonomous — decks built <60s with >99% brand compliance

**Feedback Loop:**
Human edits on presentation content → KL-005 weekly batch retrain updates slide content patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for brand compliance and effectiveness. Source: Presentation design methodology updates (Duarte, Reynolds), slide library expansions.

---

## Agent CT-006: Email Template Generator

**Division:** Content Team
**Primary Function:** Designs, maintains, and optimizes a library of email templates tested for engagement and conversion.
**Triggers:**
- 
ew_sequence_created by SDR
- engagement_drop_detected - templates underperforming
- _b_test_completed - winning template promoted
- 
ew_persona_defined
- 	emplate_fatigue_detected
**Outputs:**
- email_template - structured with subject, preview, body, CTA, variables
- 	emplate_variant - A/B variant
- 	emplate_performance_report - metrics per template
- 	emplate_optimization_recommendations
- 	emplate_saturation_alert - needs rotation
**Data Sources:** Email engagement database, sequence definitions, persona profiles, trigger taxonomy, A/B test results
**Training Corpus:** Copywriting frameworks (AIDA, PAS, BAB), cold email best practices (Close.com, Mailshake), email marketing optimization
**LLM Tier:** Moderate (Sonnet class) - template generation follows proven frameworks
**Criticality:** P1 - templates are important but SDRs can write one-off emails
**Why dedicated:** Email template management requires continuous optimization based on performance data.
**Prompt Pattern:** Generation (template with variables) + Analysis (performance)

**Business Outcome:** Increase email engagement rates by 25% through data-driven template optimization; reduce SDR template selection time by 60% by maintaining a performance-ranked library of proven, persona-specific email templates.

**Functions (Detailed):**
- generate_email_template(persona, sequence_stage, value_props) -> structured_template
- create_ab_variant(base_template, test_element) -> variant_template
- analyze_template_performance(engagement_data, template_id) -> performance_report
- detect_template_fatigue(performance_trend, threshold) -> rotation_alert
- optimize_template_metrics(underperforming_template, test_results) -> improved_template

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Email engagement database (open rates, click rates, replies)
- Sequence definition store (from SDR-X)
- Persona profile database
- A/B test results store

**KPIs & Metrics:**
- email_open_rate_improvement: target >25%
- click_through_rate: target >15% above baseline
- template_generation_latency: target <15s
- template_saturation_detection_accuracy: target >90%

**Performance Score:**
- **Red (<70):** Open rates below baseline or template fatigue undetected — escalation to AIG-001
- **Amber (70-85):** Templates generated but performance optimization sub-optimal
- **Green (>85):** Fully autonomous — templates generated <15s with >25% open rate improvement

**Feedback Loop:**
Human edits on template content → KL-005 weekly batch retrain updates template generation patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing template performance vs benchmarks. Source: Email marketing research updates, Close.com best practices, Mailshake methodology refresh.

---

## Tier 2 — Deal Acceleration

---

### Division 9: DEAL STRATEGY TEAM

These agents plan and optimize deal-specific strategies.

---

## Agent DS-001: Deal Planner

**Division:** Deal Strategy Team
**Primary Function:** Creates a comprehensive, step-by-step deal plan for each strategic opportunity.
**Triggers:**
- opportunity_created_with_value_above_threshold
- deal_stalled - creates recovery plan
- competitive_threat_detected
- 
ew_stakeholder_identified
- quarter_close_approaching
**Outputs:**
- deal_plan - milestones, stakeholder plan, competitive positioning, risk register, timeline
- deal_milestone_timeline - key dates and actions
- stakeholder_engagement_plan - who, when, what message
- isk_register_and_mitigation
**Data Sources:** CRM opportunity data, stakeholder map, competitive intelligence, discovery data, value engineering outputs, historical similar deals
**Training Corpus:** Strategic selling (Miller Heiman), complex deal planning (Salesforce, MEDDIC), military strategy (Sun Tzu, von Clausewitz), Anthony Iannarino blog deal strategy, SalesHacker deal planning articles, SaaStr deal management insights
**LLM Tier:** Complex Reasoning (Opus class) - deal planning requires multi-variable strategic reasoning
**Criticality:** P0 - strategic deals require structured plans
**Why dedicated:** Deal planning is a strategic synthesis task integrating inputs from all agents into a coherent plan.
**Prompt Pattern:** Analysis (situation assessment) + Generation (structured plan)

**Business Outcome:** Increase strategic deal win rate by 20% through comprehensive, structured deal planning; reduce deal cycle time by 25% by identifying critical milestones, stakeholders, and risks proactively before they become blockers.

**Functions (Detailed):**
- assess_deal_situation(opportunity_data, stakeholder_map, competitive_intel) -> situation_assessment
- generate_deal_milestone_plan(situation_assessment, deal_value, timeline) -> milestone_timeline
- build_stakeholder_engagement_plan(stakeholder_map, influence_levels, deal_phase) -> engagement_strategy
- identify_deal_risks(situation_assessment, historical_patterns, competitive_data) -> risk_register
- create_comprehensive_deal_plan(milestones, stakeholders, risks, positioning) -> integrated_plan

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- CRM opportunity data store
- Stakeholder map (from DC-003)
- Competitive intelligence (from CT-004)
- Discovery data (from DC-001)
- Value engineering outputs (from VE-001)
- Historical similar deals database

**KPIs & Metrics:**
- deal_plan_adoption_rate: target >85%
- strategic_deal_win_rate_impact: target >20% improvement
- risk_identification_precision: target >85%
- deal_cycle_time_reduction: target >25%
- milestone_adherence_rate: target >80%

**Performance Score:**
- **Red (<70):** Plan adoption <60% or win rate impact <10% — escalation to AIG-001
- **Amber (70-85):** Plans generated but milestone adherence or risk identification sub-optimal
- **Green (>85):** Fully autonomous — plans drive >20% win rate improvement with >85% adoption

**Feedback Loop:**
Human corrections on deal plans and milestone adjustments → KL-005 weekly batch retrain updates planning patterns and risk identification models. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing plan effectiveness against actual deal outcomes. Source: MEDDIC/MEDDPICC framework updates, Miller Heiman strategic selling methodology refresh, SalesHacker deal planning articles.

---

## Agent DS-002: Competitive Positioning Strategist

**Division:** Deal Strategy Team
**Primary Function:** Develops competitive positioning approach for each deal.
**Triggers:**
- competitor_identified_on_deal
- competitor_claim_made_in_meeting
- competitive_battle_card_updated
- competitive_loss_analyzed
- fp_competitor_list_received
**Outputs:**
- competitive_positioning_strategy - differentiate, neutralize, or cede
- strength_exploitation_plan
- weakness_mitigation_plan
- competitive_narrative - frames landscape favorably
- win_theme_development
**Data Sources:** Battle card library, win/loss database, competitor intelligence, deal-specific discovery data, analyst reports
**Training Corpus:** Competitive strategy (Michael Porter), Blue Ocean Strategy (Kim and Mauborgne), positioning (Trout and Ries), Sun Tzu
**LLM Tier:** Complex Reasoning (Opus class) - competitive strategy requires game theory reasoning
**Criticality:** P1 - critical for competitive deals
**Why dedicated:** Competitive positioning is strategic reasoning distinct from both deal planning and battle card maintenance.
**Prompt Pattern:** Analysis (competitive landscape) + Generation (positioning strategy)

**Business Outcome:** Improve competitive deal win rate by 15% through tailored, deal-specific positioning strategies; reduce competitive position erosion by 25% by proactively identifying and mitigating competitor strengths before they become deal factors.

**Functions (Detailed):**
- analyze_competitive_landscape(deal_context, competitor_list, battle_cards) -> landscape_assessment
- develop_positioning_strategy(landscape_analysis, our_strengths, buyer_needs) -> positioning_approach
- generate_competitive_narrative(positioning_strategy, buyer_stakeholders) -> persuasive_landscape_frame
- plan_strength_exploitation(our_advantages, buyer_priorities) -> exploitation_actions
- plan_weakness_mitigation(competitor_strengths, our_gaps, buyer_concerns) -> mitigation_tactics

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Battle card library (from CT-004)
- Win/loss database (from DS-003)
- Competitive intelligence feeds
- Deal-specific discovery data (from DC-001)
- Analyst report repository

**KPIs & Metrics:**
- competitive_deal_win_rate_impact: target >15% improvement
- positioning_strategy_adoption: target >80%
- competitive_erosion_reduction: target >25%
- narrative_acceptance_by_buyer: target >70% positive response

**Performance Score:**
- **Red (<70):** Competitive win rate declining or positioning adoption <55% — escalation to AIG-001
- **Amber (70-85):** Positioning strategies developed but adoption or effectiveness sub-optimal
- **Green (>85):** Fully autonomous — positioning contributes to >15% competitive win rate improvement with >80% adoption

**Feedback Loop:**
Human corrections on positioning strategies and narratives → KL-005 weekly batch retrain updates competitive analysis patterns and positioning frameworks. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing positioning strategies against competitive deal outcomes. Source: Michael Porter competitive strategy updates, Blue Ocean Shift methodology refresh, Trout and Ries positioning evolution.

---

## Agent DS-003: Win/Loss Analyst

**Division:** Deal Strategy Team
**Primary Function:** Analyzes every won and lost deal to extract actionable insights and patterns.
**Triggers:**
- deal_won - full win analysis
- deal_lost - full loss analysis
- 	ick_weekly - aggregated trend analysis
- pattern_detected_across_multiple_losses
**Outputs:**
- win_analysis - what worked, what to replicate
- loss_analysis - root cause, could we have saved it
- competitive_loss_report - deep competitor analysis
- win_loss_ratio_trend
- loss_pattern_alert - systemic issues
- win_factor_ranking - what correlates with wins
- ecommended_action_items
**Data Sources:** CRM closed won/lost data, meeting transcripts, email threads, competitive intelligence, qualification scores, pricing data
**Training Corpus:** Win/loss analysis methodologies (WinLoss.com, Clozd), root cause analysis, thematic analysis, Gong Labs win/loss research blog, SalesHacker win/loss articles, Klue win/loss analysis blog, Anthony Iannarino LinkedIn win/loss insights
**LLM Tier:** Complex Reasoning (Opus class) - win/loss requires root cause analysis across multiple data sources
**Criticality:** P0 - without analysis, organization repeats mistakes
**Why dedicated:** Win/loss analysis is a cross-deal pattern-recognition task requiring longitudinal data.
**Partial Data Support:** Operates with available data when CRM fields are incomplete; surfaces confidence intervals per insight and flags analyses based on thin data requiring human validation.
**Prompt Pattern:** Analysis (root cause) + Generation (recommendations) + Classification (loss reason)

**Business Outcome:** Improve win rate by 10% through systematic analysis of every won and lost deal; reduce repeat losses by 30% by detecting early warning patterns and recommending preemptive action across the deal cycle.

**Functions (Detailed):**
- analyze_win_reasons(deal_data, meeting_transcripts, win_context) -> win_factor_extraction
- analyze_loss_reasons(deal_data, competitive_intel, loss_context) -> root_cause_analysis
- classify_loss_reason(loss_analysis, taxonomy_framework) -> loss_category_label
- detect_loss_patterns(historical_analyses, recent_losses) -> systemic_issue_alert
- rank_win_factors(aggregated_win_data, outcome_correlations) -> win_factor_priority_list
- generate_action_recommendations(pattern_analysis, org_process) -> recommended_changes

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- CRM closed won/lost data store
- Meeting transcript repository
- Email thread store
- Competitive intelligence (from CT-004)
- Qualification scores (from DC-004)

**KPIs & Metrics:**
- loss_classification_accuracy: target >90%
- win_rate_improvement_attribution: target >10%
- repeat_loss_reduction: target >30%
- action_recommendation_adoption: target >75%

**Performance Score:**
- **Red (<70):** Classification accuracy <75% or win rate declining despite recommendations — escalation to AIG-001
- **Amber (70-85):** Analyses generated but action adoption or repeat loss reduction sub-optimal
- **Green (>85):** Fully autonomous — losses classified with >90% accuracy and >10% win rate improvement

**Feedback Loop:**
Human corrections on loss reason classification and action recommendations → KL-005 weekly batch retrain updates root cause analysis patterns and classification taxonomy. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing win/loss trends against implemented recommendations. Source: Clozd win/loss methodology updates, Gong Labs research blog, Klue win/loss analysis refresh.

---

## Agent DS-004: Price Optimizer

**Division:** Deal Strategy Team
**Primary Function:** Recommends optimal pricing based on buyer segment, competitive landscape, and historical win rates.
**Triggers:**
- pricing_discussion_upcoming
- proposal_in_progress
- discount_requested
- competitive_pricing_pressure
- enewal_or_expansion
**Outputs:**
- ecommended_price - with rationale
- price_discussion_guide - how to present pricing
- discount_impact_analysis - revenue impact
- alue_based_pricing_justification
- price_sensitivity_profile
**Data Sources:** Pricing database, historical win rates by price point, competitive pricing, deal value, discount approval matrix
**Training Corpus:** Value-based pricing (Donovan, Hinterhuber), pricing strategy (Tom Nagle), price sensitivity measurement (Van Westendorp), Tim Williams LinkedIn value pricing, SaaStr pricing articles, ProfitWell blog pricing research
**LLM Tier:** Complex Reasoning (Opus class) - pricing requires balancing competing objectives
**Criticality:** P0 - pricing directly impacts revenue and margin
**Why dedicated:** Pricing optimization requires quantitative analysis distinct from strategic planning or content generation.
**Prompt Pattern:** Analysis (price sensitivity) + Generation (pricing discussion guide)

**Business Outcome:** Improve price realization by 5% through value-based pricing recommendations tailored to buyer segment and competitive context; reduce discount depth by 10% by providing data-driven discount impact analysis and alternative concession paths.

**Functions (Detailed):**
- analyze_price_sensitivity(deal_context, buyer_segment, competitive_data) -> sensitivity_profile
- recommend_optimal_price(sensitivity_profile, historical_win_rates, margin_targets) -> price_with_rationale
- generate_pricing_discussion_guide(price_recommendation, stakeholder_context) -> presentation_script
- calculate_discount_impact(proposed_discount, deal_value, margin_model) -> revenue_impact_report
- build_value_based_justification(deal_value_proposition, price, roi_data) -> justification_document

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Pricing database
- Historical win rates by price point store
- Competitive pricing feed
- Discount approval matrix
- Deal value database (from VE-001)
- Margin model (from DS-005)

**KPIs & Metrics:**
- price_realization_rate: target >95% (price achieved vs list)
- discount_depth_reduction: target >10%
- pricing_recommendation_acceptance: target >80%
- discount_impact_accuracy: target >90%

**Performance Score:**
- **Red (<70):** Price realization <85% or discount depth increasing — escalation to AIG-001
- **Amber (70-85):** Prices optimized but recommendation acceptance or discount impact accuracy sub-optimal
- **Green (>85):** Fully autonomous — price realization >95% with >10% discount depth reduction

**Feedback Loop:**
Human corrections on pricing recommendations and discount impact analyses → KL-005 weekly batch retrain updates pricing models and sensitivity patterns. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing recommended prices against actual deal prices. Source: ProfitWell pricing research updates, SaaStr pricing articles, value-based pricing methodology refresh.

---

## Agent DS-005: Discount Authority Agent

**Division:** Deal Strategy Team
**Primary Function:** Enforces discount authority policies and recommends structured concession paths.
**Triggers:**
- discount_requested_by_rep
- ep_requests_exception_to_policy
- deal_close_threatened_by_price
- quarter_end_approaching
- discount_pattern_flagged
**Outputs:**
- discount_approval_decision - approved, denied, modified
- discount_concession_path - structured discounting
- 
on_price_concession_suggestions - alternatives
- discount_authority_violation_alert
- deal_value_protection_recommendation
**Data Sources:** Discount authority matrix, rep role/level, deal value, margin data, competitive context, historical discount patterns
**Training Corpus:** Revenue recognition, discount authority frameworks, deal desk operations, concession sequencing
**LLM Tier:** Moderate (Sonnet class) - primarily rule-based with policy evaluation
**Criticality:** P1 - important for margin management
**Why dedicated:** Discount authority is a compliance function requiring separation from pricing optimization.
**Prompt Pattern:** Classification (within/outside authority) + Routing (approval flow)

**Business Outcome:** Reduce discount leakage by 15% through systematic enforcement of discount authority policies; decrease deal approval cycle time by 40% via automated classification and routing of discount requests.

**Functions (Detailed):**
- classify_discount_authority(request_details, authority_matrix, rep_role) -> approval_level
- route_discount_request(authority_level, deal_value, exception_type) -> approval_workflow
- recommend_concession_path(discount_request, margin_data, competitive_context) -> structured_path
- suggest_non_price_concessions(requested_discount, concession_library) -> alternative_list
- detect_discount_patterns(historical_requests, current_trends) -> violation_or_anomaly_alert

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Sonnet class)
- Discount authority matrix store
- Deal value and margin database
- Competitive context (from CT-004)
- Historical discount pattern store
- Concession library

**KPIs & Metrics:**
- discount_classification_accuracy: target >95%
- discount_leakage_reduction: target >15%
- approval_cycle_time_reduction: target >40%
- non_price_concession_adoption_rate: target >30%

**Performance Score:**
- **Red (<70):** Classification accuracy <80% or no measurable leakage reduction — escalation to AIG-001
- **Amber (70-85):** Discount requests classified but routing efficiency or non-price concession adoption sub-optimal
- **Green (>85):** Fully autonomous — discounts classified with >95% accuracy and >15% leakage reduction

**Feedback Loop:**
Human overrides on discount decisions → KL-005 weekly batch retrain updates authority classification and routing patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing discount approval patterns against margin targets. Source: Revenue recognition standards updates, deal desk ops best practices, discount authority policy changes.

---


### Division 10: NEGOTIATION TEAM

These agents prepare and support negotiations with analysis, strategy, and tactical recommendations.

---

## Agent NG-001: BATNA Analyst

**Division:** Negotiation Team
**Primary Function:** Analyzes our BATNA and estimates the buyer's BATNA for each negotiation.
**Triggers:**
- 
egotiation_stage_reached
- uyer_alternative_identified - evaluating competitor
- our_pipeline_changes - our alternatives change
- market_condition_change
**Outputs:**
- our_batna_assessment - best alternative with quantified value
- uyer_batna_estimate - with confidence level
- leverage_ratio - who has stronger alternatives
- eservation_price - walk-away point
- 
egotiation_power_timeline - leverage shifts over time
**Data Sources:** Pipeline data, competitive intelligence, market data, buyer financial health, timeline data, internal capacity
**Training Corpus:** Getting to Yes (Fisher, Ury, Patton), Harvard Negotiation Project, bargaining power analysis (Schelling, Mnookin), Chris Voss YouTube BATNA examples, Never Split the Difference podcast interviews, HNP blog negotiation cases
**LLM Tier:** Complex Reasoning (Opus class) - BATNA requires game theory reasoning
**Criticality:** P0 - negotiation without BATNA knowledge is blind
**Why dedicated:** BATNA is a game-theoretic reasoning task fundamentally different from document-focused work.
**Prompt Pattern:** Analysis (alternative evaluation) + Generation (BATNA strategy)

**Business Outcome:** Increase negotiation success rate by 15% through accurate BATNA analysis; improve deal terms by 20% by establishing informed walk-away points and leverage-based negotiation strategies.

**Functions (Detailed):**
- evaluate_our_batna(pipeline_alternatives, resource_capacity) -> batna_quantified_value
- estimate_buyer_batna(competitive_intel, buyer_context) -> buyer_batna_with_confidence
- calculate_leverage_ratio(our_batna, buyer_batna, market_conditions) -> leverage_metric
- determine_reservation_price(batna_values, deal_financials) -> walk_away_point
- project_leverage_timeline(current_factors, expected_changes) -> power_shift_timeline

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Pipeline data store
- Competitive intelligence (from CT-004)
- Market data feed
- Buyer financial data (from DC-006)
- Internal capacity database

**KPIs & Metrics:**
- batna_accuracy_vs_outcomes: target >85% correlation
- negotiation_success_rate_impact: target >15% improvement
- reservation_price_adherence: target >90%
- leverage_ratio_prediction_accuracy: target >80%

**Performance Score:**
- **Red (<70):** BATNA accuracy <65% or negotiation success impact <5% — escalation to AIG-001
- **Amber (70-85):** BATNA analyzed but accuracy or reservation price adherence sub-optimal
- **Green (>85):** Fully autonomous — BATNA analysis with >85% accuracy and >15% negotiation success improvement

**Feedback Loop:**
Human corrections on BATNA assessments and reservation prices → KL-005 weekly batch retrain updates alternative evaluation patterns. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing BATNA estimates against actual negotiation outcomes. Source: HNP negotiation research updates, Chris Voss methodology refresh, Harvard Negotiation Project case studies.

---

## Agent NG-002: Concession Planner

**Division:** Negotiation Team
**Primary Function:** Designs a structured concession sequence maximizing perceived value while minimizing cost.
**Triggers:**
- 
egotiation_stage_reached
- uyer_made_demand
- concession_made
- 
egotiation_stalled
- uyer_concession_received
**Outputs:**
- concession_plan - sequenced list with triggers
- concession_framing - how to present each concession
- concession_value_calculation - cost vs perceived value
- 	rade_off_matrix - low-cost/high-value concessions
- concession_pattern_alert - giving too much too fast
- walk_away_trigger - conditions to walk away
**Data Sources:** BATNA analysis, deal financial data, buyer behavior signals, negotiation history, concession effectiveness database
**Training Corpus:** Negotiation theory (Raiffa, Malhotra, Bazerman), Getting Past No (Ury), 3D Negotiation (Lax and Sebenius), Chris Voss YouTube negotiation tactics, The Black Swan Group blog concession strategies, HBR negotiation articles
**LLM Tier:** Complex Reasoning (Opus class) - concession planning requires strategic sequencing
**Criticality:** P1 - important for complex negotiations
**Why dedicated:** Concession planning maintains a dynamic state machine across the negotiation.
**Prompt Pattern:** Analysis (concession value) + Generation (sequenced plan)

**Business Outcome:** Preserve 8% additional margin per deal through structured, value-based concession sequencing; increase perceived buyer value by 25% by framing concessions as high-value while minimizing actual cost.

**Functions (Detailed):**
- design_concession_sequence(negotiation_context, batna_data) -> sequenced_concession_plan
- calculate_concession_value(concession_item, cost_model) -> actual_vs_perceived_value
- generate_concession_framing(concession_item, buyer_priorities) -> presentation_script
- build_trade_off_matrix(available_concessions, deal_margin) -> low_cost_high_value_map
- detect_concession_patterns(concession_history, recent_actions) -> giving_too_fast_alert

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- BATNA analysis store (from NG-001)
- Deal financial database
- Concession effectiveness database
- Negotiation history store

**KPIs & Metrics:**
- concession_margin_preservation: target >8%
- perceived_value_multiplier: target >1.5x (perceived vs actual cost)
- concession_sequence_acceptance_rate: target >75%
- premature_concession_alerts: target <10% false positive

**Performance Score:**
- **Red (<70):** Margin preservation <3% or concession acceptance rate <55% — escalation to AIG-001
- **Amber (70-85):** Concessions sequenced but framing or trade-off optimization sub-optimal
- **Green (>85):** Fully autonomous — concessions preserve >8% margin with >1.5x perceived value multiplier

**Feedback Loop:**
Human corrections on concession plans and framing language → KL-005 weekly batch retrain updates concession sequencing and value calculation models. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing concession costs against deal margins. Source: Black Swan Group concession strategy updates, HBR negotiation research, Chris Voss methodology refresh.

---

## Agent NG-003: Procurement Defense Agent

**Division:** Negotiation Team
**Primary Function:** Anticipates procurement tactics, identifies common plays, and prepares counter-strategies.
**Triggers:**
- procurement_department_involved
- procurement_tactic_detected
- uyer_requests_standard_terms
- procurement_delays_tactic
- procurement_reopens_closed_items
**Outputs:**
- procurement_tactic_alert - which tactic with evidence
- 	actic_counter_strategy - specific response
- procurement_stall_counter - maintain momentum
- procurement_nibble_defense - handle reopened terms
- procurement_escalation_path - when to go around procurement
**Data Sources:** Meeting transcripts, email threads, procurement playbook library, negotiation history, contract terms database
**Training Corpus:** Enterprise procurement tactics (Gartner, Forrester), procurement defense (K and R Negotiation), purchasing psychology, ISM standards, Strategic Procurement blog procurement defense, Coupa blog procurement trends, Jonathan Hughes LinkedIn procurement insights
**LLM Tier:** Complex Reasoning (Opus class) - procurement defense requires recognizing sophisticated tactics
**Criticality:** P0 - most enterprise deals go through procurement
**Why dedicated:** Procurement defense requires specialized knowledge distinct from general negotiation strategy.
**Prompt Pattern:** Classification (tactic identification) + RAG (counter-strategy) + Generation (response)

**Business Outcome:** Reduce procurement-driven discount by 10% through proactive tactic identification and counter-strategy deployment; shorten procurement phase by 30% by preempting stall tactics and maintaining deal momentum.

**Functions (Detailed):**
- classify_procurement_tactic(buyer_behavior, communication_patterns) -> tactic_label
- retrieve_counter_strategy(tactic_type, deal_context) -> prebuilt_counter
- generate_tactic_response(counter_strategy, negotiation_state) -> response_script
- detect_procurement_stalls(deal_timeline, communication_gaps) -> stall_alert
- recommend_escalation_path(stall_severity, buyer_org_structure) -> escalation_plan

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Procurement playbook library
- Meeting transcript store
- Email thread store
- Contract terms database

**KPIs & Metrics:**
- tactic_classification_accuracy: target >92%
- procurement_phase_duration_reduction: target >30%
- discount_saved_via_defense: target >10%
- escalation_path_success_rate: target >85%

**Performance Score:**
- **Red (<70):** Tactic classification <75% or no measurable discount preservation — escalation to AIG-001
- **Amber (70-85):** Tactics identified but counter-strategies or responses sub-optimal
- **Green (>85):** Fully autonomous — tactics classified with >92% accuracy and >30% procurement phase reduction

**Feedback Loop:**
Human corrections on tactic identification and counter-strategy effectiveness → KL-005 weekly batch retrain updates procurement defense patterns and playbook. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing defense outcomes against procurement losses. Source: Gartner procurement research updates, ISM standards refresh, Coupa blog procurement trends.

---

## Agent NG-004: Terms Optimizer

**Division:** Negotiation Team
**Primary Function:** Analyzes contract terms for business impact and recommends modifications.
**Triggers:**
- contract_draft_received_from_buyer
- proposed_contract_generated
- legal_review_completed
- payment_terms_proposed
- enewal_terms_discussed
**Outputs:**
- 	erm_impact_analysis - business impact per term
- 	erm_optimization_recommendations
- payment_terms_optimization
- enewal_term_recommendations
- liability_exposure_analysis
- market_standard_comparison
**Data Sources:** Contract draft, standard terms database, market standard terms, buyer financial data, legal review comments
**Training Corpus:** Contract analysis, commercial contract terms (SaaS, services), IACCM standards, revenue recognition (ASC 606)
**LLM Tier:** Complex Reasoning (Opus class) - contract analysis requires legal, financial, and operational reasoning
**Criticality:** P1 - important but legal can review manually
**Why dedicated:** Terms optimization requires simultaneous legal, financial, and business reasoning distinct from drafting.
**Prompt Pattern:** Analysis (term-by-term impact) + Generation (optimization recommendations)

**Business Outcome:** Reduce contract liability exposure by 25% through systematic term impact analysis; increase favorable term adoption by 15% by benchmarking against market standards and recommending optimized alternatives.

**Functions (Detailed):**
- analyze_term_impact(contract_draft, deal_financials) -> impact_per_term_assessment
- recommend_term_optimizations(impact_analysis, acceptable_ranges) -> optimization_suggestions
- benchmark_against_market(contract_terms, market_standards) -> comparison_report
- optimize_payment_terms(proposed_terms, buyer_profile) -> payment_recommendation
- analyze_renewal_terms(renewal_proposal, historical_data) -> renewal_recommendation

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Standard terms database
- Market terms benchmark store
- Buyer financial data (from DS-004)
- Legal policy repository

**KPIs & Metrics:**
- term_impact_analysis_accuracy: target >90%
- favorable_term_adoption_rate: target >70%
- liability_exposure_reduction: target >25%
- market_benchmarking_coverage: target >95% of terms

**Performance Score:**
- **Red (<70):** Analysis accuracy <75% or no measurable liability reduction — escalation to AIG-001
- **Amber (70-85):** Terms analyzed but optimization recommendations or benchmarking sub-optimal
- **Green (>85):** Fully autonomous — terms analyzed with >90% accuracy and >25% liability reduction

**Feedback Loop:**
Human corrections on term impact assessments and optimization recommendations → KL-005 weekly batch retrain updates term analysis patterns. Override rate >15% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing recommended vs accepted term modifications. Source: IACCM standards updates, market term benchmarks refresh, ASC 606 compliance changes.

---

## Agent NG-005: Leverage Identifier

**Division:** Negotiation Team
**Primary Function:** Continuously identifies sources of leverage throughout the negotiation.
**Triggers:**
- 
egotiation_stage_reached
- meeting_highlights_leverage_point
- uyer_reveals_constraint
- competitive_situation_changes
- uyer_investment_increases
**Outputs:**
- leverage_inventory - all sources with strength rating
- leverage_application_recommendations
- leverage_timeline - changes over deal cycle
- leverage_loss_warning - diminishing source
- symmetric_leverage_opportunity
**Data Sources:** Meeting transcripts, email threads, competitive intelligence, deal timeline, buyer company news, relationship health scores
**Training Corpus:** Negotiation leverage (Lax and Sebenius), power in negotiation (Kim, Pinkley, Fragale), information asymmetry
**LLM Tier:** Complex Reasoning (Opus class) - leverage identification requires multi-dimensional analysis
**Criticality:** P1 - leverage awareness significantly improves outcomes
**Why dedicated:** Leverage identification requires continuous monitoring of shifting dynamics.
**Prompt Pattern:** Analysis (leverage source identification) + Generation (application strategy)

**Business Outcome:** Increase average deal value by 12% through systematic leverage identification and application; improve concession efficiency by ensuring every concession is matched with a reciprocal gain from the buyer.

**Functions (Detailed):**
- identify_leverage_sources(deal_context, meeting_data, signals) -> leverage_inventory
- score_leverage_strength(leverage_source, deal_phase, buyer_context) -> strength_rating
- recommend_leverage_application(leverage_item, negotiation_state) -> application_action
- track_leverage_changes(leverage_inventory, new_signals) -> timeline_update
- detect_leverage_opportunities(buyer_signals, competitive_data) -> asymmetric_opportunity

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Meeting transcript store
- Competitive intelligence (from CT-004)
- Buyer news monitoring feed
- Relationship health database (from RI-001)

**KPIs & Metrics:**
- leverage_identification_recall: target >90%
- leverage_application_win_rate_impact: target >10% improvement
- leverage_timeline_accuracy: target >85%
- asymmetric_opportunity_detection_precision: target >80%

**Performance Score:**
- **Red (<70):** Leverage recall <70% or no measurable win-rate impact — escalation to AIG-001
- **Amber (70-85):** Leverage identified but application recommendations or timing sub-optimal
- **Green (>85):** Fully autonomous — leverage identified with >90% recall and measurable 10%+ win-rate improvement

**Feedback Loop:**
Human corrections on leverage assessments and application recommendations → KL-005 weekly batch retrain updates leverage identification patterns. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing leverage usage rates against deal outcomes. Source: Negotiation research updates, Black Swan Group methodology refresh, HBR negotiation articles.

---

## Agent NG-006: Contract Redlining Agent

**Division:** Negotiation Team
**Primary Function:** Reviews buyer contract redlines, classifies changes, and generates counter-redlines.
**Triggers:**
- contract_redlines_received_from_buyer
- standard_terms_updated
- legal_team_feedback_received
- edline_discrepancy_detected
**Outputs:**
- edline_classification_report - accept/counter/reject with rationale
- counter_redline_draft
- contentious_term_alert - likely sticking points
- edline_negotiation_strategy
- inconsistency_detection - contradicts prior agreements
**Data Sources:** Redlined contract, standard terms library, acceptable terms playbook, legal policy documents, negotiation notes
**Training Corpus:** Contract review best practices, SaaS MSA standards (IACCM), legal redlining conventions
**LLM Tier:** Complex Reasoning (Opus class) - redlining requires understanding legal implications and business trade-offs
**Criticality:** P1 - accelerates legal review but human review remains essential
**Why dedicated:** Contract redlining is document-comparison with specialized legal domain model.
**Prompt Pattern:** Classification (redline type) + Generation (counter-redline) + Analysis (business impact)

**Business Outcome:** Reduce contract negotiation cycle time by 50% through automated redline classification and counter-draft generation; increase favorable term rate by 20% by ensuring every redline is addressed with pre-approved, market-standard counter-language.

**Functions (Detailed):**
- classify_redlines(redlined_contract, standard_terms) -> classification_report
- generate_counter_redline(redline_item, acceptable_terms) -> counter_draft
- analyze_term_impact(redline_proposal, deal_financials) -> business_impact_assessment
- identify_contentious_terms(redline_patterns, negotiation_history) -> stuck_point_alert
- detect_redline_inconsistencies(redlines, prior_agreements) -> inconsistency_warning

**Tools/APIs:**
- NATS JetStream (pub/sub for trigger/output events)
- LLM inference API (Opus class)
- Standard terms library
- Acceptable terms playbook
- Legal policy database
- Negotiation history store

**KPIs & Metrics:**
- redline_classification_accuracy: target >95%
- counter_redline_acceptance_rate: target >70%
- contract_cycle_time_reduction: target >45%
- inconsistency_detection_recall: target >90%

**Performance Score:**
- **Red (<70):** Classification accuracy <80% or cycle reduction <25% — escalation to AIG-001
- **Amber (70-85):** Redlines processed but acceptance rate or inconsistency detection sub-optimal
- **Green (>85):** Fully autonomous — redlines classified with >95% accuracy and >45% cycle reduction

**Feedback Loop:**
Human corrections on redline classification → KL-005 weekly batch retrain updates classification patterns and counter-draft templates. Override rate >20% triggers AIG-002 prompt optimization. Monthly audit by AIG-001 comparing acceptance rates and cycle times. Source: IACCM standard updates, legal policy revisions, market standard term benchmarks.

---

### Division 11: RELATIONSHIP INTELLIGENCE

These agents monitor, measure, and manage relationships across the revenue lifecycle.

---

## Agent RI-001: Stakeholder Mapper (Relationship)

**Division:** Relationship Intelligence
**Primary Function:** Maintains a living map of all relationships across an account.
**Triggers:**
- 
ew_contact_created
- email_exchange_completed
- meeting_completed
- introduction_made
- contact_role_changed
**Outputs:**
- elationship_map - graph of contacts and connections
- connection_heatmap - strongest/weakest relationships
- 
etwork_gap_analysis - missing connections
- elationship_strength_trend
- introduction_opportunity - suggested bridge
- elationship_at_risk_alert
- coverage_multiplicity_warning - single point of failure
**Data Sources:** CRM contact records, email metadata, meeting participation, LinkedIn connections, calendar events
**Training Corpus:** Relationship mapping (RE Forbes), account-based relationship management, social network analysis
**LLM Tier:** Moderate (Sonnet class) - primarily graph maintenance with classification
**Criticality:** P0 - without it, accounts are vulnerable to contact turnover
**Why dedicated:** Relationship mapping requires maintaining a graph data structure.
**Prompt Pattern:** Classification (relationship strength) + Analysis (network gaps)

**Business Outcome:** Reduce account vulnerability to churn from stakeholder turnover — maintain >2 relationship touchpoints per stakeholder in Tier-1 accounts and surface coverage gaps before they impact renewals.

**Functions (Detailed):**
- map_stakeholders(contacts, interactions) -> relationship_graph
- analyze_coverage(relationship_graph) -> coverage_heatmap
- detect_gaps(relationship_graph) -> network_gap_report
- alert_risk(relationship_at_risk) -> stakeholder_risk_alert
- suggest_introduction(missing_connection) -> introduction_opportunity

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- CRM API (contacts, accounts, opportunities)
- Email API (metadata extraction)
- Sentiment store (per-interaction scoring)
- Relationship graph DB (Neo4j-compatible)
- LinkedIn API (profile and connection data)

**KPIs & Metrics:**
- coverage_multiplicity_per_account: target >2.5
- stakeholder_map_accuracy: target >90%
- gap_identification_precision: target >85%
- alert_timely_detection_rate: target >95%

**Performance Score:**
- **Red (<70):** coverage_multiplicity <1.5 or accuracy <70% — escalate to RI lead
- **Amber (70-85):** coverage 1.5–2.5 or accuracy 70–85% — acceptable with manual review
- **Green (>85):** coverage >2.5 and accuracy >85% — fully autonomous

**Feedback Loop:**
Human corrections (missed connections, wrong strength ratings) logged via correction events → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate on strength ratings triggers AIG-002 prompt optimization. Monthly accuracy drift audit by AIG-001.

---

## Agent RI-002: Relationship Health Scorer

**Division:** Relationship Intelligence
**Primary Function:** Continuously scores relationship health based on communication, sentiment, responsiveness, and value indicators.
**Triggers:**
- 	ick_daily - recalculates scores
- email_exchange_completed
- meeting_completed
- support_ticket_filed
- long_silence_detected
**Outputs:**
- elationship_health_score - 1-100 with components
- health_score_trend - direction with velocity
- elationship_degradation_alert
- elationship_intervention_suggestion
- portfolio_health_summary
**Data Sources:** Email frequency and response time, meeting frequency and sentiment, support tickets, NPS/CSAT, communication gaps
**Training Corpus:** Customer health scoring (Gainsight, Totango), customer success metrics, relationship science, service-profit chain
**LLM Tier:** Moderate (Sonnet class) - health scoring requires multi-factor synthesis
**Criticality:** P1 - important but manual checks are possible
**Why dedicated:** Health scoring is continuous monitoring with different cadence than relationship mapping.
**Prompt Pattern:** Scoring (multi-factor computation) + Classification (risk level) + Generation (intervention)

**Business Outcome:** Reduce revenue at risk from degrading customer relationships — detect health deterioration 30+ days before churn and trigger automated intervention workflows.

**Functions (Detailed):**
- score_health(communication_freq, sentiment, responsiveness) -> health_score_1_100
- compute_trend(scores_over_time) -> health_trend_vector
- detect_degradation(score_delta, threshold) -> degradation_alert
- suggest_intervention(degradation_factors) -> intervention_plan
- summarize_portfolio(all_scores, segment) -> portfolio_health_summary

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Email API (frequency, response time metrics)
- Meeting platform API (attendance, duration)
- Sentiment store
- Support ticket API (volume, severity per account)
- CRM API (account metadata)

**KPIs & Metrics:**
- health_score_prediction_accuracy_vs_renewal: target >85%
- degradation_detection_lead_time: target >30 days pre-churn
- false_positive_rate: target <10%
- portfolio_coverage_percentage: target >95% of active accounts

**Performance Score:**
- **Red (<70):** prediction accuracy <70% or lead time <14 days — escalate to CS director
- **Amber (70-85):** accuracy 70–85% or lead time 14–30 days — semi-autonomous with CSM review
- **Green (>85):** accuracy >85% and lead time >30 days — fully autonomous scoring

**Feedback Loop:**
Human corrections (score overrides, missed degradation) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% score correction rate triggers AIG-002 prompt optimization. Monthly audit by AIG-001 for score drift.

---

## Agent RI-003: Communication Pattern Analyst

**Division:** Relationship Intelligence
**Primary Function:** Analyzes communication patterns to optimize engagement strategies.
**Triggers:**
- communication_data_accumulated
- 
ew_contact_added
- esponse_time_changes_significantly
- channel_preference_shift
- communication_gap_detected
**Outputs:**
- communication_pattern_profile - channels, timing, cadence
- channel_effectiveness_score - best channels per contact
- esponse_time_analysis - average, trend, anomalies
- optimal_send_time_recommendation
- pattern_shift_alert - disengagement signal
- nomaly_detection - unusual patterns
**Data Sources:** Email metadata, meeting patterns, channel engagement data, calendar, timezone data
**Training Corpus:** Communication optimization research, sales cadence science (SalesLoft, Outreach), email timing studies
**LLM Tier:** Simple (Haiku class) - primarily pattern computation with detection rules
**Criticality:** P2 - improves efficiency but not critical
**Why dedicated:** Communication pattern analysis is pattern-recognition over metadata volumes distinct from relationship scoring.
**Prompt Pattern:** Classification (pattern type) + Analysis (trend computation)

**Business Outcome:** Increase sales team efficiency by optimizing engagement timing and channel mix — improve response rates by 15%+ through data-driven communication pattern adaptation.

**Functions (Detailed):**
- profile_pattern(contact_id, communication_data) -> pattern_profile
- score_channel_effectiveness(channel_metrics) -> channel_effectiveness_score
- analyze_response_times(email_metadata) -> response_time_analysis
- recommend_send_time(contact_timezone, history) -> optimal_send_time
- detect_anomaly(patterns, baseline) -> pattern_shift_alert

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Haiku-class)
- Email API (metadata, response times)
- Meeting platform API (patterns, duration)
- Calendar API (timezone, availability)
- Sentiment store
- CRM API (contact timezone, preferences)

**KPIs & Metrics:**
- response_rate_improvement: target >15% lift
- pattern_classification_accuracy: target >90%
- optimal_time_recommendation_precision: target >85%
- anomaly_detection_false_positive_rate: target <5%

**Performance Score:**
- **Red (<70):** response rate improvement <5% or accuracy <70% — escalate to RI lead
- **Amber (70-85):** improvement 5–15% or accuracy 70–85% — manual review of recommendations
- **Green (>85):** improvement >15% and accuracy >85% — fully autonomous pattern analysis

**Feedback Loop:**
Human corrections (wrong pattern classification, suboptimal recommendations) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent RI-004: Churn Predictor

**Division:** Relationship Intelligence
**Primary Function:** Predicts customer churn risk by integrating multiple signal types.
**Triggers:**
- 	ick_weekly - recalculates churn risk
- usage_drop_detected
- support_escalation
- contract_renewal_approaching
- executive_departure_at_account
- sentiment_negative_trend
**Outputs:**
- churn_risk_score - 0-100 with confidence interval
- churn_risk_factors - ranked contributing factors
- churn_prediction_timeline
- t_risk_account_list
- etention_intervention_suggestions
- saved_account_value - projected retained revenue
**Data Sources:** Product usage analytics, support tickets, relationship health scores, NPS/CSAT, contract renewals, competitive intelligence
**Training Corpus:** Customer churn prediction, survival analysis, customer success best practices (Gainsight, Nick Mehta)
**LLM Tier:** Complex Reasoning (Opus class) - churn prediction requires integrating multiple signal types
**Criticality:** P0 - losing accounts without warning is critical revenue leak
**Why dedicated:** Churn prediction is predictive modeling with continuous risk monitoring distinct from relationship scoring.
**Prompt Pattern:** Analysis (multi-factor risk integration) + Scoring (churn probability) + Generation (intervention plan)

**Business Outcome:** Prevent revenue loss from preventable churn — identify 80%+ of at-risk accounts at least 60 days before renewal with ranked intervention recommendations.

**Functions (Detailed):**
- predict_churn(usage, support, sentiment, relationship) -> churn_risk_score_0_100
- rank_factors(churn_score, signal_sources) -> ranked_churn_factors
- estimate_timeline(churn_risk_trend) -> churn_prediction_timeline
- suggest_retention(churn_factors, account_profile) -> retention_intervention_suggestions
- flag_at_risk(all_scores, threshold) -> at_risk_account_list
- project_value(at_risk_accounts, win_rate) -> saved_account_value

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- Product usage analytics API
- Support ticket API
- Relationship health score store
- NPS/CSAT survey API
- CRM API (contract renewals)
- Competitive intelligence feed

**KPIs & Metrics:**
- churn_prediction_precision: target >85%
- early_detection_window: target >60 days before renewal
- intervention_conversion_rate: target >30%
- false_positive_rate: target <15%

**Performance Score:**
- **Red (<70):** precision <70% or early detection <30 days — escalate to CS VP
- **Amber (70-85):** precision 70–85% or detection 30–60 days — semi-autonomous with CSM action
- **Green (>85):** precision >85% and detection >60 days — fully autonomous prediction

**Feedback Loop:**
Human corrections (wrong churn prediction, missed signals) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% correction rate (P0 criticality) triggers AIG-002 optimization. Monthly audit by AIG-001 for prediction drift.

---

## Agent RI-005: Interaction History Analyst

**Division:** Relationship Intelligence
**Primary Function:** Maintains a comprehensive, searchable narrative of every interaction with each contact and account.
**Triggers:**
- interaction_completed - email, meeting, call, social
- context_needed_for_engagement
- gap_detected_in_coverage
- ccount_review_requested
**Outputs:**
- interaction_timeline - chronological log
- interaction_summary_for_context
- 	opic_tracking - discussed topics, by whom, when
- coverage_gap_report
- context_brief - one-page account history
- elationship_milestones - key events
**Data Sources:** Email archive, meeting transcripts, call logs, CRM activity history, LinkedIn interactions, support tickets
**Training Corpus:** CRM data management best practices, account history management, enterprise relationship history
**LLM Tier:** Moderate (Sonnet class) - history synthesis requires summarization and topic extraction
**Criticality:** P1 - important for continuity but reps maintain context manually
**Why dedicated:** Interaction history is a RAG-intensive data management task operating at scale.
**Prompt Pattern:** RAG (interaction retrieval) + Summarization (context brief)

**Business Outcome:** Reduce time-to-context for revenue team — deliver a complete account interaction brief in <30 seconds, eliminating manual history research and ensuring no relationship milestone is missed.

**Functions (Detailed):**
- retrieve_timeline(account_id, date_range) -> interaction_timeline
- summarize_brief(account_id, context_type) -> context_brief
- extract_topics(interactions) -> topic_tracking
- detect_coverage_gaps(timeline, stakeholders) -> coverage_gap_report
- identify_milestones(interactions) -> relationship_milestones

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Email archive API
- Meeting transcript store
- Call log API
- CRM activity history API
- LinkedIn interaction API
- Support ticket API

**KPIs & Metrics:**
- brief_generation_time: target <30 seconds
- interaction_coverage_completeness: target >95%
- topic_extraction_precision: target >85%
- brief_accuracy_rate: target >90% per user satisfaction

**Performance Score:**
- **Red (<70):** generation time >60s or accuracy <70% — escalate to RI lead
- **Amber (70-85):** generation time 30–60s or accuracy 70–85% — acceptable with manual verification
- **Green (>85):** generation time <30s and accuracy >85% — fully autonomous

**Feedback Loop:**
Human corrections (missing interactions, wrong summaries) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 prompt optimization. Monthly audit by AIG-001.

---

### Division 12: REVENUE OPERATIONS

These agents maintain the operational backbone.

---

## Agent RO-001: CRM Hygiene Agent

**Division:** Revenue Operations
**Primary Function:** Continuously monitors and corrects CRM data quality issues.
**Triggers:**
- 	ick_daily - routine data quality scan
- ecord_created_or_updated - validates on write
- duplicate_detected - merges or flags
- equired_field_missing - alerts owner
- data_aging_threshold_reached
**Outputs:**
- data_quality_score - overall CRM health
- duplicate_alert - with merge recommendation
- missing_field_report
- stale_record_alert
- hygiene_rule_violation
- owner_notification - data quality task list
**Data Sources:** CRM database (accounts, contacts, opportunities, activities), data quality rules, data dictionary
**Training Corpus:** Salesforce data management, master data management (MDM), data quality frameworks (DAMA, TDWI)
**LLM Tier:** Simple (Haiku class) - primarily rule-based validation
**Criticality:** P0 - poor data destroys forecast accuracy
**Why dedicated:** CRM hygiene is continuous data maintenance with a scan-correct pattern.
**Prompt Pattern:** Classification (issue type) + Routing (correction action)

**Business Outcome:** Achieve >95% CRM data accuracy — eliminate duplicate records, stale data, and missing critical fields that erode forecast reliability and pipeline analysis.

**Functions (Detailed):**
- scan_data_quality(crm_database, rules) -> data_quality_score
- detect_duplicates(records, thresholds) -> duplicate_alert
- check_required_fields(record, schema) -> missing_field_report
- flag_stale(records, aging_threshold) -> stale_record_alert
- notify_owner(violation, record_owner) -> owner_notification

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Haiku-class)
- CRM API (read/write records)
- Data quality rules store
- Data dictionary
- User notification service

**KPIs & Metrics:**
- data_quality_score: target >95%
- duplicate_resolution_time: target <24 hours
- required_field_completeness: target >98%
- false_positive_duplicate_rate: target <5%

**Performance Score:**
- **Red (<70):** data quality <80% or duplicate resolution >72h — escalate to RO director
- **Amber (70-85):** quality 80–95% or resolution 24–72h — auto-flag for manual correction
- **Green (>85):** quality >95% and resolution <24h — fully autonomous hygiene

**Feedback Loop:**
Human corrections (wrong merge suggestions, false positives) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly accuracy audit by AIG-001.

---

## Agent RO-002: Pipeline Analyst

**Division:** Revenue Operations
**Primary Function:** Analyzes pipeline health and produces actionable insights for leadership.
**Triggers:**
- 	ick_daily - routine analysis
- pipeline_milestone_reached
- deal_stage_change_batch
- weekly_pipeline_review
- pipeline_anomaly_detected
**Outputs:**
- pipeline_health_dashboard - coverage, aging, stage distribution
- pipeline_velocity_report - days per stage, stage conversion
- pipeline_coverage_ratio_alert
- ging_deals_report
- weighted_pipeline_forecast
- pipeline_contamination_warning
- stage_conversion_analysis
**Data Sources:** CRM opportunity data, historical conversion rates, stage benchmarks, source-of-business data, rep activity
**Training Corpus:** Pipeline analysis (Clari, InsightSquared), revenue operations analytics (Pavilion), sales forecasting
**LLM Tier:** Moderate (Sonnet class) - pipeline analysis requires multi-metric synthesis
**Criticality:** P0 - pipeline analysis drives forecast accuracy
**Why dedicated:** Pipeline analysis is continuous analytical function distinct from data hygiene or forecasting.
**Prompt Pattern:** Analysis (multi-metric synthesis) + Generation (insight narrative)

**Business Outcome:** Improve pipeline visibility to drive forecast reliability >85% — surface contamination, aging, and velocity risks before they distort commit numbers.

**Functions (Detailed):**
- compute_pipeline_health(pipeline_data, benchmarks) -> pipeline_health_dashboard
- analyze_velocity(deals, stage_history) -> pipeline_velocity_report
- alert_coverage(pipeline_coverage_ratio, target) -> pipeline_coverage_ratio_alert
- flag_aging(deals, age_threshold) -> aging_deals_report
- forecast_weighted(opportunities, win_rates) -> weighted_pipeline_forecast
- detect_contamination(deals, risk_signals) -> pipeline_contamination_warning

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- CRM API (opportunity data)
- Data warehouse query API
- BI tool API (Looker/Tableau)
- Historical conversion rates store

**KPIs & Metrics:**
- pipeline_forecast_accuracy: target >85%
- contamination_detection_rate: target >90%
- aging_deal_identification_lead_time: target >30 days
- insight_narrative_relevance_score: target >4/5 user rating

**Performance Score:**
- **Red (<70):** forecast accuracy <70% or contamination detection <70% — escalate to RO VP
- **Amber (70-85):** accuracy 70–85% or detection 70–85% — semi-autonomous with manual pipeline review
- **Green (>85):** accuracy >85% and detection >85% — fully autonomous pipeline analysis

**Feedback Loop:**
Human corrections (wrong velocity analysis, missed contamination) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 prompt optimization. Monthly audit by AIG-001.

---

## Agent RO-003: Forecasting Engine

**Division:** Revenue Operations
**Primary Function:** Generates revenue forecasts using multiple methodologies with confidence intervals.
**Triggers:**
- 	ick_weekly - weekly forecast update
- month_end_approaching
- quarter_end_approaching - daily updates
- pipeline_significant_change
- ooking_recorded
**Outputs:**
- evenue_forecast - with confidence intervals
- orecast_by_category - product, region, segment, rep
- orecast_accuracy_report - actual vs predicted
- scenario_forecast - best/expected/worst case
- orecast_risk_factors
- commit_forecast - high-confidence projections
**Data Sources:** CRM pipeline, historical bookings, win rates, seasonality, economic indicators, territory assignments, rep ramp
**Training Corpus:** Sales forecasting methodologies (Miller Heiman, Salesforce), predictive forecasting (Clari, BoostUp), time series forecasting
**LLM Tier:** Complex Reasoning (Opus class) - forecasting integrates quantitative models with qualitative judgment
**Criticality:** P0 - the entire business runs on forecast accuracy
**Why dedicated:** Forecasting is continuous quantitative analysis with specialized statistical methodology.
**Prompt Pattern:** Analysis (statistical forecasting) + Generation (scenario analysis)

**Business Outcome:** Deliver revenue forecasts within 5% of actuals — provide scenario modeling that enables leadership to make data-driven pipeline investment decisions with quantified confidence intervals.

**Functions (Detailed):**
- generate_forecast(pipeline, history, seasonality) -> revenue_forecast
- analyze_by_dimension(forecast, dimensions) -> forecast_by_category
- measure_accuracy(forecast, actuals) -> forecast_accuracy_report
- model_scenarios(forecast, variables) -> scenario_forecast
- identify_risks(forecast, confidence_intervals) -> forecast_risk_factors
- calculate_commit(pipeline, win_rates) -> commit_forecast

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- CRM API (pipeline, bookings)
- Data warehouse query API
- BI tool API (forecast visualization)
- Economic indicators feed
- Historical bookings store

**KPIs & Metrics:**
- forecast_accuracy_vs_actuals: target within 5%
- confidence_interval_calibration: target >90%
- scenario_generation_speed: target <5 minutes
- quarterly_forecast_bias: target <2% systematic error

**Performance Score:**
- **Red (<70):** accuracy >10% error or bias >5% — escalate to CFO/RO VP
- **Amber (70-85):** accuracy 5–10% error or bias 2–5% — semi-autonomous with finance review
- **Green (>85):** accuracy within 5% and bias <2% — fully autonomous forecasting

**Feedback Loop:**
Human corrections (forecast adjustments, missed risk factors) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% adjustment rate (P0 criticality) triggers AIG-002 optimization. Monthly audit by AIG-001 for forecast drift.

---

## Agent RO-004: Territory Designer

**Division:** Revenue Operations
**Primary Function:** Designs and optimizes sales territories based on account distribution, potential, and workload.
**Triggers:**
- 	ick_quarterly - quarterly review
- 	erritory_imbalance_detected
- 
ew_rep_hired
- ep_leave
- market_shift
- coverage_gap_detected
**Outputs:**
- 	erritory_design_proposal - with rationale
- 	erritory_balance_report - workload, potential, coverage
- ccount_assignment_recommendation
- 	erritory_capacity_analysis
- coverage_gap_alert
- ep_territory_fit_analysis
**Data Sources:** Account data, CRM opportunity history, rep capacity profiles, geographic data, market segmentation
**Training Corpus:** Sales territory design (Zoltners, Sinha, Lorimer), territory optimization, sales force effectiveness
**LLM Tier:** Complex Reasoning (Opus class) - territory design requires multi-objective optimization
**Criticality:** P1 - important but annual manual design is feasible
**Why dedicated:** Territory design is periodic optimization task using different math than forecasting.
**Prompt Pattern:** Analysis (multi-factor optimization) + Generation (design proposal)

**Business Outcome:** Increase rep productivity by 15% through optimally balanced territories — eliminate coverage gaps and workload imbalances that leave revenue potential untapped.

**Functions (Detailed):**
- design_territory(accounts, reps, constraints) -> territory_design_proposal
- balance_workload(territories, account_potential) -> territory_balance_report
- recommend_assignment(account, rep_profiles) -> account_assignment_recommendation
- analyze_capacity(territory, rep_capacity) -> territory_capacity_analysis
- detect_coverage_gap(territories, market_data) -> coverage_gap_alert

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- CRM API (account data, opportunities)
- Geographic data API
- Rep capacity profiles store
- Market segmentation data
- BI tool API

**KPIs & Metrics:**
- territory_balance_score: target >85% equity
- coverage_gap_elimination: target >90% of gaps closed
- workload_variance_across_territories: target <15%
- design_proposal_acceptance_rate: target >80%

**Performance Score:**
- **Red (<70):** balance score <70% or coverage gaps >30% unresolved — escalate to RO VP
- **Amber (70-85):** balance 70–85% or coverage 10–30% gaps — semi-autonomous with manual tuning
- **Green (>85):** balance >85% and coverage gaps <10% — fully autonomous territory design

**Feedback Loop:**
Human corrections (wrong assignments, unbalanced workloads) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Quarterly audit by AIG-001 for design drift.

---

## Agent RO-005: Commission Tracker

**Division:** Revenue Operations
**Primary Function:** Tracks commissions and variable compensation calculations.
**Triggers:**
- deal_closed - calculates commission
- month_end - commission statements
- quarter_end - quarterly calculations
- compensation_plan_changed
- commission_query_from_rep
**Outputs:**
- commission_calculation - per-deal with breakdown
- commission_statement - period summary
- ttainment_dashboard - real-time quota attainment
- compensation_scenario - what to close to make quota
- discrepancy_alert - calculation error
- spiff_tracking - special incentive progress
**Data Sources:** CRM closed won deals, compensation plan, quota assignments, commission rates, rep hierarchy
**Training Corpus:** Sales compensation design (Zoltners), commission administration, variable compensation (Xactly)
**LLM Tier:** Simple (Haiku class) - commission calculation is rule-based arithmetic
**Criticality:** P1 - critical for rep trust but manual payroll exists
**Why dedicated:** Commission tracking is transaction-processing with accuracy requirements distinct from analytical tasks.
**Prompt Pattern:** Routing (rule selection) + Analysis (calculation) + Generation (statement)

**Business Outcome:** Eliminate commission errors and disputes — achieve 100% calculation accuracy and provide reps with real-time attainment visibility, maintaining sales team trust and reducing finance query volume by 80%.

**Functions (Detailed):**
- calculate_commission(deal, plan, quotas) -> commission_calculation
- generate_statement(rep_id, period) -> commission_statement
- compute_attainment(rep_id, quota, closed_deals) -> attainment_dashboard
- model_compensation(rep_id, pipeline, plan) -> compensation_scenario
- detect_discrepancy(calculated, expected) -> discrepancy_alert
- track_spiff(spiff_program, rep_activity) -> spiff_tracking

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Haiku-class)
- CRM API (closed won deals)
- Compensation plan store
- Quota assignment DB
- Commission rates table
- Rep hierarchy data

**KPIs & Metrics:**
- commission_calculation_accuracy: target 100%
- statement_delivery_latency: target <1 hour post-close
- finance_query_volume_reduction: target >80%
- discrepancy_detection_rate: target >99%

**Performance Score:**
- **Red (<70):** accuracy <98% or discrepancy detection <90% — escalate to finance director
- **Amber (70-85):** accuracy 98–99.9% or latency 1–4h — semi-autonomous with manual spot-check
- **Green (>85):** accuracy 100% and latency <1h — fully autonomous commission tracking

**Feedback Loop:**
Human corrections (calculation errors, wrong plan applied) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% correction rate (P1 financial accuracy) triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent RO-006: Process Compliance Agent

**Division:** Revenue Operations
**Primary Function:** Monitors adherence to defined revenue processes and methodologies.
**Triggers:**
- deal_stage_change_attempted
- process_step_skipped
- equired_field_missing_at_stage
- methodology_usage_monitoring
- udit_requested
**Outputs:**
- process_compliance_score
- stage_gate_verdict - passed/blocked
- compliance_violation_alert
- coaching_recommendation
- methodology_usage_report
- process_gap_analysis
**Data Sources:** CRM opportunity data, stage history, meeting transcripts, activity logs, process definitions, methodology scorecards
**Training Corpus:** Sales process design, stage-gate methodologies, revenue operations compliance
**LLM Tier:** Moderate (Sonnet class) - compliance requires evidence evaluation against process rules
**Criticality:** P1 - important for consistency
**Why dedicated:** Process compliance is monitoring and enforcement that must remain independent from execution agents.
**Prompt Pattern:** Classification (pass/fail per rule) + Routing (block/allow transition)

**Business Outcome:** Ensure 100% sales methodology compliance across the revenue organization — reduce process leakage that causes 20%+ pipeline inaccuracy and coaching gaps.

**Functions (Detailed):**
- check_compliance(deal, process_definitions) -> process_compliance_score
- verify_stage_gate(deal, stage, gate_criteria) -> stage_gate_verdict
- alert_violation(deal, rule, severity) -> compliance_violation_alert
- recommend_coaching(violation_pattern, rep_profile) -> coaching_recommendation
- report_methodology_usage(process, usage_data) -> methodology_usage_report
- analyze_process_gaps(compliance_data, benchmarks) -> process_gap_analysis

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- CRM API (opportunity, stage history)
- Meeting transcript store
- Activity log API
- Process definition store
- Methodology scorecard DB

**KPIs & Metrics:**
- process_compliance_rate: target >90%
- stage_gate_accuracy: target >95%
- false_positive_block_rate: target <5%
- coaching_recommendation_relevance: target >4/5 user rating

**Performance Score:**
- **Red (<70):** compliance rate <75% or false positive rate >15% — escalate to RO VP
- **Amber (70-85):** compliance 75–90% or false positive 5–15% — semi-autonomous with manual override
- **Green (>85):** compliance >90% and false positives <5% — fully autonomous compliance monitoring

**Feedback Loop:**
Human corrections (wrong block/allow verdicts, false positives) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---


### Division 13: CUSTOMER SUCCESS

These agents monitor, manage, and grow customer relationships post-sale.

---

## Agent CS-001: Customer Health Scorer

**Division:** Customer Success
**Primary Function:** Continuously evaluates customer health by integrating usage, support, relationship, and financial signals.
**Triggers:**
- 	ick_daily - recalculates scores
- usage_threshold_crossed
- support_ticket_filed
- enewal_approaching
- illing_issue_detected
**Outputs:**
- customer_health_score - composite 1-100 with trend
- health_dimension_breakdown
- health_segment_assignment - green/yellow/red
- health_degradation_alert
- portfolio_health_summary
- cs_workload_prioritization
**Data Sources:** Product usage analytics, support ticket data, NPS/CSAT, relationship health scores, billing/payment data
**Training Corpus:** Customer health scoring (Gainsight, Totango, Planhat), customer success metrics (Nick Mehta), Gainsight blog health scoring methodology, ChurnZero blog churn signals, Lincoln Murphy LinkedIn customer success insights
**LLM Tier:** Moderate (Sonnet class) - health scoring requires multi-signal synthesis
**Criticality:** P0 - without health scoring, CS teams do not know where to focus
**Why dedicated:** Health scoring is continuous monitoring with different cadence and inputs than other agents.
**Prompt Pattern:** Scoring (multi-factor computation) + Classification (segment assignment)

**Business Outcome:** Improve retention rate by 20% through early health score intervention — correlate health scores to renewal outcomes and direct CSM effort to accounts with declining scores before churn becomes inevitable.

**Functions (Detailed):**
- compute_health(usage, support, relationship, billing) -> customer_health_score
- breakdown_dimensions(health_score, signal_sources) -> health_dimension_breakdown
- assign_segment(health_score, thresholds) -> health_segment_assignment
- alert_degradation(health_trend, threshold) -> health_degradation_alert
- summarize_portfolio(all_scores, segment_filter) -> portfolio_health_summary
- prioritize_workload(scores, csm_capacity) -> cs_workload_prioritization

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Product usage analytics API
- Support ticket API
- Health score KV store
- NPS/CSAT survey API
- CRM API (account data)
- Billing/payment data API

**KPIs & Metrics:**
- health_score_renewal_correlation: target R² >0.75
- early_degradation_detection_rate: target >85%
- false_positive_segment_rate: target <10%
- csm_adoption_of_scores: target >90% weekly active usage

**Performance Score:**
- **Red (<70):** renewal correlation <0.5 or false positives >20% — escalate to CS VP
- **Amber (70-85):** correlation 0.5–0.75 or false positives 10–20% — semi-autonomous with CSM verification
- **Green (>85):** correlation >0.75 and false positives <10% — fully autonomous scoring

**Feedback Loop:**
Human corrections (wrong segment, missed degradation) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001 for score drift.

---

## Agent CS-002: Adoption Monitor

**Division:** Customer Success
**Primary Function:** Tracks product adoption and identifies at-risk users.
**Triggers:**
- 	ick_weekly - routine adoption analysis
- user_onboarded
- eature_usage_drops_below_threshold
- power_user_detected
- 
ew_feature_released
- user_inactive_for_N_days
**Outputs:**
- doption_health_score - per-account and per-user
- eature_adoption_matrix
- doption_risk_alert
- power_user_report - expansion opportunities
- doption_campaign_recommendation
- 	ime_to_value_analysis
- onboarding_completion_rate
**Data Sources:** Product analytics, onboarding milestones, user roles, training completion, support ticket topics
**Training Corpus:** SaaS adoption metrics, product-led growth (Wes Bush, OpenView), user onboarding (Appcues, Userpilot)
**LLM Tier:** Moderate (Sonnet class) - adoption analysis requires behavioral pattern recognition
**Criticality:** P1 - important for retention but manual check-ins possible
**Why dedicated:** Adoption monitoring requires continuous product analytics integration distinct from health scoring.
**Prompt Pattern:** Analysis (usage pattern) + Classification (risk level) + Generation (campaign)

**Business Outcome:** Increase active user adoption by 30% and reduce time-to-value by 40% through targeted adoption campaigns — identify power users for expansion and at-risk users for re-engagement before they churn.

**Functions (Detailed):**
- compute_adoption(account_id, usage_data) -> adoption_health_score
- analyze_features(feature_usage, account_segment) -> feature_adoption_matrix
- flag_risk(user_activity, inactivity_threshold) -> adoption_risk_alert
- identify_power_users(usage_patterns, thresholds) -> power_user_report
- recommend_campaign(risk_factors, user_profile) -> adoption_campaign_recommendation
- analyze_time_to_value(onboarding_data, first_value_event) -> time_to_value_analysis

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Product usage analytics API
- User roles and profiles store
- Training completion data API
- Support ticket API (topic analysis)
- CRM API (account segment)

**KPIs & Metrics:**
- active_user_adoption_rate: target >80%
- time_to_value_reduction: target >40% improvement
- power_user_identification_precision: target >90%
- campaign_recommendation_effectiveness: target >4/5 CSM rating

**Performance Score:**
- **Red (<70):** adoption rate lift <10% or power user precision <70% — escalate to CS director
- **Amber (70-85):** adoption lift 10–30% or precision 70–90% — semi-autonomous with CSM campaign review
- **Green (>85):** adoption lift >30% and precision >90% — fully autonomous adoption monitoring

**Feedback Loop:**
Human corrections (wrong risk flags, missed power users) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent CS-003: Expansion Identifier

**Division:** Customer Success
**Primary Function:** Identifies expansion opportunities based on usage growth, new feature adoption, stakeholder expansion, and business milestones.
**Triggers:**
- usage_growth_threshold_crossed
- 
ew_department_user_added
- power_user_detected
- contract_renewal_approaching
- customer_business_milestone - funding, acquisition, IPO
- eature_adoption_reaches_threshold
**Outputs:**
- expansion_opportunity_alert - with recommended offer
- upsell_recommendation - product/seat/edition upgrade
- cross_sell_recommendation - related product
- expansion_timing_suggestion - optimal approach window
- expansion_health_check - is customer ready
- expansion_value_projection - expected additional revenue
- expansion_risk_flag - signs customer not ready
**Data Sources:** Product usage analytics, account firmographics, contract data, customer health score, support interaction themes, business news
**Training Corpus:** SaaS expansion selling, product-led growth expansion, customer success upsell frameworks (Gainsight)
**LLM Tier:** Moderate (Sonnet class) - expansion identification requires multi-signal opportunity detection
**Criticality:** P1 - expansion revenue is high-margin but not critical for survival
**Why dedicated:** Expansion identification requires a growth-oriented lens distinct from health monitoring or risk detection.
**Prompt Pattern:** Classification (expansion readiness) + Generation (upsell recommendation)

**Business Outcome:** Increase expansion revenue by 25% year-over-year by identifying upsell and cross-sell opportunities from product usage growth, stakeholder expansion, and business milestone signals.

**Functions (Detailed):**
- detect_expansion_opportunity(usage, growth_signals) -> expansion_opportunity_alert
- recommend_upsell(account, product_usage) -> upsell_recommendation
- recommend_cross_sell(account, product_map) -> cross_sell_recommendation
- suggest_timing(account_health, renewal_date) -> expansion_timing_suggestion
- check_readiness(account_health, usage_depth) -> expansion_health_check
- project_value(opportunity, win_probability) -> expansion_value_projection

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Product usage analytics API
- Account firmographics data
- Contract data store
- Customer health score KV store
- Business news API (milestone detection)
- CRM API (opportunity pipeline)

**KPIs & Metrics:**
- expansion_opportunity_identification_rate: target >80% capture
- upsell_recommendation_acceptance_rate: target >30%
- cross_sell_conversion_rate: target >15%
- false_positive_expansion_flags: target <15%

**Performance Score:**
- **Red (<70):** opportunity capture <60% or false positives >30% — escalate to CS VP
- **Amber (70-85):** capture 60–80% or false positives 15–30% — semi-autonomous with CSM review
- **Green (>85):** capture >80% and false positives <15% — fully autonomous expansion identification

**Feedback Loop:**
Human corrections (wrong expansion timing, irrelevant recommendations) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent CS-004: Renewal Risk Manager

**Division:** Customer Success
**Primary Function:** Monitors renewal pipeline, identifies at-risk renewals, and orchestrates retention workflows.
**Triggers:**
- enewal_N_days_away - triggers monitoring at 90/60/30 days
- health_score_drops_below_renewal_threshold
- support_escalation_on_renewal_account
- usage_drop_on_renewal_account
- executive_change_at_renewal_account
- competitive_activity_on_account
**Outputs:**
- enewal_risk_score - likelihood of renewal
- enewal_risk_factors - ranked
- etention_workflow - specific actions and timing
- enewal_offer_recommendation - pricing/terms
- executive_escalation_recommendation - when to involve leadership
- enewal_forecast - expected renewal rate across book
- lost_renewal_analysis - root cause when renewal lost
**Data Sources:** Customer health scores, contract/renewal dates, product usage, support history, relationship health, competitive intelligence
**Training Corpus:** SaaS renewal management, customer retention frameworks, churn reduction methodologies (Gainsight, Totango)
**LLM Tier:** Complex Reasoning (Opus class) - renewal risk requires integrating risk factors and orchestrating intervention
**Criticality:** P0 - renewal revenue is the lifeblood of SaaS
**Why dedicated:** Renewal risk is a time-bound monitoring task with specific SLA windows distinct from general health scoring.
**Prompt Pattern:** Analysis (risk factor integration) + Generation (retention workflow)

**Business Outcome:** Achieve >90% renewal rate on monitored accounts — orchestrate automated retention workflows for at-risk renewals, reducing manual escalation and preventing revenue leakage from avoidable churn.

**Functions (Detailed):**
- assess_risk(account, health_scores, signals) -> renewal_risk_score
- rank_risk_factors(risk_score, signal_weights) -> renewal_risk_factors
- orchestrate_retention(risk_factors, playbooks) -> retention_workflow
- recommend_offer(account_value, risk_level) -> renewal_offer_recommendation
- forecast_renewal(portfolio, risk_scores) -> renewal_forecast
- analyze_loss(renewal_lost, account_history) -> lost_renewal_analysis

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- Customer health score KV store
- Contract/renewal dates store
- Product usage analytics API
- Support history API
- Relationship health store
- Competitive intelligence feed

**KPIs & Metrics:**
- renewal_rate_on_monitored_accounts: target >90%
- at_risk_account_identification_precision: target >85%
- retention_workflow_execution_rate: target >95%
- intervention_to_renewal_conversion: target >50%

**Performance Score:**
- **Red (<70):** renewal rate <80% or at-risk precision <65% — escalate to CS VP
- **Amber (70-85):** renewal rate 80–90% or precision 65–85% — semi-autonomous with CSM escalation review
- **Green (>85):** renewal rate >90% and precision >85% — fully autonomous renewal risk management

**Feedback Loop:**
Human corrections (wrong risk classification, missed signals) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% correction rate (P0 renewal revenue) triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent CS-005: Onboarding Conductor

**Division:** Customer Success
**Primary Function:** Orchestrates the end-to-end customer onboarding experience, ensuring milestones are met, stakeholders are engaged, and time-to-value is optimized.
**Triggers:**
- deal_won - initiates onboarding sequence
- onboarding_milestone_completed
- onboarding_delayed_beyond_threshold
- stakeholder_not_engaged
- customer_health_drops_during_onboarding
- product_activation_completed
**Outputs:**
- onboarding_plan - customized timeline with milestones
- stakeholder_engagement_tracker - who has been activated
- onboarding_health_score - likelihood of successful onboarding
- risk_alert - when onboarding is off-track
- time_to_value_prediction - expected days to first value
- onboarding_playbook_recommendation - best practices per segment
- handoff_summary - to CSM post-onboarding
**Data Sources:** CRM deal data, product activation events, user roles and profiles, training completion data, support ticket initiation, customer success playbooks
**Training Corpus:** Customer onboarding methodology (Winning by Design, HubSpot), time-to-value optimization (TSIA), user adoption frameworks (Appcues, Userpilot)
**LLM Tier:** Moderate (Sonnet class) - orchestration follows structured playbook patterns
**Criticality:** P1 - poor onboarding leads to churn but manual oversight can compensate
**Why dedicated:** Onboarding is a time-bound, milestone-driven orchestration task with distinct velocity metrics from ongoing customer success.
**Prompt Pattern:** Planning (milestone sequence) + Scoring (onboarding health) + Generation (intervention)

**Business Outcome:** Reduce time-to-first-value by 50% — ensure 90%+ of new customers reach onboarding milestones within SLA windows through automated orchestration and early risk detection.

**Functions (Detailed):**
- create_onboarding_plan(deal_data, playbook) -> onboarding_plan
- track_stakeholder_engagement(users, milestones) -> stakeholder_engagement_tracker
- score_onboarding_health(milestones, engagement, timeline) -> onboarding_health_score
- alert_delay(current_status, plan) -> risk_alert
- predict_time_to_value(progress, segment_data) -> time_to_value_prediction
- recommend_playbook(segment, onboarding_status) -> onboarding_playbook_recommendation

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- CRM API (deal data)
- Product activation events API
- User roles and profiles store
- Training completion data API
- Support ticket API
- Customer success playbooks store

**KPIs & Metrics:**
- time_to_value_reduction: target >50%
- milestone_completion_within_sla: target >90%
- stakeholder_activation_rate_at_30_days: target >80%
- onboarding_health_score_accuracy: target >85%

**Performance Score:**
- **Red (<70):** TTV reduction <20% or SLA completion <70% — escalate to CS director
- **Amber (70-85):** TTV reduction 20–50% or SLA 70–90% — semi-autonomous with CSM intervention
- **Green (>85):** TTV reduction >50% and SLA >90% — fully autonomous onboarding

**Feedback Loop:**
Human corrections (wrong milestone sequence, missed stakeholders) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent CS-006: QBR (Quarterly Business Review) Automator

**Division:** Customer Success
**Primary Function:** Automatically generates comprehensive QBR presentations from account data.
**Triggers:**
- qbr_due_date_approaching
- customer_requested_qbr
- cs_manager_requests_qbr_draft
- ccount_milestone_reached
**Outputs:**
- qbr_presentation - complete deck with data, insights, recommendations
- qbr_executive_summary - one-page version
- alue_realization_report - ROI achieved vs projected
- health_and_adoption_review - metrics with trends
- ecommendations_for_next_quarter
- qbr_follow_up_items - commitments and action items
- qbr_effectiveness_tracking - did recommendations convert
**Data Sources:** Product usage analytics, health scores, support summary, business case/ROI from sales cycle, contract data, expansion pipeline
**Training Corpus:** QBR best practices (Gainsight, ClientSuccess), executive presentation frameworks, value realization reporting
**LLM Tier:** Moderate (Sonnet class) - QBR generation is structured reporting with some analysis
**Criticality:** P2 - valuable but CS teams can build QBRs manually
**Why dedicated:** QBR automation is a recurring document generation task with distinct timing and data integration needs.
**Prompt Pattern:** Generation (structured presentation) + Analysis (value realization) + Summarization (account history)

**Business Outcome:** Scale QBR capacity by 5x — generate complete, data-driven QBR presentations in <30 minutes, enabling CSMs to serve more accounts with consistent quality and actionable insights.

**Functions (Detailed):**
- generate_qbr_presentation(account_data, template) -> qbr_presentation
- summarize_executive(account_data, metrics) -> qbr_executive_summary
- analyze_value_realization(roi_metrics, baseline) -> value_realization_report
- review_health(health_scores, trends) -> health_and_adoption_review
- recommend_next_quarter(performance, goals) -> recommendations_for_next_quarter
- track_qbr_effectiveness(recommendations, outcomes) -> qbr_effectiveness_tracking

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Product usage analytics API
- Health score KV store
- Support summary API
- Contract data store
- CRM API (opportunity pipeline)
- Slide generation API (PowerPoint/Google Slides)

**KPIs & Metrics:**
- qbr_generation_time: target <30 minutes
- qbr_quality_score: target >4/5 CSM rating
- qbr_insight_conversion_rate: target >40%
- qbr_coverage_expansion: target >5x accounts per CSM

**Performance Score:**
- **Red (<70):** generation time >90 min or quality score <3/5 — escalate to CS director
- **Amber (70-85):** time 30–90 min or quality 3–4/5 — semi-autonomous with manual review
- **Green (>85):** time <30 min and quality >4/5 — fully autonomous QBR generation

**Feedback Loop:**
Human corrections (wrong data points, poor slide structure) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent CS-007: Escalation Triage Agent

**Division:** Customer Success
**Primary Function:** Triages customer escalations, assesses severity, and routes to the appropriate resolution team.
**Triggers:**
- support_ticket_escalated
- customer_complaint_received - negative sentiment threshold
- executive_involved_in_support_issue
- sla_breach_imminent_or_occurred
- product_outage_or_security_incident
- illing_dispute_escalated
**Outputs:**
- escalation_severity_assessment - severity level with impact
- escalation_routing - correct team/person with context
- escalation_brief - structured summary for assignee
- customer_communication_draft - initial response
- esolution_timeline_estimate
- escalation_tracking - status and SLA monitoring
- post_escalation_review - RCA after resolution
**Data Sources:** Support ticket system, customer health scores, contract data (SLA terms), product status, customer communication history, escalation playbooks
**Training Corpus:** ITIL incident management, customer support escalation frameworks, SLA management, crisis communication
**LLM Tier:** Moderate (Sonnet class) - triage requires severity classification and routing
**Criticality:** P0 - mishandled escalations destroy customer relationships
**Why dedicated:** Escalation triage requires immediate response with severity judgment, a different operational tempo from other CS agents.
**Prompt Pattern:** Classification (severity) + Routing (assignment) + Generation (response and brief)

**Business Outcome:** Reduce escalation response time by 60% — ensure P0 escalations are triaged and routed within 5 minutes with complete context, preventing SLA breaches and minimizing customer impact.

**Functions (Detailed):**
- assess_severity(escalation, impact_criteria) -> escalation_severity_assessment
- route_escalation(severity, team_capacity) -> escalation_routing
- generate_brief(escalation, context) -> escalation_brief
- draft_response(escalation_type, customer_profile) -> customer_communication_draft
- estimate_resolution(issue_type, complexity) -> resolution_timeline_estimate
- track_escalation(escalation_id, sla) -> escalation_tracking

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Support ticket system API
- Customer health score KV store
- Contract data (SLA terms)
- Product status API
- Escalation playbooks store
- Customer communication history API

**KPIs & Metrics:**
- p0_escalation_response_time: target <5 minutes
- triage_accuracy: target >95%
- sla_breach_prevention_rate: target >99%
- escalation_routing_correctness: target >90% first-time routing

**Performance Score:**
- **Red (<70):** p0 response >15 min or triage accuracy <80% — escalate to CS VP
- **Amber (70-85):** p0 response 5–15 min or accuracy 80–95% — semi-autonomous with supervisor monitoring
- **Green (>85):** p0 response <5 min and accuracy >95% — fully autonomous triage

**Feedback Loop:**
Human corrections (wrong severity, misrouted escalations) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% correction rate (P0 criticality) triggers AIG-002 optimization. Monthly audit by AIG-001.

---


### Division 14: ABM TEAM

Account-Based Marketing agents that orchestrate targeted campaigns for high-value accounts.

---

## Agent ABM-001: Account Tiering Agent

**Division:** ABM Team
**Primary Function:** Scores and tiers accounts based on fit, engagement, intent, and revenue potential.
**Triggers:**
- 	ick_weekly - recalculates account tiers
- 
ew_account_discovered
- intent_signal_spike on an account
- ccount_revenue_potential_recalculated
- pipeline_value_changes_significantly
**Outputs:**
- ccount_tier_assignment - tier 1/2/3 with rationale
- ccount_score_breakdown - fit, engagement, intent, potential
- 	ier_migration_alert - account moved between tiers
- ccount_selection_recommendation - which accounts to target
- 	ier_distribution_report - count per tier
- ccount_reassessment_schedule - when to re-evaluate
**Data Sources:** Firmographic data, intent signals, CRM pipeline history, engagement data (web, email, ads), ICP definition
**Training Corpus:** ABM account selection (ITSMA, Demandbase), account tiering frameworks (Terminus), ideal customer profile development
**LLM Tier:** Moderate (Sonnet class) - tiering requires multi-factor scoring with qualitative judgment
**Criticality:** P1 - critical for ABM program efficiency
**Why dedicated:** Account tiering is a periodic recalculation task with specific scoring methodology distinct from campaign execution.
**Prompt Pattern:** Scoring (multi-factor) + Classification (tier assignment)

**Business Outcome:** Increase ABM pipeline velocity by 35% — focus campaign resources on accounts with highest fit, engagement, and intent scores, eliminating wasted spend on low-potential targets.

**Functions (Detailed):**
- score_account_tier(account, icp_model, signals) -> account_tier_assignment
- breakdown_score(account, dimensions) -> account_score_breakdown
- alert_tier_migration(account, old_tier, new_tier) -> tier_migration_alert
- recommend_accounts(candidates, capacity) -> account_selection_recommendation
- report_distribution(tier_assignments) -> tier_distribution_report

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- ABM platform API (Demandbase/6sense)
- LinkedIn API (firmographic data)
- Intent data API (Bombora/6sense)
- CRM API (pipeline history)
- ICP definition store

**KPIs & Metrics:**
- tier_assignment_accuracy_vs_conversion: target >85%
- abm_pipeline_velocity_lift: target >35%
- tier_1_account_to_opportunity_conversion: target >25%
- false_positive_tier_1_rate: target <10%

**Performance Score:**
- **Red (<70):** assignment accuracy <70% or tier-1 conversion <15% — escalate to ABM director
- **Amber (70-85):** accuracy 70–85% or conversion 15–25% — semi-autonomous with program manager review
- **Green (>85):** accuracy >85% and conversion >25% — fully autonomous tiering

**Feedback Loop:**
Human corrections (wrong tier assignments, missed ICP fits) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001 for tier drift.

---

## Agent ABM-002: Account Researcher (ABM)

**Division:** ABM Team
**Primary Function:** Produces deep research briefs on target accounts for personalized ABM campaigns.
**Triggers:**
- ccount_selected_for_abm - triggers full research
- bm_campaign_starting
- ccount_news_event - updates research
- quarterly_account_review
**Outputs:**
- bm_account_brief - org structure, key stakeholders, technology stack, recent news, growth signals, competitive landscape, strategic initiatives
- stakeholder_engagement_history - past interactions across org
- ccount_strategic_priorities - inferred from public data
- personalization_opportunities - hooks for campaigns
- competitor_relationship_map - competitor footprint in account
- ccount_timeline - key dates and events
**Data Sources:** LinkedIn, CrunchBase, SEC filings, news RSS, company blog, job boards, technographic data, CRM history, competitor intelligence
**Training Corpus:** ABM account research methodologies (Demandbase, Terminus), competitive intelligence, financial analysis for account profiling
**LLM Tier:** Moderate (Sonnet class) - research briefs require synthesis of multiple data sources
**Criticality:** P1 - research depth directly impacts campaign personalization
**Why dedicated:** ABM research is broader and deeper than SDR-level account research, justifying a dedicated agent with different data sources.
**Prompt Pattern:** Extraction (entity and signal extraction) + Summarization (research brief) + Analysis (strategic inference)

**Business Outcome:** Improve ABM campaign personalization depth by 80% — deliver comprehensive account briefs with strategic priorities, stakeholder maps, and personalization hooks within 24 hours of account selection.

**Functions (Detailed):**
- research_account(account_id, sources) -> abm_account_brief
- extract_stakeholders(brief, crm_data) -> stakeholder_engagement_history
- infer_priorities(public_data, industry_trends) -> account_strategic_priorities
- identify_hooks(account_data, solution_capabilities) -> personalization_opportunities
- map_competitors(account, competitive_db) -> competitor_relationship_map
- build_timeline(account, news_sources) -> account_timeline

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- LinkedIn API (company, people data)
- CrunchBase API
- News RSS feed API
- Company blog and job board scraper
- CRM API (engagement history)
- Competitive intelligence store

**KPIs & Metrics:**
- brief_delivery_time: target <24 hours
- account_coverage_depth: target >85% of strategic questions answered
- personalization_hook_accuracy: target >4/5 campaign manager rating
- research_relevance_score: target >90% actionable insights

**Performance Score:**
- **Red (<70):** delivery >48h or depth <60% — escalate to ABM director
- **Amber (70-85):** delivery 24–48h or depth 60–85% — semi-autonomous with researcher supplement
- **Green (>85):** delivery <24h and depth >85% — fully autonomous account research

**Feedback Loop:**
Human corrections (missing intelligence, wrong priorities) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent ABM-003: Personalized Campaign Orchestrator

**Division:** ABM Team
**Primary Function:** Designs and orchestrates multi-channel, multi-touch ABM campaigns for target accounts.
**Triggers:**
- ccount_tier_assigned_as_tier1
- bm_campaign_kickoff
- intent_signal_received_for_abm_account
- campaign_stage_needs_update
- engagement_milestone_reached
**Outputs:**
- campaign_plan - channel mix, timeline, content, cadence
- channel_assignment - email, LinkedIn ads, direct mail, events, SDR outreach
- content_requirements - what content to create per touchpoint
- campaign_execution_commands - triggers for downstream systems
- campaign_performance_report - engagement by channel
- campaign_optimization_recommendations
- ccount_progression_update - moved through awareness/consideration/decision
**Data Sources:** ABM platform, intent data, CRM, marketing automation, content library, advertising platforms, SDR engagement data
**Training Corpus:** ABM campaign orchestration (ITSMA, Demandbase, Terminus), multi-channel campaign design, account progression frameworks
**LLM Tier:** Complex Reasoning (Opus class) - campaign orchestration requires sequencing and channel optimization
**Criticality:** P1 - ABM effectiveness depends on campaign design
**Why dedicated:** Campaign orchestration is a design and project management function distinct from research or execution agents.
**Prompt Pattern:** Generation (campaign plan) + Routing (channel assignment) + Analysis (performance)

**Business Outcome:** Increase target account engagement rate by 50% through orchestrated multi-channel campaigns that deliver the right message on the right channel at the right stage of the buying journey.

**Functions (Detailed):**
- design_campaign(account, tier, objectives) -> campaign_plan
- assign_channels(plan, channel_effectiveness) -> channel_assignment
- define_content(plan, account_research) -> content_requirements
- trigger_execution(commands, downstream_systems) -> campaign_execution_commands
- report_performance(campaign_data, kpis) -> campaign_performance_report
- optimize(performance_data, recommendations) -> campaign_optimization_recommendations

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- ABM platform API (Demandbase/6sense)
- LinkedIn API (ads, sponsored content)
- Intent data API
- CRM API (accounts, contacts)
- Marketing automation API
- Content library store

**KPIs & Metrics:**
- target_account_engagement_rate_lift: target >50%
- campaign_milestone_completion_rate: target >90%
- channel_attribution_accuracy: target >85%
- campaign_roi: target >5:1 on ABM campaigns

**Performance Score:**
- **Red (<70):** engagement lift <20% or channel attribution <65% — escalate to ABM director
- **Amber (70-85):** lift 20–50% or attribution 65–85% — semi-autonomous with campaign manager tuning
- **Green (>85):** lift >50% and attribution >85% — fully autonomous campaign orchestration

**Feedback Loop:**
Human corrections (wrong channel mix, poor content direction) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent ABM-004: Intent Signal Aggregator (ABM)

**Division:** ABM Team
**Primary Function:** Aggregates and scores intent signals across target accounts from multiple sources.
**Triggers:**
- 	ick_6_hours - scans intent sources
- intent_signal_received from any source
- intent_threshold_crossed for an account
- intent_provider_data_refresh
**Outputs:**
- ggregated_intent_score - per-account composite
- intent_signal_detail - topic, source, frequency, trend
- intent_spike_alert - sudden increase
- intent_topic_clusters - what topics are being researched
- uying_stage_inference - early/late stage based on topics
- intent_false_positive_flag - likely noise
- intent_comparison_report - which accounts have highest intent
**Data Sources:** 6sense/Bombora, G2 buyer intent, LinkedIn, content consumption events, website behavior, ad engagement, competitor research signals
**Training Corpus:** Intent data interpretation (6sense, Bombora, Demandbase), predictive lead scoring, buying signal taxonomy
**LLM Tier:** Moderate (Sonnet class) - intent aggregation requires signal quality assessment
**Criticality:** P1 - intent data is core to ABM targeting
**Why dedicated:** Intent aggregation requires continuous scanning and fusion from multiple sources, distinct from campaign orchestration.
**Prompt Pattern:** Classification (signal quality/type) + Scoring (intent strength) + Analysis (topic clustering)

**Business Outcome:** Prioritize ABM resources on accounts showing real buying intent — surface high-intent accounts 2 weeks faster than single-source methods and eliminate noise from false positive signals.

**Functions (Detailed):**
- aggregate_intent(account_id, multiple_sources) -> aggregated_intent_score
- detail_signals(account_id, source_name) -> intent_signal_detail
- alert_spike(account_id, intent_delta) -> intent_spike_alert
- cluster_topics(signals, period) -> intent_topic_clusters
- infer_buying_stage(topics, signal_patterns) -> buying_stage_inference
- flag_noise(signal, source_reliability) -> intent_false_positive_flag

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Intent data API (Bombora/6sense)
- G2 buyer intent API
- LinkedIn API (content consumption)
- Website behavior analytics API
- Ad engagement API
- CRM API (opportunity correlation)

**KPIs & Metrics:**
- high_intent_account_identification_lead_time: target >2 weeks earlier than single-source
- signal_quality_classification_accuracy: target >90%
- false_positive_signal_rate: target <10%
- intent_to_opportunity_conversion_lift: target >30%

**Performance Score:**
- **Red (<70):** lead time <1 week or false positives >25% — escalate to ABM director
- **Amber (70-85):** lead time 1–2 weeks or false positives 10–25% — semi-autonomous with analyst review
- **Green (>85):** lead time >2 weeks and false positives <10% — fully autonomous intent aggregation

**Feedback Loop:**
Human corrections (wrong signal classification, false positives) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent ABM-005: Account Progression Tracker

**Division:** ABM Team
**Primary Function:** Tracks target accounts through the ABM funnel from awareness to opportunity.
**Triggers:**
- bm_account_added
- engagement_event_recorded
- campaign_touch_completed
- meeting_booked_with_account
- opportunity_created_on_abm_account
- ccount_stagnation_detected
**Outputs:**
- ccount_progression_status - funnel stage with evidence
- ccount_velocity_metrics - time per stage
- engagement_depth_score - breadth and depth of engagement
- ccount_stuck_alert - account not progressing
- 
ext_best_action - recommended next engagement
- ccount_readiness_assessment - ready for sales conversation
- bm_to_sdr_handoff_recommendation - when to involve SDR
**Data Sources:** Marketing automation engagement data, CRM activity, meeting data, email engagement, ad engagement, web behavior
**Training Corpus:** ABM funnel frameworks (ITSMA, Demandbase), account progression metrics, B2B buying journey stages
**LLM Tier:** Moderate (Sonnet class) - progression tracking requires stage classification with evidence
**Criticality:** P1 - critical for ABM program accountability
**Why dedicated:** Progression tracking is a funnel management function distinct from campaign design or execution.
**Prompt Pattern:** Classification (funnel stage) + Analysis (velocity and stagnation) + Generation (next action)

**Business Outcome:** Increase ABM-to-sales handoff efficiency by 40% — track every target account through the ABM funnel with engagement depth metrics and automatically recommend the optimal moment to engage sales.

**Functions (Detailed):**
- track_progression(account, engagement_events) -> account_progression_status
- measure_velocity(account, stage_history) -> account_velocity_metrics
- score_engagement_depth(events, channels) -> engagement_depth_score
- alert_stuck(account, stagnation_threshold) -> account_stuck_alert
- recommend_next_action(account, stage, playbook) -> next_best_action
- assess_readiness(engagement, scoring_model) -> account_readiness_assessment

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Marketing automation engagement API
- CRM API (activity data)
- Email engagement API
- Ad engagement API
- Web behavior analytics API
- ABM progression playbooks store

**KPIs & Metrics:**
- abm_to_sdr_handoff_timing_accuracy: target >85%
- account_stuck_detection_rate: target >90%
- next_action_recommendation_acceptance: target >70%
- progression_tracking_coverage: target >95% of ABM accounts

**Performance Score:**
- **Red (<70):** handoff timing accuracy <65% or stuck detection <70% — escalate to ABM director
- **Amber (70-85):** accuracy 65–85% or detection 70–90% — semi-autonomous with SDR input
- **Green (>85):** accuracy >85% and detection >90% — fully autonomous progression tracking

**Feedback Loop:**
Human corrections (wrong stage assignment, missed stagnation) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

### Division 15: PROCUREMENT/LEGAL TEAM

These agents handle contract analysis, compliance, and legal support.

---

## Agent PL-001: Contract Analyst

**Division:** Procurement/Legal Team
**Primary Function:** Analyzes contracts for key terms, obligations, risks, and deviations from standard language.
**Triggers:**
- contract_received_from_buyer
- contract_generated_for_review
- enewal_contract_needs_review
- contract_amendment_proposed
**Outputs:**
- contract_analysis_report - term-by-term with risk flags
- deviation_from_standard - non-standard terms highlighted
- key_terms_summary - price, term, SLA, liability, IP, termination
- isk_assessment - high/medium/low per clause
- standard_contract_comparison - side-by-side diff
- eview_priority_score - urgency of review needed
**Data Sources:** Contract document, standard terms library, acceptable terms playbook, prior contract versions
**Training Corpus:** Contract analysis best practices, IACCM contract standards, commercial contract law fundamentals, SaaS contract standards
**LLM Tier:** Complex Reasoning (Opus class) - contract analysis requires nuanced legal and business understanding
**Criticality:** P1 - important but human legal review is the fallback
**Why dedicated:** Contract analysis is a specialized document understanding task requiring legal domain knowledge.
**Prompt Pattern:** Extraction (terms and clauses) + Classification (risk level per clause) + Analysis (deviation detection)

**Business Outcome:** Reduce contract review cycle time by 60% — surface critical legal and business risks in every contract clause with automated risk classification and deviation detection against standard playbook.

**Functions (Detailed):**
- classify_risk(clause_text, clause_type) -> risk_level_per_clause
- detect_deviation(clause, playbook_standard) -> deviation_detail
- extract_terms(document) -> extracted_terms
- generate_findings(extracted_terms) -> risk_findings_report
- prioritize(report, deal_value) -> prioritized_review_list
- summarize(distribution) -> contract_risk_summary

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- Contract playbook database
- CRM deal data (contract terms)
- Document parsing API
- CLM system API

**KPIs & Metrics:**
- risk_classification_accuracy_vs_legal_review: target >90%
- contract_review_cycle_reduction: target >60%
- deviation_detection_recall: target >95%
- critical_risk_false_negative_rate: target <2%

**Performance Score:**
- **Red (<70):** accuracy <70% or recall <80% — escalate to legal team
- **Amber (70-85):** accuracy 70–90% or recall 80–95% — semi-autonomous with legal counsel review
- **Green (>85):** accuracy >90% and recall >95% — fully autonomous contract analysis

**Feedback Loop:**
Human corrections (missed risks, wrong classifications) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent PL-002: Redline Reviewer

**Division:** Procurement/Legal Team
**Primary Function:** Reviews and classifies buyer redlines to standard contracts.
**Triggers:**
- edlines_received_from_buyer_legal
- edlines_received_from_procurement
- edline_discrepancy_detected
**Outputs:**
- edline_classification - acceptable, needs business approval, unacceptable
- edline_impact_assessment - business and legal impact per change
- counter_proposal_language - alternative language
- edline_negotiation_guidance - must-have vs nice-to-have positions
- legal_escalation_recommendation - when lawyer needed
- edline_summary_for_business - executive summary of changes
**Data Sources:** Redlined contract, standard terms database, acceptable terms playbook, legal escalation matrix, prior redline history
**Training Corpus:** Contract redlining conventions, SaaS MSA standards (IACCM), legal negotiation patterns
**LLM Tier:** Complex Reasoning (Opus class) - redline review requires understanding legal implications of each change
**Criticality:** P1 - accelerates legal review significantly
**Why dedicated:** Redline review is a specialized document comparison task distinct from contract analysis.
**Prompt Pattern:** Classification (redline acceptability) + Generation (counter language) + Analysis (impact)

---

## Agent PL-003: Compliance Checker

**Division:** Procurement/Legal Team
**Primary Function:** Checks contracts and deals against regulatory, policy, and compliance requirements.
**Triggers:**
- contract_ready_for_compliance_check
- deal_value_above_compliance_threshold
- industry_regulation_applies - healthcare, finance, government
- export_control_concern - cross-border deal
- data_privacy_requirement - GDPR, CCPA implications
**Outputs:**
- compliance_checklist_result - passed/failed per requirement
- egulatory_risk_flags - identified compliance issues
- equired_modifications - changes needed for compliance
- compliance_documentation - evidence for auditors
- exemption_or_exception_routing - when compliance can be waived
- compliance_certificate_readiness - is certification documentation complete
**Data Sources:** Regulatory database, compliance policy documents, deal data, contract terms, buyer geography/industry, product capabilities
**Training Corpus:** GDPR, CCPA, SOC2, HIPAA, ISO 27001, export control regulations, industry-specific compliance (FDA, FINRA)
**LLM Tier:** Complex Reasoning (Opus class) - compliance checking requires applying regulatory rules to specific deal context
**Criticality:** P0 - non-compliance can result in legal liability
**Why dedicated:** Compliance checking requires specialized regulatory knowledge distinct from general contract analysis.
**Prompt Pattern:** Classification (compliance pass/fail) + RAG (regulation retrieval) + Generation (modifications)

---

## Agent PL-004: Negotiation Support Document Generator

**Division:** Procurement/Legal Team
**Primary Function:** Generates supporting documents needed during legal/procurement negotiations.
**Triggers:**
- 
egotiation_requires_support_documents
- uyer_requests_additional_documentation
- procurement_asks_for_certification
- data_privacy_questionnaire_received
**Outputs:**
- data_processing_agreement - DPA tailored to deal
- usiness_associate_agreement - HIPAA BAA if needed
- information_security_addendum
- data_privacy_questionnaire_response
- service_level_agreement_schedule
- subprocessor_list
- certification_documents - SOC2, ISO, etc summaries
**Data Sources:** Standard document templates, deal-specific data, product/security documentation, legal policies, buyer requirements
**Training Corpus:** Legal document drafting, DPA and BAA standards, SOC2/ISO certification documentation, SaaS legal documentation
**LLM Tier:** Moderate (Sonnet class) - document generation from templates with deal-specific filling
**Criticality:** P1 - needed for many enterprise deals but templates can be filled manually
**Why dedicated:** Support document generation is a template-filling task distinct from the analysis work of other PL agents.
**Prompt Pattern:** Generation (document from template) + RAG (policy and certification data)

---

## Agent PL-005: E-Signature Automation Agent

**Division:** Procurement/Legal Team
**Primary Function:** Manages the e-signature workflow from contract finalization to executed document.
**Triggers:**
- contract_finalized_for_signature
- esignature_envelope_sent
- signer_completed - partial signing
- ll_signatures_complete
- envelope_expired
- signer_reminder_needed
**Outputs:**
- esignature_envelope_created - with signing order and roles
- signing_reminder_sent - automated nudge
- signing_completion_notification - executed document available
- executed_contract_stored - archival confirmation
- signing_workflow_status - who has signed, who remains
- signing_delay_alert - envelope stalled
- signing_analytics - time-to-sign metrics
**Data Sources:** Contract document, signer list and order, e-signature platform API (DocuSign, Adobe Sign), CRM deal data
**Training Corpus:** E-signature workflow best practices (DocuSign, Adobe Sign), contract execution lifecycle
**LLM Tier:** Simple (Haiku class) - primarily API orchestration with state tracking
**Criticality:** P1 - important for efficiency but manual sending is possible
**Why dedicated:** E-signature automation is a workflow orchestration task distinct from document analysis or generation.
**Prompt Pattern:** Routing (signing order) + State tracking (workflow management)

---

## Agent PL-006: Terms Comparison Agent

**Division:** Procurement/Legal Team
**Primary Function:** Compares contract terms across multiple versions, vendors, or standard templates.
**Triggers:**
- multiple_contract_versions_to_compare
- competitive_contract_comparison_needed
- standard_terms_updated - compare old vs new
- uyer_counter_received - compare to previous version
- enewal_contract_received - compare to original
**Outputs:**
- 	erms_comparison_matrix - side-by-side per term
- ersion_diff_report - what changed between versions
- competitive_terms_analysis - our terms vs competitor standard
- avorable_vs_unfavorable_changes - directional assessment
- 	erms_evolution_timeline - how terms changed over negotiation
- comparison_highlight_summary - key differences for decision makers
**Data Sources:** Contract documents, standard terms library, competitor contract intelligence, version history, negotiation history
**Training Corpus:** Contract comparison methodology, redlining conventions, competitive contract intelligence
**LLM Tier:** Moderate (Sonnet class) - terms comparison is structured analysis with clear dimensions
**Criticality:** P2 - valuable but not critical for deal execution
**Why dedicated:** Terms comparison is a document comparison task distinct from single-document analysis or generation.
**Prompt Pattern:** Analysis (side-by-side comparison) + Extraction (changed terms) + Classification (favorable/unfavorable)

---

### Division 16: EXECUTIVE ADVISORY TEAM

These agents support C-suite engagement, board presentations, and executive relationships.

---

## Agent EA-001: C-Suite Engagement Strategist

**Division:** Executive Advisory Team
**Primary Function:** Develops executive engagement strategies for C-level stakeholders.
**Triggers:**
- c_suite_contact_identified
- executive_meeting_scheduled
- executive_sentiment_change_detected
- oard_meeting_approaching
- executive_referral_opportunity
**Outputs:**
- executive_engagement_plan - tailored approach per executive
- executive_priority_analysis - strategic initiatives, pain points
- executive_stakeholder_profile - communication style, priorities, concerns
- executive_messaging_framework - peer-level language and framing
- executive_relationship_health - engagement quality score
- executive_network_map - board, peer, and industry connections
**Data Sources:** LinkedIn, executive bios, interview transcripts, earnings calls, company strategic announcements, industry publications, conference speaking history
**Training Corpus:** C-suite selling methodologies, executive engagement (CEB, Gartner), strategic account management (SAMA), John Barrows YouTube executive engagement, CEB LinkedIn executive selling research, Gong Labs executive engagement blog, SalesHacker executive buying patterns
**LLM Tier:** Complex Reasoning (Opus class) - executive engagement requires sophisticated strategic and social reasoning
**Criticality:** P1 - critical for enterprise deals with C-suite involvement
**Why dedicated:** Executive engagement requires strategic advisory thinking at a level distinct from deal-level tactics.
**Prompt Pattern:** Analysis (executive priority inference) + Generation (engagement strategy)

**Business Outcome:** Increase executive sponsor conversion rate by 40% — deliver personalized, priority-driven engagement strategies that align with each C-suite stakeholder's business objectives and communication preferences.

**Functions (Detailed):**
- infer_priorities(executive, public_data, internal_signals) -> executive_priority_profile
- design_strategy(executive, priorities, deal_context) -> engagement_strategy
- map_stakeholders(account, executive_contacts) -> executive_stakeholder_map
- recommend_narrative(executive, strategy, messaging) -> executive_narrative_recommendation
- schedule_touchpoints(strategy, timeline) -> engagement_calendar
- measure_effectiveness(executive, engagement_history) -> engagement_effectiveness_report

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- LinkedIn API (executive data)
- CRM API (executive engagement history)
- News/market intelligence API
- Earnings call transcript API
- Meeting analysis API

**KPIs & Metrics:**
- executive_engagement_conversion_rate_lift: target >40%
- priority_inference_accuracy: target >85%
- strategy_adoption_rate: target >70%
- engagement_timeliness: target >90% within SLA windows

**Performance Score:**
- **Red (<70):** conversion lift <15% or accuracy <65% — escalate to VP Sales
- **Amber (70-85):** conversion lift 15–40% or accuracy 65–85% — semi-autonomous with AVP review
- **Green (>85):** conversion lift >40% and accuracy >85% — fully autonomous executive engagement strategy

**Feedback Loop:**
Human corrections (wrong priority inference, ineffective strategy) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent EA-002: Board Narrative Constructor

**Division:** Executive Advisory Team
**Primary Function:** Builds compelling narratives and materials for board-level presentations.
**Triggers:**
- oard_meeting_scheduled
- oard_member_request_for_update
- quarterly_board_package_due
- strategic_initiative_board_update_needed
- oard_question_received
**Outputs:**
- oard_presentation_deck - narrative-driven board deck
- oard_narrative_document - written board memo
- strategic_initiative_summary - progress and impact
- oard_qa_preparation - anticipated questions and responses
- oard_metric_dashboard - board-relevant KPIs
- oard_meeting_talking_points - executive script
- competitive_landscape_brief - for board context
**Data Sources:** Financial data, pipeline and forecast, strategic initiative status, competitive intelligence, market trends, customer metrics, product roadmap
**Training Corpus:** Board presentation best practices, investor communications, narrative structuring (Andy Raskin), strategic storytelling
**LLM Tier:** Complex Reasoning (Opus class) - board narrative requires synthesizing complex business data into compelling story
**Criticality:** P1 - board materials are high-visibility but teams can prepare manually
**Why dedicated:** Board narrative construction is a specialized executive communication task distinct from other content generation.
**Prompt Pattern:** Generation (narrative document) + Summarization (board-level condensation) + Analysis (KPI significance)

---

## Agent EA-003: Executive Briefing Agent

**Division:** Executive Advisory Team
**Primary Function:** Prepares executives for customer meetings with comprehensive briefings.
**Triggers:**
- executive_meeting_confirmed
- executive_speaking_event_upcoming
- executive_interview_or_podcast_scheduled
- customer_executive_visit_planned
**Outputs:**
- executive_briefing_document - account context, objectives, talking points
- customer_executive_profile - background, style, priorities
- meeting_objectives_and_success_criteria
- 	alking_points_aligned_to_executive_priorities
- potential_landmine_alert - sensitive topics to avoid
- ollow_up_commitments_prefill - anticipated action items
- competitive_context_for_executive
**Data Sources:** CRM deal data, meeting history, customer firmographics, executive social media, news, earnings transcripts, industry trends
**Training Corpus:** Executive briefing best practices, customer executive engagement (Gartner, CEB), strategic account management
**LLM Tier:** Moderate (Sonnet class) - briefing preparation is research synthesis with strategic framing
**Criticality:** P1 - executive time is valuable; unprepared meetings waste it
**Why dedicated:** Executive briefing is a research and preparation task with different timing than ongoing engagement strategy.
**Prompt Pattern:** RAG (account and person research) + Summarization (briefing) + Generation (talking points)

---

## Agent EA-004: Strategic Roadmap Aligner

**Division:** Executive Advisory Team
**Primary Function:** Maps our product roadmap and strategic initiatives to customer strategic priorities.
**Triggers:**
- executive_meeting_planning
- ccount_strategic_shift_detected
- product_roadmap_updated
- expansion_opportunity_at_executive_level
- executive_sponsorship_needed
**Outputs:**
- oadmap_alignment_map - our initiatives vs their priorities
- strategic_initiative_mapping - specific roadmap items to specific customer goals
- lignment_gap_analysis - priorities not addressed
- strategic_conversation_framework - how to discuss roadmap alignment
- joint_strategy_development_proposal - co-innovation opportunities
- executive_sponsorship_brief - for internal executive sponsor
**Data Sources:** Product roadmap, customer strategic plans (from discovery), industry trends, customer annual report/investor deck, partnership opportunities
**Training Corpus:** Strategic account planning (SAMA), joint business development, technology partnership frameworks, product strategy alignment
**LLM Tier:** Complex Reasoning (Opus class) - roadmap alignment requires strategic matching across complex domains
**Criticality:** P2 - valuable for deep strategic relationships but not essential for transactions
**Why dedicated:** Strategic alignment mapping requires product and customer strategy knowledge at a level distinct from deal-level planning.
**Prompt Pattern:** Analysis (alignment mapping) + Generation (strategic conversation guide) + Gap analysis

---

## Agent EA-005: Peer Networking Mapper

**Division:** Executive Advisory Team
**Primary Function:** Identifies peer connections and networking opportunities for executive sponsors and buyers.
**Triggers:**
- executive_sponsor_assigned
- uyer_executive_needs_peer_references
- industry_event_approaching
- executive_board_or_advisory_role_detected
- peer_introduction_requested
**Outputs:**
- peer_network_map - shared connections, boards, events
- peer_referral_opportunities - warm introduction chances
- industry_event_recommendations - relevant conferences
- executive_bio_for_introduction - context for warm intro
- peer_reference_candidates - customers willing to speak
- executive_community_participation - relevant groups/associations
- 
etworking_approach_recommendation - personalized strategy
**Data Sources:** LinkedIn, board member databases, event/conference data, customer reference database, industry association memberships, alumni networks
**Training Corpus:** Executive networking strategies, board placement dynamics, B2B referral frameworks, executive relationship building
**LLM Tier:** Moderate (Sonnet class) - network mapping requires graph analysis and social reasoning
**Criticality:** P2 - valuable but not essential for deal execution
**Why dedicated:** Peer networking is a relationship mapping task distinct from engagement strategy or briefing preparation.
**Prompt Pattern:** Extraction (relationship graph entities) + Analysis (network gap/opportunity) + Generation (introduction approach)

---

## Tier 3 — Strategic Enablement

---

### Division 17: PARTNER/ALLIANCE TEAM

These agents manage partner ecosystems and co-sell opportunities.

---

## Agent PA-001: Partner Identification Agent

**Division:** Partner/Alliance Team
**Primary Function:** Identifies and evaluates potential channel, technology, and strategic partners.
**Triggers:**
- 	ick_monthly - scans for potential partners
- market_adjacency_detected - company addresses adjacent need
- customer_request_for_partner - buyer asks for a specific partner
- competitive_ecosystem_change - competitor partnered, need counter
- integration_opportunity_identified by Technical Environment Mapper
**Outputs:**
- partner_candidate_profile - company, product, market fit, reach, revenue
- partner_fit_score - strategic fit, customer overlap, complementarity
- partnership_type_recommendation - referral, resell, technology, strategic
- partner_evaluation_report - strengths, weaknesses, risks
- partner_prioritization_rankings
- partner_intelligence_brief - summary for alliance team
**Data Sources:** CrunchBase, LinkedIn, G2, partner directories (PartnerStack, Impartner), customer ecosystem data, competitor partnerships
**Training Corpus:** Channel partnership evaluation, technology alliance frameworks, strategic partnership development
**LLM Tier:** Moderate (Sonnet class) - partner evaluation requires multi-dimensional fit scoring
**Criticality:** P1 - important for ecosystem growth but not critical in early stages
**Why dedicated:** Partner identification is a periodic scanning task distinct from ongoing partner management.
**Prompt Pattern:** Extraction (partner attributes) + Scoring (fit) + Classification (partnership type)

**Business Outcome:** Increase partner-sourced pipeline by 50% — continuously scan the ecosystem for high-fit partners across technology, channel, and strategic categories with automated fit scoring and partnership type classification.

**Functions (Detailed):**
- scan_partners(criteria, ecosystem_data) -> partner_candidate_candidates
- score_fit(partner_candidate, partnership_model) -> fit_score
- classify_type(partner_candidate, capabilities) -> partnership_type
- research_capabilities(partner_candidate) -> capability_profile
- assess_overlap(market, partner_candidate) -> market_overlap_assessment
- recommend_priority(candidates, scores, strategy) -> prioritized_partner_list

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- CrunchBase API
- LinkedIn API (company data)
- G2/similar market analysis API
- Partner program database
- CRM partner data

**KPIs & Metrics:**
- partner_sourced_pipeline_lift: target >50%
- fit_scoring_accuracy_vs_onboarding_outcome: target >80%
- identification_coverage: target >90% of relevant ecosystem
- false_positive_identification_rate: target <15%

**Performance Score:**
- **Red (<70):** pipeline lift <20% or accuracy <60% — escalate to Partner Director
- **Amber (70-85):** lift 20–50% or accuracy 60–80% — semi-autonomous with partner manager review
- **Green (>85):** lift >50% and accuracy >80% — fully autonomous partner identification

**Feedback Loop:**
Human corrections (wrong fit assessment, missed candidates) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent PA-002: Co-Sell Opportunity Detector

**Division:** Partner/Alliance Team
**Primary Function:** Identifies opportunities where a partner can influence, accelerate, or strengthen a deal.
**Triggers:**
- deal_enters_stage_with_partner_potential
- partner_added_to_account_team
- customer_mentions_partner_by_name
- customer_has_existing_partner_relationship
- product_requires_partner_services
- partner_incentive_program_applicable
**Outputs:**
- co_sell_opportunity_alert - deal ID, partner, opportunity type
- partner_influence_strategy - how partner helps win
- partner_introduction_recommendation - warm intro path
- partner_motivation_analysis - why partner would help
- co_sell_revenue_sharing_estimate
- deal_stage_for_partner_involvement - when to engage
- co_sell_playbook_reference - relevant play for this scenario
**Data Sources:** CRM deal data, partner relationship mapping, partner program data, customer communication transcripts, joint customer data
**Training Corpus:** Co-sell methodologies (Salesforce, Microsoft partner programs), channel sales frameworks, partner-led deal acceleration
**LLM Tier:** Moderate (Sonnet class) - co-sell detection requires matching deal attributes to partner capabilities
**Criticality:** P1 - co-sell significantly improves win rates for partner-eligible deals
**Why dedicated:** Co-sell opportunity detection requires continuous deal-level analysis distinct from partner identification.
**Prompt Pattern:** Classification (co-sell eligibility) + Generation (partner engagement strategy)

---

## Agent PA-003: Partner Enablement Agent

**Division:** Partner/Alliance Team
**Primary Function:** Generates enablement content and training materials for partner organizations.
**Triggers:**
- 
ew_partner_onboarded
- product_feature_released_impacting_partners
- competitive_landscape_change
- partner_sales_kit_needs_refresh
- partner_training_scheduled
- partner_certification_program_update
**Outputs:**
- partner_sales_deck - partner-facing pitch
- partner_battle_card - competitive positioning for partners
- partner_demo_script - tailored demo flow
- partner_training_materials - modules, assessments, certifications
- partner_faq_document - common questions and answers
- partner_market_insights - trends and opportunities for partners
- partner_enablement_calendar - training and certification schedule
**Data Sources:** Product documentation, competitive intelligence, sales playbooks, marketing materials, partner program requirements
**Training Corpus:** Partner enablement best practices (PartnerStack, Impartner), channel training methodologies, partner program design
**LLM Tier:** Moderate (Sonnet class) - enablement content follows structured formats
**Criticality:** P2 - important for partner productivity but not critical
**Why dedicated:** Partner enablement is a content generation task for a different audience than direct sales content.
**Prompt Pattern:** Generation (training materials) + RAG (product and competitive knowledge)

---

## Agent PA-004: Joint Value Proposition Builder

**Division:** Partner/Alliance Team
**Primary Function:** Crafts joint value propositions and messaging for our products combined with partner products.
**Triggers:**
- partnership_formalized
- joint_go_to_market_planning
- partner_co_marketing_campaign
- joint_customer_case_study_needed
- joint_offering_launch
**Outputs:**
- joint_value_proposition - combined solution messaging
- partner_differentiation_statement - how we win together
- integrated_solution_use_cases - specific scenarios
- joint_roi_calculator_inputs - value levers for combined solution
- joint_competitive_positioning - vs alternative combinations
- partner_messaging_alignment_check - consistency check
- co_branded_assets_outline - content to create together
**Data Sources:** Our product capabilities, partner product capabilities, joint customer data, market need analysis, competitive intelligence
**Training Corpus:** Joint value proposition development, co-marketing frameworks, integrated solution marketing
**LLM Tier:** Complex Reasoning (Opus class) - joint value propositions require deep understanding of both products' capabilities
**Criticality:** P2 - valuable for partner-led growth but not deal-blocking
**Why dedicated:** Joint value proposition requires product knowledge across two organizations, distinct from single-vendor messaging.
**Prompt Pattern:** Generation (joint messaging) + Analysis (competitive positioning for combined offering)

---

## Agent PA-005: Partner Performance Tracker

**Division:** Partner/Alliance Team
**Primary Function:** Tracks and analyzes partner performance metrics.
**Triggers:**
- 	ick_monthly - performance review
- partner_deal_registered
- partner_deal_won_or_lost
- partner_quarterly_review_due
- partner_tier_change - promotion or demotion
- partner_coverage_gap_detected
**Outputs:**
- partner_performance_scorecard - metrics per partner
- partner_pipeline_report - influenced and sourced pipeline
- partner_conversion_metrics - registration to close rates
- partner_segment_performance - by region, product, segment
- partner_tier_recommendation - promotion or demotion
- partner_gap_analysis - underperforming partners
- partner_program_effectiveness - overall program ROI
- partner_coaching_recommendations - specific improvements
**Data Sources:** Partner CRM, deal registration data, partner program data, revenue data by partner, partner satisfaction surveys
**Training Corpus:** Partner program management, channel performance metrics, partner scorecard frameworks
**LLM Tier:** Simple (Haiku class) - primarily numeric metric computation
**Criticality:** P2 - important for program optimization
**Why dedicated:** Partner performance tracking is a metrics computation task distinct from partner relationship or enablement work.
**Prompt Pattern:** Scoring (performance metrics) + Classification (tier recommendation)

---

### Division 18: SECURITY/COMPLIANCE TEAM

These agents handle security questionnaires, compliance documentation, and vendor risk assessment.

---

## Agent SC-001: Security Questionnaire Auto-Fill

**Division:** Security/Compliance Team
**Primary Function:** Automatically fills security questionnaires using the knowledge base of standard responses.
**Triggers:**
- security_questionnaire_received
- uyer_requests_security_documentation
- endor_risk_assessment_initiated
- procurement_sends_security_survey
**Outputs:**
- completed_questionnaire - filled document with evidence references
- unanswered_questions_report - questions requiring human input
- question_classification - standard, needs review, out of scope
- evidence_attachment_package - supporting documentation
- esponse_confidence_score - per-question confidence
- questionnaire_completion_status - progress tracking
- questionnaire_history_for_this_buyer - past responses
**Data Sources:** Security documentation library, policy documents, SOC2/ISO certifications, past questionnaire responses, product security specs, infrastructure documentation
**Training Corpus:** Security questionnaire standards (CAIQ, SIG, VSA), SOC2/ISO certification requirements, cloud security frameworks (CSA STAR, NIST)
**LLM Tier:** Moderate (Sonnet class) - questionnaire responses require matching questions to documented answers
**Criticality:** P0 - security questionnaires are mandatory for enterprise deals
**Why dedicated:** Questionnaire auto-fill is a RAG-intensive task requiring a specialized knowledge base distinct from other agents.
**Prompt Pattern:** RAG (answer retrieval) + Classification (question type) + Generation (tailored response)

**Business Outcome:** Reduce security questionnaire response time by 80% — auto-fill enterprise security questionnaires with 95%+ accuracy, eliminating manual research and enabling sales to respond to security requests within hours instead of days.

**Functions (Detailed):**
- retrieve_answer(question, knowledge_base) -> relevant_answer_candidates
- classify_question(question, taxonomy) -> question_type
- generate_response(question, answer_candidates, context) -> tailored_response
- verify_compliance(response, policy_database) -> compliance_verification_flag
- check_completeness(questionnaire) -> completeness_gap_report
- prioritize_gaps(gaps, deadline) -> gap_prioritization

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Sonnet-class)
- Security knowledge base (RAG store)
- Policy and certification document store
- Product documentation store
- Previous response database
- SOC2/ISO/HIPAA certification repository

**KPIs & Metrics:**
- questionnaire_response_time_reduction: target >80%
- answer_accuracy_vs_human_review: target >95%
- incomplete_response_rate: target <5%
- rework_due_to_inaccuracy: target <3%

**Performance Score:**
- **Red (<70):** response reduction <40% or accuracy <80% — escalate to Security team
- **Amber (70-85):** reduction 40–80% or accuracy 80–95% — semi-autonomous with security engineer review
- **Green (>85):** reduction >80% and accuracy >95% — fully autonomous questionnaire response

**Feedback Loop:**
Human corrections (wrong answers, missing responses) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >15% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent SC-002: Compliance Matrix Generator

**Division:** Security/Compliance Team
**Primary Function:** Generates compliance requirement matrices mapping regulations to controls.
**Triggers:**
- 
ew_compliance_standard_to_map
- uyer_requests_compliance_matrix
- egulatory_update_published
- udit_preparation_started
- product_feature_affects_compliance_posture
**Outputs:**
- compliance_matrix - regulation x control mapping
- gap_analysis_report - controls not meeting requirements
- emediation_recommendations - actions to close gaps
- compliance_coverage_percentage - how compliant we are
- control_evidence_catalog - evidence per control
- pplicable_regulations - which regs apply to this deal
- compliance_roadmap - timeline to full compliance
**Data Sources:** Regulatory text, compliance policy framework, control documentation, audit evidence repository, product architecture docs
**Training Corpus:** SOC2, ISO 27001, HIPAA, GDPR, PCI-DSS, FedRAMP, NIST CSF, SOX compliance frameworks
**LLM Tier:** Complex Reasoning (Opus class) - compliance mapping requires interpreting regulatory requirements and mapping to specific controls
**Criticality:** P1 - important for regulated industries
**Why dedicated:** Compliance matrix generation is a systematic mapping task requiring specialized regulatory knowledge.
**Prompt Pattern:** Analysis (regulation to control mapping) + Generation (gap assessment) + Classification (compliance status)

---

## Agent SC-003: SOC2/ISO Readiness Assessor

**Division:** Security/Compliance Team
**Primary Function:** Assesses organizational readiness for SOC2, ISO 27001, and other certifications.
**Triggers:**
- certification_audit_scheduled
- pre_audit_assessment_requested
- control_failure_detected
- quarterly_readiness_review
- 
ew_product_or_service_launched
**Outputs:**
- eadiness_assessment_report - per-control readiness status
- control_strength_score - how well each control operates
- gap_analysis - controls not meeting certification thresholds
- emediation_priority_list - critical gaps ranked
- evidence_readiness_check - is evidence audit-ready
- udit_simulation_results - predicted audit outcome
- eadiness_timeline - projected ready date
**Data Sources:** Control documentation, evidence repository, policy library, past audit findings, incident reports, system configuration data
**Training Corpus:** SOC2 trust services criteria, ISO 27001 Annex A controls, audit readiness best practices (AICPA, ISO)
**LLM Tier:** Complex Reasoning (Opus class) - readiness assessment requires holistic control environment evaluation
**Criticality:** P1 - certifications are table stakes for enterprise deals
**Why dedicated:** Readiness assessment requires audit methodology knowledge distinct from questionnaire filling or compliance matrix generation.
**Prompt Pattern:** Analysis (control strength evaluation) + Classification (readiness status) + Generation (remediation plan)

---

## Agent SC-004: Data Privacy Checker

**Division:** Security/Compliance Team
**Primary Function:** Checks deals for data privacy compliance requirements.
**Triggers:**
- deal_involves_eu_personally_identifiable_information
- deal_involves_california_residents
- health_data_mentioned_in_deal
- cross_border_data_transfer_detected
- 
ew_privacy_regulation_effective
- privacy_impact_assessment_needed
**Outputs:**
- privacy_requirement_checklist - applicable regulations
- data_classification_for_deal - what data types are involved
- privacy_risk_assessment - risk level with justification
- equired_privacy_controls - specific measures needed
- dpa_or_baa_requirement_flag - additional agreements needed
- data_residency_requirement - storage location requirements
- privacy_impact_assessment_summary
- privacy_compliance_certificate - for buyer confidence
**Data Sources:** Deal data, buyer geography, product data handling documentation, DPA templates, regulatory database, data classification policy
**Training Corpus:** GDPR (EU), CCPA/CPRA (California), LGPD (Brazil), PIPEDA (Canada), data protection principles, privacy by design frameworks
**LLM Tier:** Complex Reasoning (Opus class) - privacy assessment requires applying complex regulations to specific deal contexts
**Criticality:** P0 - privacy violations carry significant legal liability
**Why dedicated:** Data privacy checking requires specialized regulatory knowledge distinct from general compliance.
**Prompt Pattern:** Classification (applicable regulations) + Analysis (risk assessment) + Generation (required controls)

---

## Agent SC-005: Vendor Risk Assessment Agent

**Division:** Security/Compliance Team
**Primary Function:** Assesses risks of third-party vendors and subprocessors.
**Triggers:**
- 
ew_vendor_or_subprocessor_engaged
- endor_renewal_review_due
- endor_security_incident_reported
- endor_questionnaire_response_received
- endor_tier_change
**Outputs:**
- endor_risk_score - composite risk rating
- endor_security_posture_report - controls assessment
- endor_questionnaire_analysis - strength of responses
- endor_remediation_requirements - conditions for engagement
- endor_due_diligence_checklist - completed steps
- endor_risk_comparison - vs industry peers
- endor_monitoring_plan - ongoing oversight
- endor_approval_recommendation - approved, conditional, rejected
**Data Sources:** Vendor security questionnaires, SOC2/ISO reports, vendor penetration test results, breach databases, vendor business health data
**Training Corpus:** Vendor risk management frameworks (NIST, SIG), third-party security assessment, supply chain risk management
**LLM Tier:** Moderate (Sonnet class) - vendor risk assessment requires evidence evaluation
**Criticality:** P1 - important for enterprise deals requiring subprocessor review
**Why dedicated:** Vendor risk assessment is a third-party evaluation task distinct from internal compliance or privacy checking.
**Prompt Pattern:** Analysis (risk evidence evaluation) + Scoring (composite risk) + Classification (approval recommendation)

---

### Division 19: DELIVERY CONFIDENCE TEAM

These agents assess implementation feasibility and manage deployment risk.

---

## Agent DLC-001: Implementation Risk Assessor

**Division:** Delivery Confidence Team
**Primary Function:** Assesses implementation risks for each deal based on complexity, dependencies, and readiness.
**Triggers:**
- deal_reaches_technical_review_stage
- 	echnical_environment_map_completed
- implementation_milestone_defined
- complex_integration_identified
- esource_constraint_detected
**Outputs:**
- implementation_risk_score - composite risk rating
- isk_register - identified risks with severity and probability
- critical_risk_alerts - deal-blocking implementation risks
- isk_mitigation_recommendations - specific actions
- implementation_complexity_assessment - simple/moderate/complex
- historical_comparison - similar implementations and outcomes
- implementation_confidence_score - likelihood of successful delivery
**Data Sources:** Technical environment map, integration requirements, resource capacity data, historical implementation data, product specifications, timeline constraints
**Training Corpus:** Implementation risk management (PMI), enterprise software deployment patterns, professional services risk assessment
**LLM Tier:** Complex Reasoning (Opus class) - risk assessment requires probabilistic reasoning across multiple dimensions
**Criticality:** P1 - important for managing delivery expectations
**Why dedicated:** Implementation risk assessment requires project management expertise distinct from technical discovery.
**Prompt Pattern:** Analysis (risk identification and assessment) + Scoring (probability/impact)

**Business Outcome:** Reduce implementation delays by 50% — identify and score implementation risks before they materialize, enabling proactive mitigation and accurate delivery timeline commitments at deal stage.

**Functions (Detailed):**
- identify_risks(deal_data, implementation_context) -> implementation_risk_list
- score_probability(risk, historical_data) -> risk_probability_score
- score_impact(risk, deal_scope) -> risk_impact_score
- prioritize_risks(risks, thresholds) -> risk_priority_matrix
- recommend_mitigation(risk, playbook) -> mitigation_recommendation
- track_mitigation_status(milestones, action_items) -> mitigation_tracking_dashboard

**Tools/APIs:**
- NATS JetStream (pub/sub for events)
- LLM inference API (Opus-class)
- Historical implementation data store
- Project management API
- CRM deal data
- Technical scoping documents
- Resource availability API
- Customer readiness data

**KPIs & Metrics:**
- implementation_delay_reduction: target >50%
- risk_identification_accuracy: target >85%
- early_warning_lead_time: target >30 days before go-live
- mitigation_effectiveness_rate: target >70%

**Performance Score:**
- **Red (<70):** delay reduction <20% or identification accuracy <65% — escalate to Delivery Director
- **Amber (70-85):** reduction 20–50% or accuracy 65–85% — semi-autonomous with PM review
- **Green (>85):** reduction >50% and accuracy >85% — fully autonomous risk assessment

**Feedback Loop:**
Human corrections (missed risks, wrong scoring) logged → KL-005 weekly batch retrain → agent retrained. Override trigger: >20% correction rate triggers AIG-002 optimization. Monthly audit by AIG-001.

---

## Agent DLC-002: Timeline Estimator

**Division:** Delivery Confidence Team
**Primary Function:** Generates implementation timeline estimates based on scope, complexity, and resource availability.
**Triggers:**
- deal_requires_implementation_timeline
- scope_of_work_defined
- esource_constraint_identified
- dependency_map_completed
- implementation_start_date_set
**Outputs:**
- implementation_timeline_estimate - phased timeline with milestones
- critical_path_analysis - longest dependency chain
- esource_loading_plan - who works on what when
- 	imeline_contingency_buffer - risk-adjusted timeline
- parallel_vs_sequential_task_analysis - optimization
- 	imeline_confidence_range - optimistic/pessimistic estimates
- cceleration_possibilities - what could shorten timeline
- 	imeline_dependency_alert - external dependencies affecting schedule
**Data Sources:** Scope of work, technical environment data, resource capacity, historical implementation timelines, dependency map, product release calendar
**Training Corpus:** Project estimation methodologies (PMP, Agile, critical chain), professional services delivery, software implementation patterns
**LLM Tier:** Moderate (Sonnet class) - timeline estimation follows structured project planning methodology
**Criticality:** P1 - timeline commitments directly affect deal closure
**Why dedicated:** Timeline estimation is a project planning task distinct from risk assessment or technical discovery.
**Prompt Pattern:** Analysis (task dependency and duration) + Generation (timeline plan) + Scoring (confidence)

---

## Agent DLC-003: Resource Planner

**Division:** Delivery Confidence Team
**Primary Function:** Plans resource allocation for implementations based on skills, availability, and deal requirements.
**Triggers:**
- implementation_team_needed
- esource_conflict_detected
- skill_gap_identified_for_implementation
- 
ew_implementation_starting
- esource_availability_changed
**Outputs:**
- esource_plan - who, what, when for implementation
- skill_gap_analysis - missing skills on team
- esource_conflict_alert - over-allocated resources
- hiring_or_contractor_recommendation - if gap exists
- esource_cost_estimate - implementation labor cost
- 	eam_loading_report - utilization across projects
- esource_plan_scenario - what-if with different team compositions
**Data Sources:** Resource skill database, availability calendar, project scope, skills required per implementation type, budget data, contractor rates
**Training Corpus:** Professional services resource management, staffing optimization, project resource planning (PSA tools)
**LLM Tier:** Moderate (Sonnet class) - resource planning is optimization with constraints
**Criticality:** P1 - poor resource planning causes implementation delays
**Why dedicated:** Resource planning is an optimization task distinct from timeline estimation or risk assessment.
**Prompt Pattern:** Analysis (skill matching) + Optimization (resource allocation) + Generation (plan)

---

## Agent DLC-004: Dependency Mapper

**Division:** Delivery Confidence Team
**Primary Function:** Maps all dependencies required for successful implementation.
**Triggers:**
- scope_of_work_finalized
- integration_identified_in_technical_map
- 	hird_party_service_needed
- customer_prerequisite_identified
- go_live_criteria_defined
**Outputs:**
- dependency_graph - visualizable dependency network
- critical_dependencies_list - must-have prerequisites
- dependency_status_tracker - completed, in progress, blocked
- dependency_owner_assignment - who is responsible per dependency
- dependency_risk_assessment - likelihood of each dependency failing
- external_dependency_alert - dependencies outside our control
- dependency_completion_forecast - expected completion dates
**Data Sources:** Scope of work, technical environment map, integration specifications, third-party documentation, customer readiness data, resource plan
**Training Corpus:** Dependency management (PMI, critical path method), enterprise integration patterns, project dependency mapping
**LLM Tier:** Moderate (Sonnet class) - dependency mapping follows graph structure patterns
**Criticality:** P1 - unmanaged dependencies cause implementation failures
**Why dedicated:** Dependency mapping is a graph construction task distinct from other delivery planning functions.
**Prompt Pattern:** Extraction (dependency relationships) + Analysis (critical path) + Classification (status)

---

## Agent DLC-005: Go-Live Readiness Assessor

**Division:** Delivery Confidence Team
**Primary Function:** Assesses whether the customer and our team are ready for go-live.
**Triggers:**
- go_live_date_approaching - T-30, T-14, T-7
- go_live_checklist_item_completed
- go_live_blocker_identified
- cutover_plan_drafting
- customer_readiness_check_needed
**Outputs:**
- go_live_readiness_score - composite readiness assessment
- go_live_checklist_status - per-item completion
- locker_log - items preventing go-live
- ollback_criteria - when to abort go-live
- go_live_go_no_go_recommendation - proceed or delay
- cutover_plan_support_document - step-by-step cutover
- post_go_live_support_requirements
**Data Sources:** Implementation milestone status, dependency completion, testing results, customer training completion, integration test results, resource availability
**Training Corpus:** Go-live readiness assessment, cutover management, enterprise deployment best practices, release management (ITIL)
**LLM Tier:** Moderate (Sonnet class) - readiness assessment follows structured checklist methodology
**Criticality:** P1 - prevents failed go-lives
**Why dedicated:** Go-live readiness is a milestone-specific assessment task distinct from ongoing implementation planning.
**Prompt Pattern:** Scoring (readiness dimensions) + Classification (go/no-go) + Generation (checklist)

---

## Agent DLC-006: Hypercare Planner

**Division:** Delivery Confidence Team
**Primary Function:** Plans the post-launch hypercare period to ensure smooth transition to ongoing operations.
**Triggers:**
- go_live_date_within_14_days
- hypercare_plan_needed
- support_handoff_planning
- known_issues_to_monitor_during_hypercare
- customer_staff_readiness_concern
**Outputs:**
- hypercare_plan - schedule, team, escalation, success criteria
- hypercare_team_roster - who is on call
- monitoring_dashboard_requirements - what to watch
- escalation_pathway_document - who to contact for what
- known_issues_watchlist - items requiring close monitoring
- hypercare_success_criteria - when hypercare ends
- hypercare_daily_standup_agenda
- 	ransition_to_bau_plan - handoff to support
**Data Sources:** Implementation documentation, known issues log, support team capacity, customer contacts, escalation playbooks, monitoring tools
**Training Corpus:** Hypercare best practices, ITIL transition planning, professional services handoff processes
**LLM Tier:** Moderate (Sonnet class) - hypercare planning follows operational playbook structure
**Criticality:** P2 - valuable for smooth transitions but teams can plan manually
**Why dedicated:** Hypercare planning is an operational planning task distinct from implementation planning.
**Prompt Pattern:** Generation (operational plan) + Routing (escalation paths) + Analysis (risk monitoring)

---

### Division 20: RFP/RFQ TEAM

These agents handle request for proposal and request for quotation processes.

---

## Agent RFP-001: RFP Decomposition Agent

**Division:** RFP/RFQ Team
**Primary Function:** Decomposes RFP documents into structured requirements, questions, and response items.
**Triggers:**
- fp_document_received
- fp_rfi_or_rfq_uploaded
- uyer_sends_requirements_document
- 	ender_document_published
**Outputs:**
- fp_requirements_extract - structured requirement list
- fp_question_catalog - all questions needing answers
- fp_requirement_classification - mandatory vs desirable vs optional
- fp_scoring_criteria_analysis - how responses will be evaluated
- fp_complexity_assessment - simple/moderate/complex
- fp_win_themes_extraction - buyer's stated priorities
- fp_deadline_and_constraints - timeline, page limits, formatting
- fp_question_assignment - which agent/person answers what
**Data Sources:** RFP document, buyer history, industry tender data, RFP response templates
**Training Corpus:** RFP response management (RFPIO, Loopio), government procurement frameworks, tender writing best practices
**LLM Tier:** Complex Reasoning (Opus class) - RFP decomposition requires understanding nuanced procurement language
**Criticality:** P0 - RFPs are mandatory for deal pursuit in B2B enterprise
**Why dedicated:** RFP decomposition is the upstream intake task that enables all downstream RFP response agents.
**Ownership Boundary:** RFP/RFQ Team owns all RFP responses; RFP-001 produces structured extracts but final response content and submission require RFP/RFQ Team approval. Does not auto-submit.
**Prompt Pattern:** Extraction (requirements from text) + Classification (mandatory/optional) + Analysis (scoring criteria)

**Business Outcome:** Achieve >95% RFP requirement capture accuracy and reduce decomposition cycle time by 60%, enabling faster bid/no-bid decisions with fewer missed mandatory requirements.

**Functions (Detailed):**
- decompose_rfp_document(pdf/docx) -> structured_requirement_list
- classify_requirement(requirement_text) -> mandatory|desirable|optional
- extract_scoring_criteria(rfp_document) -> evaluation_weightings
- assign_question_owner(question, agent_registry) -> agent_id
- assess_rfp_complexity(requirement_count, technical_depth) -> simple|moderate|complex
- extract_win_themes(rfp_document, buyer_history) -> priority_themes

**Tools/APIs:**
- NATS JetStream (pub/sub for agent events)
- LLM inference API (Opus class)
- RFP library KV store (past RFP responses and templates)
- Compliance rules store (mandatory requirement database)
- Proposal template DB (response formatting standards)
- Document parsing API (PDF, DOCX extraction)

**KPIs & Metrics:**
- requirement_extraction_recall: target >95%
- requirement_classification_accuracy: target >90%
- decomposition_turnaround_time: target <30min
- missed_mandatory_requirement_rate: target <2%
- win_theme_accuracy: target >85%

**Performance Score:**
- **Red (<70):** Extraction recall below 85% or missed mandatory requirements >5% — escalation to AIG-001 for root cause analysis and prompt retraining
- **Amber (70-85):** Recall 85-95% with minor classification errors — acceptable with monitoring; review edge cases weekly
- **Green (>85):** All metrics at or above target with zero missed mandatory requirements — fully autonomous operation

**Feedback Loop:**
Human corrections to requirement classifications logged → KL-005 weekly batch retrain on corrected extraction patterns → agent retrained on new RFP document formats. Override trigger: >15% classification errors on any single RFP (P0) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent RFP-002: Response Content Generator

**Division:** RFP/RFQ Team
**Primary Function:** Generates response content for each RFP question using the knowledge base.
**Triggers:**
- fp_question_assigned_for_response
- fp_question_needs_update_for_new_product_version
- fp_section_with_standard_content
**Outputs:**
- fp_question_response - tailored answer per question
- fp_exclusion_recommendation - questions not to answer
- fp_reference_content - source material for the answer
- fp_response_draft_section - complete section of the RFP
- fp_confidence_score_per_question - how confident in the answer
- fp_compliance_flag - requirements we cannot meet
- fp_differentiation_opportunity - questions to emphasize strengths
**Data Sources:** RFP response library, product documentation, case studies, technical specs, competitive intelligence, past RFP responses
**Training Corpus:** RFP response writing (RFPIO, Loopio, Responsive.io), persuasive technical writing, compliance response frameworks
**LLM Tier:** Complex Reasoning (Opus class) - RFP responses require persuasive yet factual writing with compliance awareness
**Criticality:** P0 - RFP responses directly determine win/loss
**Why dedicated:** RFP response generation requires retrieval-augmented generation at scale with compliance cross-checking.
**Prompt Pattern:** RAG (retrieve best response) + Generation (tailored answer) + Classification (compliance check)

**Business Outcome:** Achieve >90% first-pass RFP response accuracy and reduce response generation time by 70%, enabling coverage of 3x more RFP opportunities with consistent compliance-aware content.

**Functions (Detailed):**
- generate_question_response(question, knowledge_base) -> answer_text
- retrieve_best_response(question, response_library) -> candidate_answer
- check_compliance(response, requirement) -> compliant|non_compliant
- flag_compliance_gap(question, product_capabilities) -> gap_report
- suggest_differentiation_angle(question, competitive_data) -> emphasis_point
- score_response_confidence(response, evidence) -> confidence_percentage

**Tools/APIs:**
- NATS JetStream (pub/sub for agent events)
- LLM inference API (Opus class)
- RFP response library KV (past approved answers)
- Product capabilities database (feature-to-requirement mapping)
- Case study library (evidence references)
- Compliance rules store (mandatory requirement enforcement)

**KPIs & Metrics:**
- response_accuracy: target >90%
- response_generation_time_per_question: target <5min
- compliance_flag_precision: target >95%
- differentiation_opportunity_capture_rate: target >80%
- human_revision_rate: target <15%

**Performance Score:**
- **Red (<70):** Response accuracy below 80% or human revision rate >25% — escalation to AIG-001 for prompt retraining and knowledge base review
- **Amber (70-85):** Accuracy 80-90% with minor factual errors — acceptable with QA review; flag for KL-005 weekly retrain
- **Green (>85):** Accuracy at target with <10% human revision — fully autonomous generation; responses auto-approved for standard sections

**Feedback Loop:**
Human revisions to generated responses logged → KL-005 weekly batch retrain on correction patterns → response library updated with validated answers. Override trigger: >20% non-compliance flags (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent RFP-003: Compliance Status Checker

**Division:** RFP/RFQ Team
**Primary Function:** Checks each RFP requirement against our product capabilities for compliance gaps.
**Triggers:**
- fp_requirement_catalog_completed
- fp_mandatory_requirement_identified
- fp_compliance_matrix_needed
- fp_bid_no_bid_decision_in_progress
**Outputs:**
- fp_compliance_matrix - requirement by compliance status
- fp_gap_analysis - requirements we partially or cannot meet
- fp_compliance_percentage - overall compliance score
- fp_mitigation_strategy - how to address gaps
- fp_waiver_or_exception_requests - questions to raise
- fp_competitive_exposure_analysis - gaps competitors exploit
- fp_partner_solution_recommendation - partner fills the gap
- fp_bid_confidence_score - compliance-adjusted win probability
**Data Sources:** RFP requirements, product capabilities database, partner solution catalog, compliance documentation, competitive landscape
**Training Corpus:** Compliance assessment frameworks, gap analysis methodology, RFP compliance best practices
**LLM Tier:** Complex Reasoning (Opus class) - compliance checking requires nuanced interpretation of requirements vs capabilities
**Criticality:** P0 - compliance gaps determine bid/no-bid decisions
**Why dedicated:** Compliance checking is a systematic verification task distinct from response content generation.
**Prompt Pattern:** Analysis (requirement vs capability match) + Classification (compliant/gap/missing) + Generation (mitigation strategy)

**Business Outcome:** Achieve >99% RFP compliance accuracy, detect all compliance gaps before bid submission, and increase bid compliance score by 25% through proactive gap mitigation.

**Functions (Detailed):**
- check_requirement_compliance(requirement, product_capabilities) -> compliant|partial|gap
- compute_compliance_matrix(requirements_list, capabilities) -> compliance_percentage
- identify_mitigation_strategy(gap, partner_catalog) -> fill_strategy
- flag_competitive_exposure(gap, competitive_data) -> risk_assessment
- recommend_partner_fill(gap, partner_solutions) -> partner_recommendation
- generate_compliance_report(matrix, mitigations) -> formatted_report

**Tools/APIs:**
- NATS JetStream (pub/sub for agent events)
- LLM inference API (Opus class)
- Product capabilities database (feature-to-requirement mapping)
- RFP requirement catalog KV
- Partner solution catalog DB
- Compliance documentation store (certifications, policies)

**KPIs & Metrics:**
- compliance_check_accuracy: target >99%
- gap_detection_recall: target >98%
- false_positive_compliance_flag: target <3%
- mitigation_strategy_effectiveness: target >85%
- compliance_check_turnaround: target <15min per RFP

**Performance Score:**
- **Red (<70):** Compliance accuracy below 95% or missed critical gap on mandatory requirement — escalation to AIG-001 for full audit and AIG-002 for prompt rewrite
- **Amber (70-85):** Accuracy 95-99% with minor false flags — acceptable with human QA; weekly compliance pattern review
- **Green (>85):** Accuracy at target with zero missed mandatory gaps — fully autonomous compliance checking; auto-approves standard compliance reports

**Feedback Loop:**
Human overrides on compliance flags logged → KL-005 weekly batch retrain on requirement interpretation corrections. Override trigger: >15% false positives (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent RFP-004: Bid/No-Bid Recommender

**Division:** RFP/RFQ Team
**Primary Function:** Determines whether to pursue or skip each RFP opportunity.
**Triggers:**
- fp_decomposition_completed
- fp_win_probability_needs_assessment
- fp_compliance_check_completed
- id_decision_needed_by_deadline
- fp_evaluation_criteria_analyzed
**Outputs:**
- id_recommendation - bid, no-bid, or conditional bid
- win_probability_assessment - likelihood of winning
- id_cost_estimate - effort and cost to respond
- id_roi_analysis - expected return vs investment
- competitive_landscape_for_rfp - likely competitors
- strategic_importance_assessment - beyond this RFP value
- id_decision_package - summary for executive decision
- conditional_bid_requirements - conditions if bidding
**Data Sources:** RFP analysis, compliance matrix, competitive intelligence, win/loss history, resource capacity, strategic account plan
**Training Corpus:** Bid/no-bid decision frameworks (Shipley, APMP), capture management, strategic pursuit decisions
**LLM Tier:** Complex Reasoning (Opus class) - bid/no-bid decisions require multi-dimensional strategic analysis
**Criticality:** P0 - poor bid decisions waste resources or miss opportunities
**Why dedicated:** Bid/no-bid is a high-stakes strategic decision distinct from the execution of RFP responses.
**Prompt Pattern:** Analysis (multi-dimensional assessment) + Scoring (win probability, ROI) + Classification (recommendation)

---

## Agent RFP-005: RFP Library Manager

**Division:** RFP/RFQ Team
**Primary Function:** Manages the RFP response library, keeping content current and organized.
**Triggers:**
- 	ick_weekly - maintenance cycle
- product_feature_released_or_updated
- 
ew_competitive_threat_identified
- fp_response_approved
- content_quality_issue_reported
- 
ew_compliance_certification_obtained
**Outputs:**
- fp_library_gap_report - missing content areas
- fp_content_staleness_index - outdated responses
- fp_content_update_priority - what to update first
- fp_answer_quality_score - freshness and completeness
- fp_content_organization_suggestion - taxonomy improvements
- fp_template_update_notification - new templates needed
- fp_content_usage_statistics - most/least used content
- fp_library_health_dashboard - overall library status
**Data Sources:** RFP response history, product documentation updates, competitive intelligence, compliance certifications, usage analytics
**Training Corpus:** Content management best practices, knowledge base maintenance, technical documentation lifecycle
**LLM Tier:** Moderate (Sonnet class) - library management is primarily classification and quality scoring
**Criticality:** P2 - important for efficiency but not critical
**Why dedicated:** RFP library management is a continuous maintenance task distinct from per-RFP response generation.
**Prompt Pattern:** Classification (content quality) + Scoring (staleness) + Generation (update recommendations)

---

### Division 21: KNOWLEDGE & LEARNING TEAM

These agents manage the organizational knowledge base and power continuous learning.

---

## Agent KL-001: Deal Autopsy Agent

**Division:** Knowledge & Learning Team
**Primary Function:** Conducts systematic win/loss analysis to extract learnings from every deal outcome.
**Triggers:**
- deal_marked_won_or_lost
- deal_stage_exit_with_significant_learning
- quarterly_deal_autopsy_batch
- unexpected_win_or_loss
**Outputs:**
- deal_autopsy_report - structured win/loss analysis
- oot_cause_of_outcome - primary factor for win/loss
- competitive_learnings - what worked/didn't vs each competitor
- deal_process_improvements - what to change in process
- 	raining_recommendations - skills to develop
- messaging_effectiveness_feedback - what resonated
- win_loss_trend_analysis - patterns over time
- knowledge_base_updates - new insights to capture
**Data Sources:** CRM deal data, communication transcripts, deal timeline, competitor interactions, deal team notes, buyer feedback
**Training Corpus:** Win/loss analysis methodologies, root cause analysis (5 whys, fishbone), competitive analysis frameworks
**LLM Tier:** Complex Reasoning (Opus class) - deal autopsy requires tracing complex causal chains across many data points
**Criticality:** P2 - valuable for continuous improvement but not time-sensitive
**Why dedicated:** Deal autopsy is a dedicated post-mortem analysis requiring structured methodology distinct from deal execution.
**Prompt Pattern:** Analysis (root cause identification) + Extraction (learnings) + Generation (recommendations)

**Business Outcome:** Reduce repeat deal losses by 40% through systematic win/loss analysis, extracting actionable learnings from every closed deal within 48 hours of outcome.

**Functions (Detailed):**
- conduct_deal_autopsy(deal_id, outcome) -> structured_report
- identify_root_cause(outcome_data, deal_timeline) -> primary_factor
- extract_competitive_learnings(lost_deal, competitor) -> insight_entry
- generate_process_improvements(autopsy) -> recommendation_list
- flag_training_needs(recurring_issue) -> skill_gap_alert
- update_knowledge_base(learning, target_db) -> knowledge_entry

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- CRM deal data API
- Call transcript store (Gong/Chorus archive)
- Communication history DB (email, chat, meeting notes)
- Knowledge base update API

**KPIs & Metrics:**
- autopsy_completion_time: target <48h post-deal-close
- root_cause_accuracy: target >85%
- learning_actionability_rate: target >80%
- process_improvement_implementation: target >60%
- autopsy_coverage_rate: target >95% of all closed deals

**Performance Score:**
- **Red (<70):** Completion time >72h or accuracy below 75% — AIG-001 audit and retrain; escalation to AIG-002 for prompt refinement
- **Amber (70-85):** Accuracy 75-85% with partial coverage — acceptable with QA review; flag recurring misses for KL-005 retrain
- **Green (>85):** All targets met with consistent on-time delivery — fully autonomous; auto-publishes learnings to knowledge base

**Feedback Loop:**
Human validation of root cause findings logged → KL-005 weekly retrain on correction patterns → autopsy methodology refined. Override trigger: >20% incorrect root cause classifications (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent KL-002: Playbook Creator Agent

**Division:** Knowledge & Learning Team
**Primary Function:** Creates and updates sales plays based on deal autopsy findings and market shifts.
**Triggers:**
- deal_autopsy_completed_with_novel_learning
- competitive_threat_emerged
- market_condition_significant_change
- successful_deal_pattern_identified
- product_feature_major_release
- 
ew_buyer_persona_identified
- quarterly_playbook_refresh
**Outputs:**
- sales_play_document - structured play with all sections
- play_trigger_conditions - when to use this play
- play_success_metrics - how to measure effectiveness
- play_competitive_applications - which competitors it counters
- play_audience_segment - ideal buyer profile for the play
- play_outcome_forecast - expected impact
- playbook_organization_recommendation - where in hierarchy
- play_effectiveness_tracker - how plays perform over time
**Data Sources:** Deal autopsy reports, win/loss data, competitive intelligence, market research, product documentation, sales communication data
**Training Corpus:** Sales playbook creation, revenue play design (Salesforce, Gong, Outreach), situational sales frameworks
**LLM Tier:** Complex Reasoning (Opus class) - playbook creation requires synthesizing learning into actionable methodology
**Criticality:** P2 - playbooks drive scale but organizations can operate without automated ones
**Why dedicated:** Playbook creation is a synthesis and codification task distinct from deal execution.
**Prompt Pattern:** Synthesis (multiple learnings into play) + Generation (playbook content) + Classification (applicable scenarios)

**Business Outcome:** Reduce ramp time for new sales reps by 50% and increase play adoption rate to >80% through dynamically generated, data-backed sales plays.

**Functions (Detailed):**
- synthesize_play_from_learnings(learning_set, play_framework) -> play_document
- generate_play_trigger_conditions(play, deal_patterns) -> trigger_rules
- classify_applicable_scenarios(play, buyer_segments) -> scenario_list
- update_play_effectiveness(play_id, outcome_data) -> effectiveness_score
- retire_outdated_play(play_id, new_play_id) -> deprecation_record
- recommend_play_organization(play, existing_hierarchy) -> insertion_point

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- Deal autopsy store (KL-001 outputs)
- CRM win/loss pattern data
- Playbook version control KV
- Play effectiveness tracker DB

**KPIs & Metrics:**
- play_creation_time: target <4h per play
- play_adoption_rate: target >80%
- play_effectiveness_impact: target >+15% win rate on applicable deals
- play_refresh_frequency: target <90 days
- trigger_accuracy: target >90%

**Performance Score:**
- **Red (<70):** Play adoption below 50% or effectiveness impact <+5% — AIG-001 audit; escalation for play framework redesign
- **Amber (70-85):** Adoption 50-80% with moderate impact — acceptable; trigger refinement and usability improvements via KL-005 retrain
- **Green (>85):** Adoption at target with measurable win rate impact — autonomous play lifecycle management

**Feedback Loop:**
Play usage and effectiveness data collected → KL-005 weekly retrain on play structure improvements → underperforming plays flagged for revision. Override trigger: >30% plays with below-baseline performance (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent KL-003: Objection Library Manager

**Division:** Knowledge & Learning Team
**Primary Function:** Maintains a living library of buyer objections, effective responses, and handling techniques.
**Triggers:**
- 
ew_objection_heard_in_call
- existing_objection_has_ineffective_response
- market_condition_change_causing_new_objections
- competitor_move_creates_new_objections
- pricing_change_triggers_new_objections
**Outputs:**
- objection_catalog_entry - objection + recommended responses
- objection_frequency_tracker - how often each objection occurs
- objection_severity_rating - deal-killing vs minor
- objection_response_effectiveness - which responses work
- objection_by_stage_analysis - when objections arise
- objection_by_persona_analysis - who raises what
- objection_prevention_tips - how to avoid objections
- objection_training_materials - coaching resources
**Data Sources:** Call transcripts, email threads, meeting notes, competitive intelligence, market research, CRM deal stage data
**Training Corpus:** Objection handling frameworks (Challenger, MEDDIC, SPIN), sales negotiation techniques, competitive positioning
**LLM Tier:** Moderate (Sonnet class) - objection library management requires pattern recognition and response crafting
**Criticality:** P2 - valuable for improvement but not critical
**Why dedicated:** Objection management is a continuous capture and response optimization task distinct from playbook creation.
**Prompt Pattern:** Extraction (objection from conversation) + Classification (frequency, severity) + Generation (response)

**Business Outcome:** Achieve >90% objection coverage in the library with validated effective responses, reducing unhandled objections in live calls by 60% within 90 days.

**Functions (Detailed):**
- extract_objection(transcript_or_email, source_ref) -> objection_entry
- classify_objection_type(objection_text) -> category
- score_objection_severity(objection, deal_context) -> critical|major|minor
- track_objection_frequency(objection_id) -> occurrence_count
- evaluate_response_effectiveness(response, deal_outcome) -> effectiveness_rating
- generate_recommended_response(objection, best_practices) -> response_text

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Call transcript store
- Email/chat communication archive
- Objection library KV database
- CRM deal outcome data

**KPIs & Metrics:**
- objection_coverage_rate: target >90%
- response_effectiveness_score: target >80%
- objection_library_quality: target <5% outdated entries
- time_to_capture_new_objection: target <24h
- objection_prevention_rate: target >25% (reduction in repeat occurrences)

**Performance Score:**
- **Red (<70):** Coverage below 70% or response effectiveness <60% — AIG-001 audit; queue for playbook and training update via KL-005
- **Amber (70-85):** Coverage 70-90% with moderate effectiveness — acceptable; prioritize response refinement via KL-005 retrain
- **Green (>85):** Coverage at target with validated high-effectiveness responses — autonomous objection library management

**Feedback Loop:**
New objections from call analysis (CV-001) auto-ingested → effective-response data from deal outcomes logged → KL-005 weekly retrain on objection handling patterns. Override trigger: >15% ineffective responses (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent KL-004: Competitive Intelligence Synthesizer

**Division:** Knowledge & Learning Team
**Primary Function:** Synthesizes competitive intelligence from deal interactions and external sources into actionable insights.
**Triggers:**
- competitor_mentioned_in_call
- competitive_deal_loss
- competitive_win
- competitor_news_or_release
- competitor_pricing_change
- quarterly_competitive_update
- 
ew_competitor_entered_market
**Outputs:**
- competitive_brief - competitor profile update
- competitive_positioning_update - our +/vs/weaknesses
- competitive_win_theme_recommendation - how to position
- competitive_threat_level_assessment - urgency
- competitive_messaging_guidance - what to say
- competitive_battle_card_update - frontline material
- competitive_trend_analysis - patterns over time
- competitive_early_warning - emerging threats
**Data Sources:** Call transcripts, deal records, competitor websites and product, news feeds, industry reports, social media, win/loss data
**Training Corpus:** Competitive intelligence gathering (Crayon, Klue), competitive positioning, market analysis
**LLM Tier:** Complex Reasoning (Opus class) - competitive synthesis requires piecing together fragmented data into strategic insight
**Criticality:** P1 - competitive intelligence directly affects win rates
**Why dedicated:** Competitive intelligence requires continuous scanning and synthesis distinct from deal-specific analysis.
**Prompt Pattern:** Extraction (competitive signals) + Synthesis (trends) + Generation (battle card, guidance)

**Business Outcome:** Reduce competitive loss rate by 25% through real-time competitive intelligence synthesis, delivering actionable battle cards within 48 hours of competitive event detection.

**Functions (Detailed):**
- extract_competitive_signals(source_type, content) -> signal_entry
- synthesize_competitive_trend(signal_batch, time_window) -> trend_report
- generate_battle_card(competitor, positioning_data) -> battle_card_doc
- assess_threat_level(competitor, market_impact) -> critical|high|medium|low
- recommend_positioning(competitor, strengths, weaknesses) -> messaging_guidance
- monitor_competitor_changes(competitor_id, news_sources) -> change_alert

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- News aggregation feeds API
- Call transcript store (competitor mentions)
- CRM win/loss data
- Battle card library DB

**KPIs & Metrics:**
- battle_card_delivery_time: target <48h per event
- competitive_win_rate_impact: target >+25%
- signal_extraction_recall: target >90%
- battle_card_accuracy: target >85%
- intelligence_freshness: target <7 days stale max

**Performance Score:**
- **Red (<70):** Delivery time >72h or accuracy <75% — AIG-001 audit; escalation for prompt retraining and source pipeline review
- **Amber (70-85):** Delivery time 48-72h with acceptable accuracy — moderate; prioritize pipeline optimization
- **Green (>85):** All targets met with consistent fast delivery — autonomous competitive monitoring and battle card generation

**Feedback Loop:**
Competitive deal outcome data collected → battle card effectiveness measured against win/loss → KL-005 weekly retrain on positioning effectiveness. Override trigger: losing share to a competitor without timely intelligence (P0) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent KL-005: Training Content Generator

**Division:** Knowledge & Learning Team
**Primary Function:** Generates sales training materials from knowledge base content and deal learnings.
**Triggers:**
- 
ew_play_created_or_updated
- competitive_threat_requires_training
- product_feature_release_with_sales_impact
- skill_gap_identified_in_reviews
- onboarding_new_team_member
- efresher_training_due
**Outputs:**
- 	raining_module - structured learning content
- 	raining_video_script - video narration
- 	raining_quiz - knowledge check questions
- 	raining_roleplay_scenario - practice scenario
- 	raining_certification_assessment - pass/fail criteria
- 	raining_pathway_design - recommended learning progression
- 	raining_refresher_content - quick update on changes
- 	raining_effectiveness_metrics - assessment scores and impact
**Data Sources:** Playbook content, objection library, competitive intelligence, product documentation, deal autopsy reports, call recordings
**Training Corpus:** Instructional design (ADDIE, SAM), sales training best practices, e-learning content development
**LLM Tier:** Moderate (Sonnet class) - training content follows structured pedagogical formats
**Criticality:** P2 - training content drives scale and consistency
**Why dedicated:** Training content creation requires pedagogical methodology distinct from playbook creation or competitive intelligence.
**Prompt Pattern:** Generation (training materials) + Classification (skill level) + Assessment (quiz questions)

**Business Outcome:** Reduce sales rep ramp time to full productivity by 40% across all roles through personalized, dynamically generated training content from live knowledge base.

**Functions (Detailed):**
- generate_training_module(topic, format, skill_level) -> module_document
- classify_skill_level(rep_profile, assessment_results) -> beginner|intermediate|advanced
- create_assessment_quiz(module_content) -> quiz_questions
- generate_roleplay_scenario(module, persona_data) -> scenario_script
- design_training_pathway(rep_role, gaps) -> learning_progression
- measure_training_effectiveness(module_id, pre_post_scores) -> impact_report

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Playbook content store (KL-002)
- Objection library (KL-003)
- Competitive intelligence DB (KL-004)
- Rep skill assessment database

**KPIs & Metrics:**
- module_generation_time: target <2h per module
- training_effectiveness_score: target >+30% skill improvement
- training_relevance_score: target >85%
- training_completion_rate: target >90%
- knowledge_retention_rate: target >80% at 30 days

**Performance Score:**
- **Red (<70):** Skills improvement <15% or relevance <70% — AIG-001 audit; training content framework review and prompt retraining
- **Amber (70-85):** Improvement 15-30% with acceptable relevance — moderate; optimize content structure via KL-005 retrain
- **Green (>85):** All targets met with measurable skill improvement — autonomous training content generation and pathway design

**Feedback Loop:**
Post-training assessment scores collected → content effectiveness analyzed by AIG-001 → underperforming modules flagged for KL-005 regeneration. Override trigger: >25% low-effectiveness modules (P1) triggers AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

### Division 22: AI GOVERNANCE TEAM

These agents monitor, audit, and improve the performance of the agent system itself.

---

## Agent AIG-001: Agent Performance Auditor

**Division:** AI Governance Team
**Primary Function:** Audits agent outputs for accuracy, consistency, and adherence to standards.
**Triggers:**
- 	ick_daily - random sampling audit
- gent_output_flagged_as_anomalous
- gent_confidence_below_threshold
- human_complaint_about_agent_output
- gent_output_led_to_negative_deal_outcome
- 
ew_agent_deployed_or_updated
**Outputs:**
- gent_performance_report - accuracy, consistency, compliance
- nomalous_output_report - flagged outputs with analysis
- gent_accuracy_score - percentage correct
- gent_drift_detection - performance change over time
- udit_sample_log - which outputs were sampled
- improvement_recommendations - specific corrections
- gent_confidence_calibration_check - over/under confidence
- human_review_required_flag - outputs needing human review
**Data Sources:** Agent output log, ground truth data, human corrections, CRM data, call transcripts, meeting notes
**Training Corpus:** AI auditing methodologies, LLM output evaluation, quality assurance frameworks
**LLM Tier:** Complex Reasoning (Opus class) - auditing requires evaluating nuanced AI outputs against truth
**Criticality:** P0 - agent system quality depends on continuous auditing
**Why dedicated:** Agent auditing is a meta-task that requires impartial quality evaluation distinct from any domain agent.
**Prompt Pattern:** Analysis (output correctness) + Scoring (quality metrics) + Classification (review required)

**Business Outcome:** Maintain system-wide agent output accuracy at >95% through continuous automated auditing, detecting performance drift within 24 hours of occurrence.

**Functions (Detailed):**
- audit_agent_output(agent_id, output, ground_truth) -> accuracy_score
- score_output_quality(output, quality_rubric) -> quality_metrics
- detect_performance_drift(agent_id, trend_window) -> drift_alert
- classify_review_requirement(anomaly, severity) -> review_priority
- sample_outputs_for_audit(agent_pool, sample_rate) -> audit_sample
- generate_performance_report(agent_id, period) -> audit_report

**Tools/APIs:**
- NATS JetStream (event brokers)
- LLM inference API (Opus class — evaluator)
- Agent output log store
- Ground truth database (human-verified)
- Agent registry (deployed agents, versions)
- Anomaly detection engine

**KPIs & Metrics:**
- audit_sampling_coverage: target >5% of all outputs
- accuracy_score_system_wide: target >95%
- drift_detection_latency: target <24h
- false_positive_audit_flag: target <5%
- audit_report_generation_time: target <1h

**Performance Score:**
- **Red (<70):** System accuracy below 85% or drift detection >48h latency — escalation to human oversight; immediate AIG-002 prompt optimization
- **Amber (70-85):** Accuracy 85-95% with acceptable drift detection — moderate; prioritize corrective actions for underperforming agents
- **Green (>85):** All targets met with consistent accuracy — fully autonomous auditing; auto-escalates only confirmed critical issues

**Feedback Loop:**
Human validation of audit flags collected → audit rubric refined by AIG-002 → AIG-001 prompt updated with new evaluation criteria. Override trigger: >20% false positive flags (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AIG-002: Prompt Engineering Agent

**Division:** AI Governance Team
**Primary Function:** Designs, tests, and optimizes prompts for all agents in the system.
**Triggers:**
- 
ew_agent_created
- gent_performance_below_threshold
- gent_output_quality_degraded
- 
ew_llm_model_available
- prompt_optimization_cycle
- gent_behavior_change_requested
**Outputs:**
- gent_prompt_template - optimized prompt for each agent
- prompt_test_results - A/B test outcomes
- prompt_version_control - version history
- prompt_optimization_recommendation - specific changes
- prompt_effectiveness_metrics - before/after comparison
- prompt_injection_vulnerability_check - security assessment
- prompt_component_library - reusable prompt modules
- prompt_style_guide - consistency standards
**Data Sources:** Agent output logs, prompt test harness, performance metrics, prompt security testing tools, LLM documentation
**Training Corpus:** Prompt engineering best practices, LLM capability boundaries, prompt injection defense, few-shot learning design
**LLM Tier:** Complex Reasoning (Opus class) - prompt engineering requires deep understanding of LLM behavior nuances
**Criticality:** P1 - prompt quality directly determines agent output quality
**Why dedicated:** Prompt engineering requires specialized LLM expertise distinct from the domain knowledge of any other agent.
**Prompt Pattern:** Generation (prompt templates) + Analysis (prompt effectiveness) + Testing (A/B comparison)

**Business Outcome:** Reduce agent error rates by 60% through systematic prompt engineering, achieving >95% first-pass prompt effectiveness across all 27 agents within the system.

**Functions (Detailed):**
- generate_prompt_template(agent_spec, best_practices) -> prompt_template
- analyze_prompt_effectiveness(prompt_id, performance_data) -> effectiveness_rating
- run_ab_test(variant_a, variant_b, test_cases) -> winning_variant
- test_prompt_security(prompt) -> injection_vulnerabilities
- version_prompt(prompt_id, new_version) -> version_history
- optimize_prompt(prompt_id, performance_data, objectives) -> optimized_prompt

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class — prompt optimizer)
- Prompt template library KV
- Agent performance metrics store (AIG-001 outputs)
- Prompt test harness (simulated agent runs)
- Prompt security scanner

**KPIs & Metrics:**
- prompt_first_pass_effectiveness: target >95%
- prompt_optimization_cycle_time: target <8h
- ab_test_statistical_significance: target >95% confidence
- prompt_version_adoption: target 100% (all agents on latest)
- prompt_security_pass_rate: target 100%

**Performance Score:**
- **Red (<70):** First-pass effectiveness below 80% or security vulnerabilities detected — immediate review; human oversight on all prompt changes
- **Amber (70-85):** Effectiveness 80-95% with no security issues — acceptable; continue A/B testing cycle for improvement
- **Green (>85):** All targets met with validated security — fully autonomous prompt engineering; A/B testing automated

**Feedback Loop:**
Agent performance data from AIG-001 analyzed → underperforming prompts flagged for optimization → KL-005 weekly retrain on prompt effectiveness patterns. Override trigger: any prompt injection vulnerability (P0) triggers immediate human review. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AIG-003: Knowledge Base Orchestrator

**Division:** AI Governance Team
**Primary Function:** Manages the knowledge base federation across all agents, ensuring consistent and current information.
**Triggers:**
- 	ick_hourly - knowledge base health check
- knowledge_source_updated
- knowledge_gap_identified by any agent
- knowledge_conflict_detected - contradictory information
- 
ew_knowledge_source_available
- knowledge_base_performance_issue
**Outputs:**
- knowledge_base_health_report - freshness, coverage, conflicts
- knowledge_source_registry - all sources and their status
- knowledge_conflict_resolution - resolution for contradictions
- knowledge_coverage_gap_map - topics lacking coverage
- knowledge_refresh_schedule - when to update each source
- knowledge_source_retirement_recommendation - stale sources
- knowledge_federation_rules - which agents use which sources
- knowledge_base_performance_metrics - retrieval accuracy, latency
**Data Sources:** All knowledge sources used by agents, source metadata, retrieval analytics, agent feedback
**Training Corpus:** Knowledge management systems, RAG system architecture, information lifecycle management
**LLM Tier:** Complex Reasoning (Opus class) - knowledge orchestration requires understanding the entire knowledge ecosystem
**Criticality:** P1 - knowledge quality determines agent effectiveness across the system
**Why dedicated:** Knowledge orchestration is a system-wide meta-function distinct from any domain-specific knowledge task.
**Prompt Pattern:** Analysis (knowledge health) + Classification (conflict, gap) + Generation (resolution, schedule)

**Business Outcome:** Maintain knowledge base freshness at >95% with zero unanswered agent queries, reducing retrieval failure rate by 80% through proactive gap detection.

**Functions (Detailed):**
- analyze_knowledge_health(source_registry, usage_stats) -> health_report
- classify_knowledge_conflict(source_a_content, source_b_content) -> conflict_record
- detect_knowledge_gap(query_failures, agent_coverage) -> gap_report
- generate_resolution_plan(conflict_or_gap, resolution_strategy) -> plan
- schedule_refresh(source_id, refresh_frequency) -> schedule_entry
- retire_knowledge_source(source_id, replacement_id) -> retirement_record

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- All agent knowledge source registries
- Agent retrieval failure logs
- Source metadata store (freshness, format, permissions)
- Knowledge conflict detection engine

**KPIs & Metrics:**
- knowledge_base_freshness: target >95%
- query_retrieval_success_rate: target >99%
- gap_detection_to_resolution: target <24h
- conflict_resolution_accuracy: target >90%
- source_staleness_warning_time: target >7 days before expiry

**Performance Score:**
- **Red (<70):** Freshness below 80% or retrieval success <95% — escalation to AIG-001; immediate source pipeline review and AIG-002 prompt optimization
- **Amber (70-85):** Freshness 80-95% with acceptable retrieval — moderate; prioritize resolution of critical gaps
- **Green (>85):** All targets met with proactive gap detection — fully autonomous knowledge orchestration

**Feedback Loop:**
Agent query failure logs analyzed → knowledge gaps identified and filled → source quality feedback sent to KL-005 for retrain calibration. Override trigger: >15% retrieval failure rate (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AIG-004: Agent Collaboration Router

**Division:** AI Governance Team
**Primary Function:** Routes tasks between agents and orchestrates multi-agent workflows.
**Triggers:**
- 	ask_received_that_requires_multiple_agents
- gent_handoff_needed
- gent_overload_detected
- gent_busy_or_down
- workflow_execution_completed_one_step
- 	ask_priority_changed
**Outputs:**
- 	ask_routing_decision - which agent handles what
- workflow_execution_plan - multi-step orchestration
- gent_handoff_document - context for next agent
- workflow_status_update - progress on multi-agent tasks
- gent_queue_status - current load per agent
- 	ask_rerouting_action - if agent unavailable
- workflow_completion_report - outcome of orchestrated workflow
- gent_collaboration_pattern_analysis - optimization opportunities
**Data Sources:** Agent registry, agent capability definitions, task queue, workflow definitions, agent status, task priority data
**Training Corpus:** Multi-agent orchestration, workflow automation design (n8n, Zapier), distributed systems routing
**LLM Tier:** Complex Reasoning (Opus class) - orchestration requires holistic understanding of agent capabilities and dependencies
**Criticality:** P0 - orchestration is the central nervous system of the agent architecture
**Why dedicated:** Task routing and orchestration is a system-level function requiring ongoing coordination awareness.
**Prompt Pattern:** Classification (task to agent mapping) + Planning (workflow steps) + Monitoring (execution status)

**Business Outcome:** Achieve <5% task misrouting rate and reduce multi-agent workflow completion time by 50% through intelligent task routing and parallel execution optimization.

**Functions (Detailed):**
- classify_task_to_agent(task_request, agent_registry) -> best_agent_match
- plan_workflow_steps(task, agent_dependencies) -> execution_plan
- monitor_execution_status(workflow_id) -> current_status
- reroute_on_agent_failure(workflow, failed_step, alternatives) -> recovery_plan
- balance_agent_load(task_queue, agent_status) -> priority_assignment
- analyze_collaboration_patterns(workflow_history) -> optimization_recommendation

**Tools/APIs:**
- NATS JetStream (event brokers)
- LLM inference API (Opus class)
- Agent registry (capability, status, load)
- Workflow definition store
- Task queuing system
- Agent status heartbeat monitor

**KPIs & Metrics:**
- task_misrouting_rate: target <5%
- workflow_completion_time_reduction: target >50%
- agent_utilization_balance: target ±15% of mean
- recovery_time_on_failure: target <30s
- workflow_execution_success_rate: target >99%

**Performance Score:**
- **Red (<70):** Misrouting >15% or success rate <90% — escalation to AIG-001; immediate agent capability registry review and AIG-002 prompt optimization
- **Amber (70-85):** Misrouting 5-15% with acceptable success rate — moderate; optimize routing rules and retrain classification
- **Green (>85):** All targets met with minimal failures — fully autonomous routing with self-healing recovery

**Feedback Loop:**
Routing outcomes and failure data collected → misrouting patterns analyzed by AIG-001 → KL-005 weekly retrain on routing decision patterns. Override trigger: >15% misrouting of critical tasks (P1) triggers AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AIG-005: Agent Training & Feedback Agent

**Division:** AI Governance Team
**Primary Function:** Collects feedback, manages reinforcement signals, and tunes agent behavior over time.
**Triggers:**
- human_provides_feedback_on_agent_output
- gent_output_corrected_by_human
- positive_or_negative_deal_outcome
- gent_performance_trend_changed
- eedback_aggregation_cycle
- gent_behavior_adjustment_needed
**Outputs:**
- gent_feedback_log - structured feedback per output
- gent_behavior_adjustment - prompt or parameter change
- einforcement_signal - positive/negative per pattern
- gent_learning_curves - performance improvement over time
- eedback_aggregation_report - trends in feedback
- gent_behavior_issue_report - recurring problems
- gent_improvement_roadmap - prioritized enhancements
- human_in_the_loop_metrics - how much human intervention
**Data Sources:** Human feedback interface, output correction history, deal outcomes, agent performance metrics, user satisfaction scores
**Training Corpus:** Reinforcement learning from human feedback, LLM fine-tuning methodology, feedback system design
**LLM Tier:** Moderate (Sonnet class) - feedback processing follows structured aggregation patterns
**Criticality:** P1 - agent improvement depends on systematic feedback incorporation
**Why dedicated:** Agent training is a continuous improvement loop distinct from one-time prompt engineering.
**Prompt Pattern:** Analysis (feedback patterns) + Classification (positive/negative signal) + Generation (adjustment recommendations)

---

---

## Tier 4 — Foundation & Intelligence

---

### Division 23: ACCOUNT INTELLIGENCE TEAM

These agents provide deep account-level research and relationship mapping.

---

## Agent AI-001: Account Research Agent

**Division:** Account Intelligence Team
**Primary Function:** Conducts deep research on target accounts, providing comprehensive intelligence for account teams.
**Triggers:**
- ccount_entered_target_list
- ccount_research_needed
- ccount_reaching_key_milestone
- executive_change_at_account
- ccount_quarterly_business_review_preparation
**Outputs:**
- ccount_intelligence_report - company overview, strategy, priorities
- ccount_financial_health_score - revenue, funding, growth metrics
- ccount_technology_stack_analysis - current tech environment
- ccount_organizational_chart - decision makers and influencers
- ccount_initiative_mapping - active strategic initiatives
- ccount_challenge_identification - pain points and needs
- ccount_news_summary - recent developments
- ccount_competitive_landscape - who else sells to them
**Data Sources:** CrunchBase, LinkedIn, company website, annual reports, news, job postings, technology stack detection tools (BuiltWith, Wappalyzer), press releases
**Training Corpus:** B2B account research, financial analysis, organizational mapping, technographic profiling, CrunchBase blog firmographic data sources, LinkedIn Sales Navigator data quality articles, ZoomInfo blog account intelligence, BuiltWith blog technographic insights
**LLM Tier:** Complex Reasoning (Opus class) - account research requires synthesizing fragmented public data into strategic intelligence
**Criticality:** P1 - account intelligence directly informs engagement strategy
**Why dedicated:** Account research is a data-intensive synthesis task providing foundational intelligence for all other account-facing agents.
**Prompt Pattern:** Extraction (company data points) + Synthesis (strategic profile) + Scoring (health, fit)

**Business Outcome:** Reduce account research time by 80% and achieve >90% intelligence accuracy, enabling reps to have strategic, informed conversations from first contact.

**Functions (Detailed):**
- research_account(account_name, sources) -> intelligence_report
- extract_financial_health(account_data) -> health_score_and_metrics
- map_technology_stack(account_domain, detection_tools) -> tech_profile
- identify_strategic_initiatives(account_news, filings) -> initiative_list
- score_account_fit(account_profile, icp_criteria) -> fit_percentage
- generate_organizational_chart(contacts, hierarchy_data) -> org_chart

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- CrunchBase API / web enrichment sources
- LinkedIn Sales Navigator integration
- Technology stack detection tools
- Account intelligence DB (persistent store)

**KPIs & Metrics:**
- research_completion_time: target <15min per account
- intelligence_accuracy: target >90%
- account_fit_scoring_accuracy: target >85%
- research_coverage: target 100% of target accounts
- intelligence_update_frequency: target <30 days

**Performance Score:**
- **Red (<70):** Accuracy below 80% or research time >30min — escalation to AIG-001; source quality review and AIG-002 prompt optimization
- **Amber (70-85):** Accuracy 80-90% with acceptable research time — moderate; refine extraction prompts weekly via KL-005
- **Green (>85):** All targets met with comprehensive coverage — fully autonomous research generation

**Feedback Loop:**
Human corrections to account intelligence logged → KL-005 weekly retrain on extraction patterns → source reliability scores updated. Override trigger: >20% inaccuracy in financial/extractive fields (P1) triggers AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AI-002: Relationship Mapper

**Division:** Account Intelligence Team
**Primary Function:** Maps relationships between our team and the buyer organization, identifying warm paths and coverage gaps.
**Triggers:**
- ccount_entered_active_pursuit
- 
ew_contact_added_to_account
- contact_moved_roles_or_companies
- elationship_mapping_refresh_needed
- warm_intro_opportunity_detected
- ccount_quarterly_business_review_preparation
**Outputs:**
- ccount_relationship_map - org chart with relationship strength
- warm_intro_path_analysis - who can introduce us to whom
- coverage_gap_analysis - decision makers without relationships
- elationship_strength_score - per-contact and per-account
- elationship_building_plan - targeted relationship actions
- executive_relationship_bridge - C-suite connection map
- elationship_decay_alert - atrophied connections
- mutual_connection_discovery - through CRM and LinkedIn
**Data Sources:** CRM contact data, email and calendar history, LinkedIn (through integrations), meeting notes, call transcripts, past deal data
**Training Corpus:** Account relationship mapping, social selling frameworks, organizational network analysis
**LLM Tier:** Moderate (Sonnet class) - relationship mapping is a structured graph-building task
**Criticality:** P1 - relationship intelligence directly affects deal progression
**Why dedicated:** Relationship mapping is a continuous graph management task distinct from account research.
**Prompt Pattern:** Extraction (relationship data) + Graph Construction (relationship map) + Analysis (gap, strength)

**Business Outcome:** Achieve >90% relationship coverage on all decision-makers in active deals, enabling warm intros to 3x more buying committee members.

**Functions (Detailed):**
- extract_relationships(account_id, contact_sources) -> relationship_edges
- build_relationship_graph(relationships, account_id) -> graph_model
- analyze_coverage_gaps(graph, ideal_coverage) -> gap_report
- assess_relationship_strength(relationship_history) -> strength_score
- discover_warm_intro_paths(target_contact, relationship_graph) -> path_list
- suggest_relationship_building_actions(gap, account_strategy) -> action_plan

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- CRM contact database
- Email/calendar history API
- LinkedIn integration data
- Relationship graph store (Neo4j or equivalent)

**KPIs & Metrics:**
- relationship_coverage_on_dealmakers: target >90%
- warm_intro_path_discovery: target >3 per stakeholder
- relationship_strength_scoring_accuracy: target >85%
- coverage_gap_detection_recall: target >95%
- relationship_map_freshness: target <7 days stale

**Performance Score:**
- **Red (<70):** Coverage below 70% or strength scoring <70% accuracy — AIG-001 audit; data source pipeline review and AIG-002 prompt optimization
- **Amber (70-85):** Coverage 70-90% with acceptable accuracy — moderate; prioritize gap closure actions
- **Green (>85):** All targets met with comprehensive mapping — autonomous relationship graph management

**Feedback Loop:**
Relationship data from meeting outcomes and call analysis (CV-001) ingested → relationship strength recalibrated → KL-005 weekly retrain on relationship pattern recognition. Override trigger: >20% incorrect strength scoring (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AI-003: Buying Committee Analyzer

**Division:** Account Intelligence Team
**Primary Function:** Identifies and profiles every member of the buying committee for active deals.
**Triggers:**
- deal_created_or_stage_changed
- 
ew_stakeholder_added_to_deal
- stakeholder_role_or_influence_changed
- deal_in_technical_evaluation_phase
- deal_needs_executive_sponsor_mapping
**Outputs:**
- uying_committee_profiles - per-member profile
- stakeholder_influence_map - who influences whom
- stakeholder_sentiment_analysis - supporter/neutral/detractor
- stakeholder_pain_alignment - which pains resonate per person
- stakeholder_communication_preference - style and channel
- stakeholder_power_structure - decision hierarchy
- coverage_strategy - how to engage each stakeholder
- stakeholder_sentiment_trend - changes over time
**Data Sources:** CRM contact records, call transcripts, email threads, meeting notes, LinkedIn data, deal stage information
**Training Corpus:** Buying committee analysis (Gartner, Forrester), B2B stakeholder mapping, influence analysis
**LLM Tier:** Complex Reasoning (Opus class) - buying committee analysis requires nuanced understanding of interpersonal dynamics
**Criticality:** P1 - buying committee understanding is critical for complex deal navigation
**Why dedicated:** Buying committee analysis is a relationship dynamics task distinct from general account research.
**Prompt Pattern:** Extraction (stakeholder attributes) + Analysis (influence, sentiment) + Generation (engagement strategy)

**Business Outcome:** Increase stakeholder engagement rate by 40% and reduce deal slippage due to unidentified stakeholders by 60% through complete buying committee mapping.

**Functions (Detailed):**
- identify_stakeholders(deal_id, contact_sources) -> stakeholder_list
- analyze_influence(stakeholder, org_structure, deal_context) -> influence_rating
- assess_sentiment(stakeholder, communication_data) -> supporter|neutral|detractor
- generate_engagement_strategy(stakeholder_profile, persona_data) -> strategy_plan
- map_power_structure(stakeholders, dependencies) -> influence_diagram
- track_sentiment_trends(stakeholder_id, time_window) -> sentiment_timeline

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- CRM deal contact data
- Call and email communication analytics
- Org chart data (AI-001 output)
- Relationship graph (AI-002 output)

**KPIs & Metrics:**
- stakeholder_identification_recall: target >95%
- influence_rating_accuracy: target >85%
- engagement_strategy_effectiveness: target >+40% engagement
- sentiment_tracking_accuracy: target >85%
- unmapped_stakeholder_rate: target <5% per deal

**Performance Score:**
- **Red (<70):** Stakeholder identification <80% or influence accuracy <70% — AIG-001 audit; data source pipeline review and AIG-002 prompt optimization
- **Amber (70-85):** Identification 80-95% with acceptable accuracy — moderate; refinements via KL-005 weekly retrain
- **Green (>85):** All targets met with comprehensive coverage — autonomous stakeholder mapping and strategy generation

**Feedback Loop:**
Engagement outcomes tracked against recommendations → KL-005 weekly retrain on influence modeling patterns. Override trigger: missing key stakeholder on >10% of deals (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AI-004: Account Health Monitor

**Division:** Account Intelligence Team
**Primary Function:** Monitors account health indicators to predict risk, churn, or expansion opportunities.
**Triggers:**
- 	ick_daily - health score monitoring
- support_ticket_spike_detected
- ccount_usage_dropped_significantly
- executive_sponsor_change_at_account
- enewal_within_90_days
- expansion_opportunity_detected
**Outputs:**
- ccount_health_score - composite health rating
- churn_risk_assessment - likelihood and drivers
- ccount_health_trend - trajectory over time
- early_warning_alerts - specific risk indicators
- health_improvement_recommendations - actions to protect account
- expansion_readiness_score - readiness for upsell
- ccount_health_comparison - vs peer accounts
- ccount_intervention_priority - which accounts need attention
**Data Sources:** Product usage data, support ticket data, CRM activity, communication frequency, payment history, NPS/satisfaction data
**Training Corpus:** Customer health scoring, churn prediction, customer success best practices (Gainsight, Totango, ChurnZero)
**LLM Tier:** Moderate (Sonnet class) - health monitoring is primarily metric computation with pattern detection
**Criticality:** P1 - account health monitoring prevents revenue churn
**Why dedicated:** Account health is a continuous monitoring task requiring its own data pipeline distinct from deal-oriented analysis.
**Prompt Pattern:** Scoring (health dimensions) + Classification (risk level) + Generation (intervention recommendations)

**Business Outcome:** Reduce preventable account churn by 50% and increase expansion revenue by 30% through real-time health monitoring with 7-day early warning on at-risk accounts.

**Functions (Detailed):**
- score_account_health(account_id, metric_sources) -> composite_health_score
- classify_churn_risk(health_score, trend_data) -> critical|high|medium|low
- detect_early_warning_signals(account_data) -> alert_list
- generate_intervention_plan(risk_level, account_context) -> action_plan
- assess_expansion_readiness(health_score, usage_growth) -> readiness_rating
- compare_account_health(account_id, peer_group) -> percentile_rank

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Product usage analytics API
- Support ticket system API
- CRM account data
- Customer success platform integration

**KPIs & Metrics:**
- churn_prediction_accuracy: target >85%
- early_warning_lead_time: target >7 days
- intervention_effectiveness: target >50% at-risk recovery
- health_score_calibration: target ±10% of actual outcome
- expansion_identification_accuracy: target >80%

**Performance Score:**
- **Red (<70):** Churn prediction <70% accuracy or warning lead <3 days — AIG-001 audit; health model recalibration and AIG-002 prompt optimization
- **Amber (70-85):** Prediction 70-85% with moderate lead time — acceptable; weekly health model refinement via KL-005
- **Green (>85):** All targets met with effective early warnings — autonomous health monitoring with auto-generated intervention

**Feedback Loop:**
Churn outcomes and intervention results tracked → health model recalibrated by AIG-001 → KL-005 weekly retrain on risk pattern recognition. Override trigger: >20% missed churn predictions (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent AI-005: Trigger Event Detector

**Division:** Account Intelligence Team
**Primary Function:** Detects trigger events across target accounts that indicate buying intent or organizational change.
**Triggers:**
- 	ick_hourly - continuous scan
- 
ews_about_target_account
- unding_round_detected
- executive_hiring_or_departure_at_account
- egulation_change_impacting_account_industry
- competitor_activity_in_account
**Outputs:**
- 	rigger_event_alert - event with deal impact assessment
- 	rigger_priority_ranking - which events to act on now
- 	rigger_to_playbook_mapping - which play applies
- ccount_trigger_timeline - all recent triggers
- 	rigger_based_outreach_draft - message leveraging the trigger
- 	rigger_source_tracking - where the trigger was detected
- 	rigger_effectiveness_analysis - which triggers lead to deals
- 	rigger_based_account_scoring - account priority updates
**Data Sources:** News feeds, press releases, LinkedIn, job posting boards, funding databases (CrunchBase, PitchBook), social media, SEC filings
**Training Corpus:** Trigger event selling methodologies, account-based marketing triggers, intent data utilization
**LLM Tier:** Moderate (Sonnet class) - trigger detection is pattern matching with classification
**Criticality:** P1 - trigger events are primary sales motion accelerators
**Why dedicated:** Trigger detection requires continuous scanning across multiple data sources distinct from periodic account analysis.
**Prompt Pattern:** Classification (trigger type) + Scoring (priority, relevance) + Generation (outreach draft)

---

### Division 24: SALES PSYCHOLOGY RESEARCH TEAM

These agents research and apply buyer psychology principles to improve sales effectiveness.

---

## Agent SPR-001: Buyer Persona Psychographer

**Division:** Sales Psychology Research Team
**Primary Function:** Develops psychological profiles for buyer personas based on interaction data.
**Triggers:**
- 
ew_buyer_persona_identified
- sufficient_interaction_data_accumulated
- uyer_behavior_pattern_change_detected
- persona_based_message_not_performing
- quarterly_persona_refresh
**Outputs:**
- uyer_persona_psychographic_profile - motivations, fears, values, decision style
- persona_communication_preference - tone, channel, format, frequency
- persona_decision_making_pattern - rational vs emotional, speed, risk tolerance
- persona_pain_sensitivity_map - which pains trigger action
- persona_value_hierarchy - what matters most (ROI, safety, status, ease)
- persona_objection_predisposition - likely objections by type
- persona_message_resonance_analysis - which messages work
- persona_psychographic_segment_comparison - differences between segments
**Data Sources:** Call transcripts, email responses, meeting notes, CRM data, survey responses, buyer behavior analytics, win/loss data
**Training Corpus:** Buyer psychology (Cialdini, Kahneman), B2B persona development, behavioral economics in sales
**LLM Tier:** Complex Reasoning (Opus class) - psychological profiling requires deep analysis of behavioral patterns
**Criticality:** P2 - valuable for messaging optimization but not critical
**Why dedicated:** Psychographic profiling requires behavioral science expertise distinct from demographic persona development.
**Prompt Pattern:** Analysis (behavioral patterns) + Classification (psychological traits) + Generation (persona profile)

**Business Outcome:** Improve message resonance scores by 35% across all buyer personas through validated psychographic profiles, enabling personalized communication at scale.

**Functions (Detailed):**
- analyze_behavioral_patterns(interaction_history, persona_id) -> pattern_report
- classify_psychological_traits(patterns, psychology_framework) -> trait_profile
- generate_persona_profile(traits, demographic_data) -> persona_document
- map_communication_preferences(persona, channel_data) -> preference_guide
- identify_decision_making_pattern(persona, deal_outcomes) -> decision_style
- create_pain_sensitivity_map(persona, objection_history) -> pain_map

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- Call transcript store
- Email response history
- CRM deal outcome data
- Persona profile DB

**KPIs & Metrics:**
- persona_profile_accuracy: target >85%
- message_resonance_improvement: target >+35%
- persona_coverage: target 100% of identified segments
- profile_refresh_frequency: target <90 days
- psychographic_insight_actionability: target >80%

**Performance Score:**
- **Red (<70):** Profile accuracy <70% or resonance improvement <15% — AIG-001 audit; psychology framework review and AIG-002 prompt optimization
- **Amber (70-85):** Accuracy 70-85% with moderate resonance improvement — acceptable; refine traits via KL-005 weekly retrain
- **Green (>85):** All targets met with validated profiles — autonomous persona management; profiles auto-updated from live interaction data

**Feedback Loop:**
Message performance data correlated with persona profiles → underperforming profiles flagged for revision → KL-005 weekly retrain on psychological trait patterns. Override trigger: >20% inaccurate trait classifications (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent SPR-002: Message Psychology Optimizer

**Division:** Sales Psychology Research Team
**Primary Function:** Applies psychological principles to optimize sales messaging for maximum resonance.
**Triggers:**
- message_draft_needs_psychological_optimization
- uyer_persona_psychographic_profile_updated
- message_performance_below_baseline
- 
ew_channel_or_format_for_outreach
- b_test_results_available_for_learning
**Outputs:**
- psychologically_optimized_message - message with psychological triggers
- psychological_trigger_analysis - which triggers are activated
- message_resonance_prediction - expected engagement level
- persuasion_pattern_applied - specific technique used (scarcity, social proof, etc.)
- persona_specific_adjustment - tailored for target persona
- cognitive_bias_utilization - biases leveraged in message
- message_tone_and_framing_analysis - emotional framing
- message_psychology_score - how well psychological principles are applied
**Data Sources:** Message drafts, persona psychographic profiles, persuasion research database, A/B test results, engagement data
**Training Corpus:** Persuasion psychology (Cialdini principles), neuromarketing, copywriting psychology, behavioral economics
**LLM Tier:** Complex Reasoning (Opus class) - psychological optimization requires nuanced application of behavioral science
**Criticality:** P2 - improves effectiveness but messages work without it
**Why dedicated:** Message psychology optimization requires behavioral science expertise distinct from copywriting.
**Prompt Pattern:** Analysis (psychology gap) + Generation (optimized message) + Scoring (psychological effectiveness)

---

## Agent SPR-003: Cognitive Bias Detector

**Division:** Sales Psychology Research Team
**Primary Function:** Identifies cognitive biases at play in buyer decision-making and suggests counter-strategies.
**Triggers:**
- deal_stalled_or_delayed
- uyer_exhibiting_irrational_behavior
- objection_seems_rooted_in_bias
- competitor_win_due_to_buyer_bias
- deal_review_reveals_bias_pattern
**Outputs:**
- cognitive_bias_identification - bias type and evidence
- ias_impact_assessment - how bias affects the deal
- ias_counter_strategy - specific techniques to overcome
- ias_awareness_message_draft - communication that addresses bias
- ias_pattern_in_account - recurring biases in this buyer
- ias_training_recommendation - team awareness
- ias_based_deal_risk_assessment - risk level due to bias
- ias_mitigation_playbook - standard plays per bias type
**Data Sources:** Call transcripts, email threads, meeting notes, deal timeline data, competitor interactions, buyer decision history
**Training Corpus:** Cognitive bias research (Kahneman, Tversky), behavioral economics, negotiation psychology
**LLM Tier:** Complex Reasoning (Opus class) - bias detection requires subtle behavioral pattern recognition
**Criticality:** P2 - bias awareness improves outcomes but is advanced capability
**Why dedicated:** Cognitive bias detection requires specialized psychology knowledge distinct from general buyer analysis.
**Prompt Pattern:** Classification (bias type) + Analysis (impact) + Generation (counter-strategy)

---

## Agent SPR-004: Decision Architecture Designer

**Division:** Sales Psychology Research Team
**Primary Function:** Designs the decision architecture for complex sales processes to reduce friction and guide buyers.
**Triggers:**
- complex_deal_with_multiple_decision_points
- uying_committee_analysis_shows_decision_friction
- deal_stage_progression_slower_than_benchmark
- uyer_paralysis_or_decision_avoidance_detected
- sales_process_redesign
**Outputs:**
- decision_architecture_design - structured decision pathway
- decision_friction_point_analysis - where decisions stall
- decision_framework_recommendation - how to frame choices
- choice_architecture_design - how options are presented
- decision_default_option - easiest path forward
- decision_milestone_structure - smaller commitments
- decision_fatigue_prevention_plan - cognitive load management
- decision_confidence_builder - evidence and validation strategy
**Data Sources:** Deal stage progression data, buying committee analysis, decision timing data, communication transcripts, win/loss data
**Training Corpus:** Decision architecture (Thaler, Sunstein), choice architecture in B2B, behavioral economics applied to enterprise sales
**LLM Tier:** Complex Reasoning (Opus class) - decision architecture requires sophisticated behavioral design
**Criticality:** P2 - advanced capability for complex deal acceleration
**Why dedicated:** Decision architecture is a behavioral design discipline distinct from messaging or persona analysis.
**Prompt Pattern:** Analysis (decision friction) + Design (decision pathway) + Generation (implementation)

---

## Agent SPR-005: Trust & Rapport Analyzer

**Division:** Sales Psychology Research Team
**Primary Function:** Analyzes trust and rapport levels in buyer relationships.
**Triggers:**
- deal_relationship_review_needed
- 	rust_issue_suspected_in_deal
- uyer_engagement_decreased
- 
ew_stakeholder_entered_deal_with_skepticism
- competitive_situation_requires_trust_leverage
- quarterly_relationship_health_check
**Outputs:**
- 	rust_score_per_stakeholder - quantified trust level
- 	rust_building_opportunities - specific actions to build trust
- 	rust_erosion_warning - signs of trust degrading
- apport_quality_assessment - personal connection level
- 	rust_leveraging_strategy - how to use existing trust
- 	rust_repair_plan - if trust has been damaged
- 	rust_transfer_opportunity - use one trust to build another
- 	rust_based_communication_guidance - tone adjustments
**Data Sources:** Call transcripts (tone, language analysis), email patterns, meeting frequency and quality, relationship mapping data, feedback
**Training Corpus:** Trust frameworks (Mayer, Davis, Schoorman), rapport building methodology, social capital assessment
**LLM Tier:** Complex Reasoning (Opus class) - trust assessment requires subtle linguistic and behavioral analysis
**Criticality:** P2 - trust analysis is advanced capability for strategic account management
**Why dedicated:** Trust analysis requires specialized interpersonal assessment expertise distinct from general relationship mapping.
**Prompt Pattern:** Analysis (trust signals in communication) + Scoring (trust level) + Generation (trust building plan)

---

### Division 25: CUSTOMER VOICE TEAM

These agents capture and analyze buyer feedback, sentiment, and signals across all touchpoints.

---

## Agent CV-001: Call Sentiment Analyst

**Division:** Customer Voice Team
**Primary Function:** Analyzes sales calls for sentiment, engagement, buying signals, and coaching opportunities.
**Triggers:**
- call_recording_or_transcript_available
- call_summary_needed
- uying_signal_detected_in_realtime
- call_coaching_opportunity_identified
- call_ended_with_negative_outcome
**Outputs:**
- call_sentiment_analysis - sentiment per segment and overall
- call_engagement_score - participant engagement levels
- uying_signal_detection - specific buying signals with timestamps
- objection_occurrence_log - objections raised and responses
- call_summary_with_key_takeaways - structured summary
- 	alk_time_ratio_analysis - who spoke how much
- question_quality_assessment - questions asked by seller
- coaching_opportunities - specific improvement areas
- ollow_up_item_extraction - action items from call
**Data Sources:** Call recording platforms (Gong, Chorus, Zoom), transcription services, CRM call logging
**Training Corpus:** Call analysis frameworks, conversation intelligence, sales coaching methodologies (Gong, Chorus, Jiminny)
**LLM Tier:** Moderate (Sonnet class) - call analysis follows structured conversation analysis patterns
**Criticality:** P1 - call analytics drive coaching and deal intelligence
**Why dedicated:** Call analysis requires audio/transcript-specific processing distinct from text-based communication analysis.
**Prompt Pattern:** Extraction (signals, objections) + Analysis (sentiment, engagement) + Generation (summary, coaching)

**Business Outcome:** Improve call-to-close conversion by 20% through real-time sentiment and buying signal detection, delivering actionable coaching insights within 1 hour of call completion.

**Functions (Detailed):**
- analyze_call_sentiment(transcript, segments) -> segment_sentiment_map
- extract_buying_signal(transcript, signal_definitions) -> signal_with_timestamp
- log_objection_occurrence(transcript, objection_definitions) -> objection_log
- calculate_engagement_score(transcript, participation_metrics) -> engagement_percentage
- generate_call_summary(transcript, analysis) -> structured_summary
- identify_coaching_opportunity(analysis, best_practices) -> coaching_tip

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Call recording API (Gong/Chorus/Zoom)
- Transcription service
- Signal pattern database
- Coaching recommendations KB

**KPIs & Metrics:**
- sentiment_analysis_accuracy: target >85%
- buying_signal_detection_recall: target >90%
- objection_capture_rate: target >85%
- summary_generation_time: target <15min post-call
- coaching_tip_effectiveness: target >+20% conversion improvement

**Performance Score:**
- **Red (<70):** Sentiment accuracy <75% or signal recall <75% — AIG-001 audit; signal pattern review and AIG-002 prompt optimization
- **Amber (70-85):** Accuracy 75-85% with acceptable signal detection — moderate; refine patterns via KL-005 weekly retrain
- **Green (>85):** All targets met with timely delivery — autonomous call analysis; coaching auto-generated and pushed to rep dashboard

**Feedback Loop:**
Coach and rep feedback on analysis quality collected → signal patterns refined by AIG-002 → KL-005 weekly retrain on sentiment and signal accuracy. Override trigger: >20% missed buying signals (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent CV-002: Written Communication Sentiment Tracker

**Division:** Customer Voice Team
**Primary Function:** Analyzes written communications (email, chat) for sentiment and intent.
**Triggers:**
- email_or_chat_message_received
- communication_thread_being_monitored
- sentiment_shift_detected_in_thread
- uyer_stated_satisfaction_or_dissatisfaction
- communication_requires_urgency_assessment
**Outputs:**
- message_sentiment_score - positive/negative/neutral
- communication_intent_classification - question, concern, request, commitment
- sentiment_trend_in_thread - changes over time
- urgency_assessment - how quickly response needed
- communication_tone_analysis - formal, frustrated, enthusiastic
- uyer_satisfaction_indicator - satisfaction signals
- esponse_priority_rating - prioritize response queue
- sentiment_based_alert - significant negative shift
- communication_style_match - adapt to buyer preferences
**Data Sources:** Email threads, chat platforms (Slack, Teams), CRM communication history, support tickets
**Training Corpus:** Sentiment analysis, communication psychology, customer communication best practices
**LLM Tier:** Moderate (Sonnet class) - written sentiment analysis follows established NLP patterns
**Criticality:** P2 - sentiment tracking provides useful alerts but is not deal-critical
**Why dedicated:** Written communication analysis requires real-time monitoring of a different medium than call analysis.
**Prompt Pattern:** Classification (sentiment, intent) + Scoring (urgency) + Analysis (trend)

**Business Outcome:** Reduce negative sentiment response time to <1 hour and improve communication alignment score with buyer preferences by 30% through real-time written communication analysis.

**Functions (Detailed):**
- classify_message_sentiment(message_text) -> positive|negative|neutral|mixed
- detect_intent(message_text, intent_definitions) -> question|concern|commitment|request
- score_urgency(message_content, context, history) -> low|medium|high|critical
- analyze_sentiment_trend(thread_id, time_window) -> trend_direction
- detect_sentiment_shift(thread_id, message_comparison) -> shift_alert
- suggest_response_priority(messages, urgency_scores) -> priority_queue

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Email API integration
- Chat platform API (Slack/Teams)
- CRM communication history
- Sentiment model store

**KPIs & Metrics:**
- sentiment_classification_accuracy: target >85%
- urgency_scoring_accuracy: target >85%
- negative_sentiment_response_time: target <1h
- intent_detection_recall: target >80%
- sentiment_trend_detection_accuracy: target >80%

**Performance Score:**
- **Red (<70):** Classification accuracy <75% or urgency scoring <70% — AIG-001 audit; model recalibration and AIG-002 prompt optimization
- **Amber (70-85):** Accuracy 75-85% with acceptable urgency detection — moderate; refine classification patterns via KL-005 retrain
- **Green (>85):** All targets met with real-time detection — fully autonomous; critical alerts auto-escalated to reps and managers

**Feedback Loop:**
Human response ratings on urgency/sentiment flags collected → KL-005 weekly retrain on classification corrections. Override trigger: >20% miscategorized critical messages (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent CV-003: NPS & Survey Response Agent

**Division:** Customer Voice Team
**Primary Function:** Processes and analyzes NPS and customer survey responses.
**Triggers:**
- 
ps_survey_response_received
- survey_campaign_completed
- survey_response_requires_immediate_follow_up
- 
ps_trend_analysis_needed
- survey_design_feedback_available
**Outputs:**
- 
ps_score_calculation - score with confidence interval
- survey_response_thematic_analysis - key themes
- detractor_immediate_alert - needs human follow-up
- survey_driver_analysis - what drives scores
- 
ps_trend_report - change over time
- survey_verbatim_insights - notable comments
- improvement_priority_matrix - impact vs effort
- closed_loop_follow_up_task - actionable items
- segment_based_nps_comparison - by account type
**Data Sources:** NPS survey platform, CRM customer data, survey response database, customer segment data
**Training Corpus:** NPS methodology (Reichheld), survey analysis, customer experience management (Qualtrics, Medallia)
**LLM Tier:** Moderate (Sonnet class) - survey analysis is thematic analysis with structured scoring
**Criticality:** P2 - survey analysis provides strategic insights
**Why dedicated:** Survey analysis requires structured research methodology distinct from free-form sentiment tracking.
**Prompt Pattern:** Analysis (thematic, driver) + Classification (detractor/promoter) + Generation (improvement plan)

---

## Agent CV-004: Churn Signal Detector

**Division:** Customer Voice Team
**Primary Function:** Detects early churn signals from communication patterns and account behavior.
**Triggers:**
- 	ick_daily - continuous monitoring
- support_ticket_sentiment_negative
- communication_frequency_dropped
- executive_sponsor_left_account
- usage_metric_dropped_significantly
- contract_renewal_approaching
**Outputs:**
- churn_signal_alert - specific signal with confidence
- churn_risk_score - composite churn probability
- churn_signal_classification - behavioral, communication, usage, relationship
- signal_strength_assessment - low/medium/high
- churn_mitigation_strategy - recommended interventions
- churn_driver_analysis - root causes of signals
- ccount_churn_timeline - predicted timeline
- churn_watchlist - accounts needing attention
- intervention_effectiveness_tracking - what worked
**Data Sources:** Product usage data, support tickets, communication frequency, relationship mapping, account health data, billing history
**Training Corpus:** Churn prediction methodologies, customer success analytics, churn driver research (B2B SaaS)
**LLM Tier:** Complex Reasoning (Opus class) - churn detection requires synthesizing multi-source signals into risk assessment
**Criticality:** P1 - churn detection directly protects revenue
**Why dedicated:** Churn signal detection requires multi-dimensional signal fusion distinct from general account health monitoring.
**Prompt Pattern:** Classification (signal type) + Scoring (risk level) + Analysis (root cause) + Generation (mitigation)

---

## Agent CV-005: Voice of Customer (VOC) Program Manager

**Division:** Customer Voice Team
**Primary Function:** Manages the Voice of Customer program, aggregating feedback across all channels.
**Triggers:**
- 	ick_weekly - feedback aggregation
- quarterly_voc_report_due
- major_feedback_theme_emerging
- product_team_requests_customer_insights
- customer_reference_requested
**Outputs:**
- oc_insight_report - aggregated customer feedback
- eedback_theme_clusters - grouped by topic
- eedback_priority_matrix - frequency vs impact
- customer_quote_library - searchable verbatims
- product_feedback_for_roadmap - prioritized feature requests
- 	estimonial_and_case_study_opportunities - reference candidates
- oc_dashboard - metrics and trends
- eedback_loop_effectiveness_report - closed-loop tracking
- executive_voc_summary - customer sentiment for leadership
**Data Sources:** NPS responses, survey data, support tickets, call transcripts, email feedback, social media mentions, review sites (G2, Capterra)
**Training Corpus:** Voice of Customer program management (Qualtrics, Medallia), customer insight aggregation, CX management
**LLM Tier:** Complex Reasoning (Opus class) - VOC requires synthesizing diverse feedback into strategic insights
**Criticality:** P2 - VOC drives product and go-to-market improvement
**Why dedicated:** VOC program management is a synthesis and reporting function distinct from individual feedback channel analysis.
**Prompt Pattern:** Extraction (feedback from channels) + Synthesis (theme clustering) + Analysis (priority, impact)

---

### Division 26: DATA SERVICES TEAM

These agents provide foundational data operations and analytical infrastructure.

---

## Agent DS-001: CRM Data Hygiene Agent

**Division:** Data Services Team
**Primary Function:** Maintains CRM data quality through deduplication, enrichment, and standardization.
**Triggers:**
- 	ick_daily - data quality scan
- duplicate_record_detected
- incomplete_record_identified
- data_import_completed
- data_standardization_needed
- data_enrichment_source_received
**Outputs:**
- data_quality_score - overall CRM data health
- duplicate_record_report - duplicates for merge
- incomplete_record_list - records needing data
- data_standardization_changes - normalized values
- enrichment_recommendations - missing data to add
- merge_suggestion_log - records to merge
- data_quality_rule_violations - broken quality rules
- data_quality_improvement_trend - progress over time
**Data Sources:** CRM, data enrichment APIs (Clearbit, ZoomInfo), data quality rules, user-defined standards
**Training Corpus:** CRM data management (Salesforce, HubSpot), data quality frameworks, master data management
**LLM Tier:** Simple (Haiku class) - data hygiene is rule-based deduplication and standardization
**Criticality:** P1 - poor data quality undermines all agents
**Why dedicated:** Data hygiene is a continuous operational task requiring CRM-specific data management expertise.
**Prompt Pattern:** Classification (duplicate, incomplete) + Standardization (data formatting) + Merging (record consolidation)

**Business Outcome:** Achieve and maintain >98% CRM data quality score, reducing duplicate records to <1% and incomplete records to <3% across all objects.

**Functions (Detailed):**
- classify_record_quality(record, quality_rules) -> clean|duplicate|incomplete|stale
- standardize_data_field(record_id, field, format_rules) -> standardized_value
- merge_duplicate_records(primary_id, secondary_id, merge_rules) -> consolidated_record
- detect_data_anomaly(record, historical_pattern) -> anomaly_flag
- suggest_data_enrichment(record, enrichment_sources) -> enrichment_data
- generate_data_quality_report(object_type, period) -> quality_dashboard

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Haiku class)
- CRM API (Salesforce/HubSpot)
- Data enrichment APIs (Clearbit/Zoominfo)
- Data quality rule engine
- Record merge management tool

**KPIs & Metrics:**
- data_quality_score: target >98%
- duplicate_record_rate: target <1%
- incomplete_record_rate: target <3%
- standardization_accuracy: target >99%
- enrichment_completion_rate: target >80% of missing fields

**Performance Score:**
- **Red (<70):** Data quality <90% or duplicate rate >5% — AIG-001 audit; data quality rule review and AIG-002 prompt optimization
- **Amber (70-85):** Quality 90-98% with acceptable issues — moderate; prioritize fixes via daily hygiene scan
- **Green (>85):** All targets met with consistent quality — autonomous data hygiene; auto-merge low-risk duplicates

**Feedback Loop:**
Human corrections to merge/classification decisions logged → KL-005 weekly retrain on pattern recognition. Override trigger: >15% incorrect auto-merges (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent DS-002: Reporting & Dashboard Agent

**Division:** Data Services Team
**Primary Function:** Generates reports and dashboards across all revenue operations dimensions.
**Triggers:**
- 	ick_weekly_or_monthly - recurring reports
- d_hoc_report_requested
- dashboard_refresh_needed
- executive_quarterly_business_review
- pipeline_review_meeting
- nomaly_in_metrics_detected
**Outputs:**
- pipeline_report - pipeline metrics by stage, rep, region
- orecast_report - weighted and commit forecast
- conversion_funnel_report - stage conversion rates
- sales_activity_report - calls, emails, meetings per rep
- evenue_attribution_report - what drives revenue
- executive_dashboard - key metrics for leadership
- nomaly_report - metric deviations
- 	rend_report - month-over-month/quarter-over-quarter
- custom_report_definition - reusable report templates
**Data Sources:** CRM, billing data, marketing automation, call platform, email platform, activity logs
**Training Corpus:** Revenue reporting frameworks, sales analytics, dashboard design (Tableau, Power BI, Looker)
**LLM Tier:** Moderate (Sonnet class) - report generation requires structured data analysis and visualization design
**Criticality:** P1 - reporting is essential for management visibility
**Why dedicated:** Reporting requires analytics and visualization expertise distinct from operational tasks.
**Prompt Pattern:** Analysis (metrics computation) + Generation (report) + Visualization (dashboard design)

**Business Outcome:** Reduce report generation time by 90% and achieve zero-delay dashboard updates, enabling real-time visibility into all revenue operations metrics.

**Functions (Detailed):**
- compute_metrics(metric_definitions, data_sources, period) -> metric_values
- structure_report(metrics, report_template) -> report_document
- design_visualization(metric_data, chart_best_practices) -> visualization_config
- detect_metric_anomaly(current_values, historical_baseline) -> anomaly_alert
- schedule_report(report_id, frequency, recipients) -> schedule_entry
- generate_executive_dashboard(platform, kpis) -> dashboard_config

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- CRM data warehouse
- BI platform API (Tableau/Looker/PowerBI)
- Scheduled job manager
- Dashboard template store

**KPIs & Metrics:**
- report_generation_time: target <30s per report
- dashboard_freshness: target real-time (<5min lag)
- metric_accuracy: target 100% (verified against source)
- anomaly_detection_recall: target >90%
- report_adoption_rate: target >90% of stakeholders

**Performance Score:**
- **Red (<70):** Generation time >5min or metric errors detected — AIG-001 audit; data pipeline review and AIG-002 prompt optimization
- **Amber (70-85):** Generation time 30s-5min with accurate metrics — moderate; optimize pipeline performance
- **Green (>85):** All targets met with real-time delivery — fully autonomous reporting; dashboard self-service enabled

**Feedback Loop:**
Report usage analytics and human corrections collected → KL-005 weekly retrain on metric computation patterns. Override trigger: persistent metric discrepancies (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent DS-003: Data Integration Agent

**Division:** Data Services Team
**Primary Function:** Manages data pipelines between systems, ensuring clean and timely data flow.
**Triggers:**
- 
ew_data_source_connected
- data_sync_failure_detected
- data_mapping_error_identified
- data_latency_exceeds_threshold
- data_transformation_logic_update_needed
- 
ew_integration_requested
**Outputs:**
- data_pipeline_health_report - all integrations status
- data_sync_issue_log - failures with root cause
- data_mapping_documentation - field-to-field mappings
- data_transformation_script - ETL logic
- data_flow_diagram - source to destination
- integration_setup_guide - how to connect new source
- data_latency_report - sync timing per system
- data_consistency_check_results - cross-system validation
**Data Sources:** CRM, marketing automation, billing, support platform, data warehouse, integration tools (Zapier, Make, Workato)
**Training Corpus:** Data integration patterns, ETL design, API integration (REST, GraphQL), data pipeline architecture
**LLM Tier:** Moderate (Sonnet class) - data integration requires structured mapping and transformation logic
**Criticality:** P1 - data flow failures affect all downstream agents
**Why dedicated:** Data integration is a technical infrastructure task distinct from data analysis or reporting.
**Prompt Pattern:** Analysis (pipeline health) + Generation (transformation logic) + Classification (issue type)

**Business Outcome:** Achieve >99.9% data pipeline uptime and reduce data sync latency to <5min, ensuring all agents operate on the freshest data available.

**Functions (Detailed):**
- analyze_pipeline_health(pipeline_id, metrics) -> health_status
- generate_transformation_logic(source_schema, target_schema, rules) -> etl_script
- classify_issue(issue_description, error_log) -> data|mapping|connectivity|latency
- detect_sync_failure(pipeline_id, expected_vs_actual) -> failure_alert
- monitor_data_latency(pipeline_id, threshold) -> latency_report
- map_data_field(source_field, target_field, mapping_rules) -> mapped_field

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Integration platform API (Zapier/Make/Workato)
- Data warehouse query engine
- Pipeline monitoring tools
- API gateway connectors

**KPIs & Metrics:**
- pipeline_uptime: target >99.9%
- sync_latency: target <5min
- transformation_accuracy: target >99%
- mean_time_to_detect_failure: target <1min
- mean_time_to_resolve_issues: target <30min

**Performance Score:**
- **Red (<70):** Uptime <99% or latency >30min — AIG-001 audit; pipeline architecture review and AIG-002 prompt optimization
- **Amber (70-85):** Uptime 99-99.9% with acceptable latency — moderate; prioritize failure-prone pipelines
- **Green (>85):** All targets met with reliable throughput — autonomous pipeline management with auto-healing

**Feedback Loop:**
Pipeline failure data and human fixes logged → KL-005 weekly retrain on transformation and issue classification patterns. Override trigger: >10% pipeline failure rate (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent DS-004: Forecasting Agent

**Division:** Data Services Team
**Primary Function:** Generates revenue forecasts using historical data, pipeline analytics, and predictive models.
**Triggers:**
- 	ick_weekly - forecast cycle
- monthly_close_forecast_needed
- quarterly_guidance_preparation
- pipeline_significant_change
- orecast_accuracy_review
**Outputs:**
- evenue_forecast - weighted, commit, and stretch scenarios
- orecast_confidence_interval - range and probability
- pipeline_coverage_analysis - coverage ratio by rep/region
- historical_accuracy_comparison - how past forecasts performed
- orecast_driver_analysis - what is driving the forecast
- scenario_analysis - best/worst/most likely cases
- upside_potential_identification - deals that could accelerate
- downside_risk_assessment - deals at risk
- orecast_recommendations - actions to improve forecast outcome
**Data Sources:** CRM pipeline data, historical close rates, seasonal patterns, win/loss data, deal velocity metrics, external market data
**Training Corpus:** Sales forecasting methodologies (SFDC, Clari, Groove), statistical forecasting, pipeline analytics
**LLM Tier:** Complex Reasoning (Opus class) - forecasting requires probabilistic reasoning across multiple variables
**Criticality:** P0 - revenue forecast is critical for business operations
**Why dedicated:** Forecasting requires specialized predictive analytics expertise distinct from standard reporting.
**Prompt Pattern:** Analysis (pipeline and history) + Prediction (forecast scenarios) + Classification (risk/upside)

**Business Outcome:** Improve forecast accuracy to within ±5% of actual revenue by combining historical pattern analysis with real-time pipeline signals and probabilistic modeling.

**Functions (Detailed):**
- analyze_pipeline(deal_data, stage_conversion_rates) -> weighted_forecast
- predict_scenarios(pipeline, historical_patterns) -> best_case|likely|worst_case
- classify_upside_opportunity(deal, acceleration_signals) -> upside_candidate
- classify_downside_risk(deal, risk_factors) -> risk_assessment
- calculate_forecast_confidence(components, historical_accuracy) -> confidence_interval
- generate_forecast_report(forecasts, period) -> executive_report

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Opus class)
- CRM pipeline data
- Historical close rate DB
- Deal velocity analytics
- External market data feeds

**KPIs & Metrics:**
- forecast_accuracy_vs_actual: target ±5%
- confidence_interval_calibration: target >90% coverage
- scenario_analysis_completion: target <1h per cycle
- upside_identification_precision: target >80%
- risk_detection_recall: target >85%

**Performance Score:**
- **Red (<70):** Forecast error >±15% or confidence calibration <70% — AIG-001 audit; model recalibration and AIG-002 prompt optimization
- **Amber (70-85):** Error ±5-15% with acceptable calibration — moderate; refine prediction patterns via KL-005 weekly retrain
- **Green (>85):** All targets met with consistent accuracy — fully autonomous forecasting; auto-generates variance explanations

**Feedback Loop:**
Actual vs forecast outcomes logged monthly → KL-005 weekly retrain on prediction pattern corrections. Override trigger: persistent >±10% forecast error for 2 consecutive months (P0) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent DS-005: Attribution Modeler

**Division:** Data Services Team
**Primary Function:** Models revenue attribution across channels, campaigns, and touchpoints.
**Triggers:**
- 	ick_monthly - attribution refresh
- 
ew_marketing_channel_added
- campaign_completed_with_revenue
- ttribution_model_review_needed
- marketing_spend_effectiveness_analysis
**Outputs:**
- ttribution_model - configured attribution rules
- channel_attribution_report - revenue by channel
- campaign_roi_analysis - return per campaign
- 	ouchpoint_influence_analysis - importance of each touch
- ttribution_comparison - first/last/multi-touch comparison
- marketing_influenced_pipeline - pipeline with marketing touch
- sales_touch_attribution - deals influenced by specific activities
- ttribution_based_budget_recommendation - spend allocation
**Data Sources:** CRM, marketing automation, ad platforms, web analytics, call platform, email platform, campaign data
**Training Corpus:** Marketing attribution models, multi-touch attribution (Bizible, GA4, HubSpot), ROI analysis
**LLM Tier:** Complex Reasoning (Opus class) - attribution requires sophisticated multi-dimensional analysis
**Criticality:** P2 - attribution drives marketing optimization
**Why dedicated:** Attribution modeling requires specialized marketing analytics expertise distinct from general reporting or forecasting.
**Prompt Pattern:** Analysis (touchpoint contribution) + Modeling (attribution rules) + Scoring (channel effectiveness)

**Business Outcome:** Achieve >90% attribution accuracy across all channels, enabling data-driven marketing budget allocation that increases marketing-influenced pipeline by 25%.

**Functions (Detailed):**
- analyze_touchpoint_contribution(deal_id, touchpoint_history) -> contribution_fractions
- model_attribution_rules(rules_config, touchpoints) -> attributed_revenue
- score_channel_effectiveness(channel_id, attribution_results) -> effectiveness_score
- compare_attribution_models(first_touch, last_touch, multi_touch) -> model_comparison
- generate_roi_by_channel(attribution, spend_data) -> roi_report
- recommend_budget_allocation(effectiveness_scores, budget) -> allocation_plan

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- CRM with campaign tracking
- Marketing automation platform
- Ad platform APIs
- Spend data warehouse

**KPIs & Metrics:**
- attribution_model_accuracy: target >90%
- channel_effectiveness_score_variance: target ±10% of actual
- roi_calculation_accuracy: target >90%
- budget_recommendation_impact: target >+25% influenced pipeline
- model_refresh_frequency: target monthly

**Performance Score:**
- **Red (<70):** Attribution accuracy <80% or ROI variance >±20% — AIG-001 audit; attribution model review and AIG-002 prompt optimization
- **Amber (70-85):** Accuracy 80-90% with acceptable variance — moderate; refine attribution rules via KL-005 retrain
- **Green (>85):** All targets met with validated models — fully autonomous attribution; auto-generated budget recommendations

**Feedback Loop:**
Attribution vs actual measured outcomes logged → KL-005 weekly retrain on attribution modeling patterns. Override trigger: attribution model disagreement >20% with manual analysis (P1) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

### Division 27: SECURITY & PRIVACY TEAM

These agents protect sensitive data and ensure compliance across the entire agent system.

---

## Agent SP-001: Data Classification Agent

**Division:** Security & Privacy Team
**Primary Function:** Classifies data processed by agents according to sensitivity and regulatory requirements.
**Triggers:**
- 
ew_data_source_added_to_system
- gent_generates_or_processes_new_data_type
- egulatory_requirement_changed
- data_classification_audit_needed
- sensitive_data_detected_in_unclassified_source
**Outputs:**
- data_classification_registry - all data types and classifications
- sensitive_data_inventory - where sensitive data resides
- data_classification_change_log - reclassification history
- data_handling_requirement - how to handle per classification
- classification_rule_suggestions - new rules for detection
- unclassified_data_alert - data needing classification
- classification_audit_report - compliance with policy
- data_mapping_for_regulation - data x regulation matrix
**Data Sources:** Data source schemas, data samples, regulatory requirements, data classification policy, agent data usage logs
**Training Corpus:** Data classification frameworks, data privacy regulations (GDPR, CCPA, HIPAA), data governance
**LLM Tier:** Moderate (Sonnet class) - data classification follows established patterns and rules
**Criticality:** P0 - data classification is foundational for security and compliance
**Why dedicated:** Data classification is a systematic governance task requiring regulatory knowledge distinct from any domain agent.
**Prompt Pattern:** Classification (data sensitivity) + Analysis (regulatory mapping) + Generation (handling requirements)

**Business Outcome:** Achieve 100% data classification coverage across all agent-processed data, with zero unclassified sensitive data and full regulatory compliance mapping within 24 hours of new data source connection.

**Functions (Detailed):**
- classify_data_sensitivity(data_sample, classification_policy) -> public|internal|confidential|restricted
- map_to_regulation(data_type, regulatory_frameworks) -> applicable_regulations
- generate_handling_requirements(data_classification, regulations) -> handling_policy
- detect_unclassified_data(data_source, existing_registry) -> classification_alert
- audit_classification_accuracy(classifications, sample) -> accuracy_report
- suggest_classification_rule(data_pattern, classification_gaps) -> new_rule

**Tools/APIs:**
- NATS JetStream (event-driven triggers)
- LLM inference API (Sonnet class)
- Data source schema registry
- Regulatory requirements DB
- Data classification policy store
- Agent data usage logs

**KPIs & Metrics:**
- data_classification_coverage: target 100%
- unclassified_data_detection_time: target <24h
- classification_accuracy: target >95%
- regulatory_mapping_completeness: target 100%
- reclassification_turnaround: target <4h

**Performance Score:**
- **Red (<70):** Classification coverage <90% or regulatory gaps detected — AIG-001 audit; immediate human review and AIG-002 prompt optimization
- **Amber (70-85):** Coverage 90-100% with acceptable accuracy — moderate; prioritize remaining unclassified sources
- **Green (>85):** All targets met with full coverage — fully autonomous classification; auto-enforces handling policies

**Feedback Loop:**
Classification audit results and human overrides logged → KL-005 weekly retrain on sensitivity pattern detection. Override trigger: any unclassified PII/PHI discovered (P0) triggers AIG-002 prompt optimization. Override threshold triggering AIG-002 prompt optimization. Source: KL-005 weekly retrain cycle.

---

## Agent SP-002: Access Control Monitor

**Division:** Security & Privacy Team
**Primary Function:** Monitors and manages access controls across the agent system.
**Triggers:**
- 
ew_agent_deployed_or_updated
- 
ew_data_source_connected
- ccess_permission_change_requested
- unauthorized_access_attempt_detected
- ccess_review_audit_due
- user_role_changed
**Outputs:**
- ccess_control_matrix - who/what can access which data
- permission_change_log - all changes with audit trail
- unauthorized_access_alert - blocked attempts
- least_privilege_violation_report - over-permissioned agents
- ccess_review_report - audit results
- ccess_remediation_recommendations - fix over-permissions
- gent_data_access_log - which agents accessed what
- ccess_policy_violation_analysis - policy gaps
**Data Sources:** Agent registry, data classification, user management system, access logs, permission configuration
**Training Corpus:** Access control models (RBAC, ABAC), security best practices (least privilege), audit methodologies
**LLM Tier:** Moderate (Sonnet class) - access control monitoring is rule-based with classification
**Criticality:** P0 - access control violations can lead to data breaches
**Why dedicated:** Access control monitoring is a continuous security task distinct from data classification.
**Prompt Pattern:** Classification (access level) + Analysis (violation detection) + Generation (remediation)

---

## Agent SP-003: PII/PHI Redaction Agent

**Division:** Security & Privacy Team
**Primary Function:** Detects and redacts personally identifiable information and protected health information from agent outputs.
**Triggers:**
- gent_generates_output_with_identified_pii_or_phi
- data_contains_contact_information
- document_for_external_sharing_needs_sanitization
- compliance_audit_requires_redaction_verification
- 
ew_pii_or_phi_type_to_detect
**Outputs:**
- edacted_document - cleaned output
- pii_or_phi_detection_log - what was found and redacted
- edaction_verification_report - confirmed all detected
- alse_positive_analysis - incorrectly flagged items
- 
ew_pii_or_phi_pattern_suggestion - patterns to add
- pii_or_phi_exposure_alert - sensitive data in unexpected places
- edaction_effectiveness_score - recall and precision
- data_sharing_safety_assessment - safe to share externally
**Data Sources:** All agent outputs, data classification registry, PII/PHI pattern database, regulatory requirements
**Training Corpus:** PII/PHI detection patterns, data redaction techniques, privacy regulations (GDPR, HIPAA, CCPA)
**LLM Tier:** Moderate (Sonnet class) - PII/PHI detection follows pattern matching with contextual awareness
**Criticality:** P0 - PII/PHI exposure carries significant legal liability
**Why dedicated:** PII/PHI redaction requires specialized pattern detection and regulatory knowledge distinct from general security monitoring.
**Prompt Pattern:** Detection (PII/PHI patterns) + Redaction (sanitization) + Verification (completeness check)

---

## Agent SP-004: Compliance Audit Agent

**Division:** Security & Privacy Team
**Primary Function:** Performs continuous compliance audits across the agent system.
**Triggers:**
- 	ick_weekly - audit cycle
- egulatory_requirement_updated
- compliance_incident_detected
- udit_finding_from_external_auditor
- 
ew_compliance_framework_adopted
- gent_behavior_change_affecting_compliance
**Outputs:**
- compliance_audit_report - findings per framework
- compliance_score - overall compliance rating
- inding_details - specific non-compliances
- emediation_tracker - finding resolution status
- compliance_evidence_package - proof of compliance
- udit_trail_log - all compliance-relevant actions
- control_effectiveness_assessment - how well controls work
- compliance_trend_report - improvement or degradation
- egulatory_change_impact_analysis - new regulation effect
**Data Sources:** Agent output logs, access control logs, data classification, PII/PHI redaction logs, system configuration, regulatory database
**Training Corpus:** Compliance audit methodology (SOC2, ISO, HIPAA), audit frameworks (COBIT, ITIL), regulatory compliance
**LLM Tier:** Complex Reasoning (Opus class) - compliance audit requires holistic evaluation against regulatory frameworks
**Criticality:** P0 - compliance failures can result in legal and financial penalties
**Why dedicated:** Compliance auditing requires systematic audit methodology distinct from other security tasks.
**Prompt Pattern:** Analysis (control effectiveness) + Scoring (compliance level) + Generation (audit report, remediation)

---

## Agent SP-005: Incident Response Agent

**Division:** Security & Privacy Team
**Primary Function:** Detects and coordinates response to security incidents.
**Triggers:**
- security_breach_detected
- suspicious_activity_pattern_identified
- data_exposure_confirmed
- security_vulnerability_discovered
- 	hird_party_breach_affecting_us
- incident_response_drill
**Outputs:**
- incident_severity_assessment - severity, scope, impact
- incident_timeline - events in chronological order
- containment_recommendation - immediate actions
- eradication_plan - remove threat
- ecovery_steps - restore normal operation
- post_incident_analysis - root cause and lessons
- incident_report - for stakeholders and regulators
- preventive_measure_recommendations - avoid recurrence
- ffected_data_inventory - what data was exposed
**Data Sources:** System logs, access logs, agent output logs, data classification, security tools, incident history
**Training Corpus:** Incident response frameworks (NIST, SANS), security breach management, forensic analysis
**LLM Tier:** Complex Reasoning (Opus class) - incident response requires rapid multi-dimensional analysis under pressure
**Criticality:** P0 - incident response directly limits breach impact
**Why dedicated:** Incident response requires real-time crisis management methodology distinct from routine compliance monitoring.
**Prompt Pattern:** Analysis (incident scope and impact) + Generation (response actions, report) + Classification (severity)

---

## Agent SP-006: Consent & Preference Manager

**Division:** Security & Privacy Team
**Primary Function:** Manages buyer and customer consent preferences across all communication channels.
**Triggers:**
- contact_opted_in_or_out_of_communication
- consent_regulation_updated
- communication_scheduled_for_opted_out_contact
- consent_audit_needed
- 
ew_communication_channel_added
**Outputs:**
- consent_status_report - per contact/channel/type
- opt_out_compliance_check - validation before send
- consent_change_log - full audit trail
- communication_block_alert - prevented non-compliant send
- consent_framework_configuration - rules per regulation
- consent_renewal_reminder - expiring consents
- consent_policy_violation_report - non-compliance
- preference_based_segmentation - audiences by consent
**Data Sources:** CRM, email/marketing platforms, consent preferences database, regulatory database, communication logs
**Training Corpus:** Consent management frameworks (GDPR, CAN-SPAM, CASL), privacy preference management, communication compliance
**LLM Tier:** Moderate (Sonnet class) - consent management is rule-based with compliance cross-checking
**Criticality:** P1 - consent violations carry regulatory penalties
**Why dedicated:** Consent management requires real-time compliance checking distinct from general security monitoring.
**Pattern Type:** Classification (consent status) + Analysis (compliance verification) + Generation (violation report)

---

# END OF DOCUMENT

---

## Document Summary

**Total Agents:** 108
**Total Divisions:** 27 (across 4 tiers)
**Tier 1 — Core Revenue Engine:** Divisions 1-10 (approximately 55 agents)
**Tier 2 — Strategic & Operational Support:** Divisions 11-16 (approximately 30 agents)
**Tier 3 — Strategic Enablement:** Divisions 17-22 (approximately 30 agents)
**Tier 4 — Foundation & Intelligence:** Divisions 23-27 (approximately 30 agents)

**LLM Tier Distribution:**
- **Complex Reasoning (Opus class):** ~42 agents — strategic, analytical, psychological, compliance, and governance
- **Moderate (Sonnet class):** ~47 agents — generation, extraction, analysis, reporting
- **Simple (Haiku class):** ~19 agents — rule-based, computation, monitoring, hygiene

**Top 10 Most Critical Agent Categories (by P0 concentration):**
1. CRM Data Hygiene (Division 26)
2. Revenue Forecasting (Division 26)
3. Security/Compliance (Division 27)
4. RFP Response (Division 20)
5. Deal Strategy & Meddic (Division 9)
6. Negotiation (Division 10)
7. Agent Governance (Division 22)
8. Account Health (Division 23)
9. Customer Voice (Division 25)
10. Delivery Confidence (Division 19)
