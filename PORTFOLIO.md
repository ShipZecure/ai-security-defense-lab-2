# AI Defense Lab — Portfolio

**Student:** Cyber Ayoni

**GitHub:** https://github.com/AibinuolaDamilola/ai-security-defense-lab/compare/main...ShipZecure:ai-security-defense-lab-2:main

**Streamlit App:** https://ai-security-defenselab.streamlit.app/

**Completed:** 7/7/2026

---

Fill in each section as you complete a level. Link directly to your commit diff so a recruiter can see exactly what you changed.

---

## Level 1 — MedVitals AI · Cloud Infrastructure Security

**Problem:** The MedVitals AI production deployment wrapper hardcoded live AWS credentials and a database password directly inside the source code which was pushed to a public GitHub repository. 

The IAM service account running the application was configured with a wildcard policy granting full administrative access to the entire AWS account. An attacker who obtained these credentials could assume the AdminFullAccess role, enumerate all cloud resources, read and write to any S3 bucket, and exfiltrate sensitive patient records with no restrictions.

**Method:** Parsed 17 AWS CloudTrail events covering a 6-hour window. 
Identified a source IP change from the internal address 10.0.4.22 to an external address 198.51.100.45 at event 13. Confirmed the breach via the AssumeRole event targeting AdminFullAccess, followed by ListBuckets, PutObject to a path named __exfil__/bulk-export-20260630.tar.gz, and GetObject — all within 130 seconds.

Verified successful exfiltration through the ETag value returned in the PutObject responseElements, which AWS only returns on a successful write. 

Fixed the credential exposure by replacing all hardcoded secrets with os.environ.get() calls, created a .env file for local development, and added .gitignore to prevent secrets from ever being committed. Rewrote the IAM policy from a wildcard to specific permitted actions scoped to two named S3 bucket ARNs.

**Evidence:** https://github.com/ShipZecure/ai-security-defense-lab-2/commit/15b14a6

**Outcome:** Credentials no longer appear anywhere in source code. 
If the repository is public, no secret is exposed. 
The IAM blast radius is reduced from full account administrative access to eight specific actions across two named S3buckets. A compromised credential can no longer be used to access  model weights, access logs, or any other bucket outside the defined scope. 

For a HealthTech company handling patient data, this directly reduces HIPAA breach liability and protects investor confidence ahead of a funding round.

**Skills:** CloudTrail log forensics · IAM least privilege · Secrets management
· Environment variable security · Incident Timeline documentation


**Others:**
- Technical write-up: [Medium blog post](https://medium.com/@CyberDammy/ai-security-defense-lab-part-1-bca2fc4ba074?postPublishedType=repub) 


---

## Level 2 — DataForge ML · AI Model Security

Problem: DataForge ML's model loader downloaded AI model weights from an unverified Hugging Face account (logix-community) in legacy pickle format without running any integrity verification before loading into the production genomics inference pipeline. The downloaded model contained a malicious subprocess.check_output payload embedded in the serialised weight file — a MITRE ATLAS AML.T0010 supply chain compromise. Loading the model would have given an attacker shell execution access to the inference server and all connected research data.

Method: Audited model_loader.py and identified pickle.load() with no pre-scan verification. Audited the source Hugging Face repository and identified four supply chain risk factors: unverified publisher account, no model card, no checksum, legacy .pkl format. Ran Picklescan against the model fixture file — scan returned dangerous import 'subprocess check_output' FOUND. Replaced pickle.load() with safe_open() from the safetensors library. Added scan_model_before_loading() as a mandatory security gate that must pass before the load function executes. Changed source repository reference to a verified account.

Evidence: (https://github.com/AibinuolaDamilola/ai-security-defense-lab/commit/4f8a10ed4ec7877f1b9f2442a11b228ba7ece2eb)

Outcome: The inference pipeline can no longer load a pickle-format model file. Even if a future malicious model reaches the download step, the Picklescan gate catches it and aborts before execution. The supply chain attack vector that enabled this breach no longer exists in the pipeline.

Skills: AI model supply chain security · Picklescan · safetensors · MITRE ATLAS AML.T0010 · Static malware analysis · CI/CD security gates

**Others:**
- [Technical write-up link]
- [LinkedIn post link]

---

## Level 3 — CartBot AI · Application & API Security

**Problem:**

**Method:**

**Evidence:** [Link to commit]

**Outcome:**

**Skills:** AI API Hardening · Rate Limiting · Output Filtering · OWASP LLM Top 10 · Direct Prompt Injection Defence

**Others:**
- [Technical write-up link]
- [LinkedIn post link]

---

## Level 4 — PayGuard · Data Security in AI

**Problem:**

**Method:**

**Evidence:** [Link to commit]

**Outcome:**

**Skills:** STRIDE Threat Modeling · RAG Pipeline Security · Multi-Tenant Data Isolation · Indirect Prompt Injection Defence

**Others:**
- [Technical write-up link]
- [LinkedIn post link]

---

## Level 5 — LegalBot Municipal · Agentic AI Security

**Problem:**

**Method:**

**Evidence:** [Link to commit]

**Outcome:**

**Skills:** Excessive Agency Mitigation · Llama Guard Integration · Pydantic Schema Enforcement · Autonomous Agent Containment

**Others:**
- [Technical write-up link]
- [LinkedIn post link]
