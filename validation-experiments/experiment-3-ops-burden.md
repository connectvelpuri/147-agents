# SOVEREIGN CRM — VALIDATION EXPERIMENT 3: SELF-HOSTED OPS BURDEN SURVEY

**Document Type:** Validation Experiment Design  
**Created:** 2026-06-07  
**Author:** Hermes Agent  
**Duration:** 72 hours  
**Classification:** INTERNAL — NOT FOR GIT PUSH

---

## 1. EXPERIMENT OVERVIEW

### Objective
Validate whether IT Services companies are willing to manage self-hosted
infrastructure, or if the operational burden outweighs the benefits.

### Hypothesis
**H1:** IT Services companies have the technical capability and willingness
to self-host, especially when given clear documentation and support.

**H0 (Null):** The operational burden of self-hosting is too high, and
users prefer managed solutions despite privacy concerns.

### Key Metrics
- **Primary:** Willingness to self-host (Yes/No/Maybe)
- **Secondary:** Comfort level with technical requirements (1-5)
- **Tertiary:** Preferred deployment method

---

## 2. SURVEY DESIGN

### Target Audience
- IT Services company owners/operators
- SaaS startup CTOs/technical founders
- System administrators at small companies
- Developers interested in self-hosted tools

### Distribution Channels
- Reddit (r/selfhosted, r/sysadmin, r/devops)
- Hacker News (Ask HN)
- Twitter/X (self-hosted community)
- Dev.to article
- Email to early signups

---

## 3. SURVEY QUESTIONS

### Q1: Company Size
**What is your company size?**
- 1-5 employees
- 6-20 employees
- 21-50 employees
- 51-200 employees
- 200+ employees

### Q2: Current CRM
**What CRM do you currently use?**
- HubSpot (free tier)
- HubSpot (paid)
- Salesforce
- Zoho CRM
- Pipedrive
- Excel/Google Sheets
- No CRM
- Other: ___

### Q3: Self-Hosting Experience
**Have you self-hosted software before?**
- Yes, frequently (5+ self-hosted apps)
- Yes, occasionally (1-4 self-hosted apps)
- No, but I'm comfortable with command line
- No, and I prefer not to

### Q4: Willingness to Self-Host
**Would you be willing to self-host a CRM if it meant:**
- Complete data privacy
- No per-user fees
- Full customization control
- No vendor lock-in

**Scale:** Very Unlikely → Very Likely (1-5)

### Q5: Technical Requirements
**Which deployment method would you prefer?**
- Docker/Podman one-command setup
- Manual installation with guide
- Cloud marketplace (AWS, GCP, DigitalOcean)
- Managed hosting (we host for you)
- No preference

### Q6: Operational Concerns
**What concerns do you have about self-hosting? (Select all that apply)**
- Backup and disaster recovery
- Security updates and patches
- Performance monitoring
- Scaling as company grows
- Time required for maintenance
- Lack of IT staff
- Other: ___

### Q7: Support Expectations
**What level of support would you expect?**
- Community forum only
- Email support (48hr response)
- Priority email support (24hr response)
- Phone/video support
- Dedicated account manager

### Q8: Willingness to Pay
**Would you pay for:**
- Premium support plan
- Managed hosting option
- Advanced features
- Training/onboarding

**Scale:** Not interested → Very interested (1-5)

### Q9: Decision Factors
**Rank the following factors by importance (1 = most important):**
- Data privacy
- Ease of use
- Price
- Features
- Support quality
- Community size
- Customization options

### Q10: Open Feedback
**What would make you more likely to adopt a self-hosted CRM?**
[Open text field]

---

## 4. MEASUREMENT PLAN

### Success Criteria
| Metric | Target | Minimum |
|--------|--------|---------|
| Willingness to self-host | >60% Yes | >40% Yes |
| Comfort with tech requirements | >3.5 avg | >2.5 avg |
| Response rate | >200 responses | >100 responses |

### Analysis Plan
1. **Segment by company size** — Do larger companies prefer managed?
2. **Segment by current CRM** — Do HubSpot users prefer managed?
3. **Segment by self-hosting experience** — Does experience correlate with willingness?
4. **Identify top concerns** — What objections need addressing?

---

## 5. IMPLEMENTATION

### Survey Tool
- **Option A:** Google Forms (simple, free)
- **Option B:** Typeform (better UX, paid)
- **Option C:** Custom HTML form (full control)

### Distribution Strategy
1. **Day 1:** Post on Reddit (r/selfhosted, r/sysadmin)
2. **Day 1:** Tweet with survey link
3. **Day 2:** Post on Hacker News (Ask HN)
4. **Day 2:** Publish Dev.to article with survey embed
5. **Day 3:** Email to early signups, final push

### Timeline
- **Hour 0-2:** Create survey
- **Hour 2-24:** Begin distribution
- **Hour 24-48:** Monitor responses, boost distribution
- **Hour 48-72:** Close survey, analyze results

---

## 6. POST-EXPERIMENT ACTIONS

### If H1 Supported (Users Willing to Self-Host)
- Proceed with self-hosted deployment model
- Create comprehensive documentation
- Build deployment automation
- Offer premium support tier

### If H0 Not Rejected (Burden Too High)
- Consider managed hosting option
- Simplify deployment further
- Create video tutorials
- Offer white-glove onboarding

###无论结果如何
- Document findings in vault
- Update GO-NO-GO decision
- Inform Sprint 7 planning

---

*Document maintained by Hermes Agent. Never push to Git.*  
*Last Updated: 2026-06-07*
