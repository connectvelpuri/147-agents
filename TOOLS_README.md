# OSINT Tools for Account Intelligence

## Installed Tools

### 1. theHarvester
**Purpose:** Email, subdomain, IP, and employee reconnaissance
**Usage:** `python tools/osint/theHarvester/theHarvester.py -d company.com -b all`
**Output:** Emails, hosts, virtual hosts, employee names
**Value for sales:** Find key decision makers' email patterns, verify technology stack

### 2. sherlock
**Purpose:** Username search across 400+ social networks
**Usage:** `python tools/osint/sherlock/sherlock username`
**Output:** Links to profiles on social platforms
**Value for sales:** Find prospects' social presence, interests, network

### 3. holehe
**Purpose:** Email verification across 100+ services
**Usage:** `python tools/osint/holehe/holehe.py email@company.com`
**Output:** Which services the email is registered on
**Value for sales:** Verify email format, find what platforms prospect uses

### 4. maigret
**Purpose:** Advanced username search (stronger than sherlock)
**Usage:** `python tools/osint/maigret/maigret username`
**Output:** Extensive profile links with screenshots
**Value for sales:** Deep prospect research

### 5. Account Intelligence Engine (Built-in)
**Purpose:** Multi-source company research
**Usage:** `python -m agents.account_intel.engine "Company Name"`
**Output:** 20-section strategic account intelligence report
**Value for sales:** Complete company analysis for deal preparation

## Unified Research Command
```bash
python research.py "Company Name"
```
