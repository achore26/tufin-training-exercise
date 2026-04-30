Executive Summary
This document summarizes the 30-day Proof of Concept (PoC) for Tufin SecureTrack+. The goal was to determine if Tufin could resolve Meridian Financial Group's ongoing challenges with manual firewall management, painful audit cycles, and unexpected network outages across its Nairobi, London, and Dubai sites.

Outcome: The PoC successfully demonstrated that Tufin SecureTrack+ provides the visibility and automation necessary to transform Meridian’s security operations from a reactive, manual process into a proactive, compliant, and centralized system.

Current Challenges
Meridian currently manages 14 FortiGate devices manually. This has led to:
1. Audit Fatigue: PCI DSS compliance reporting currently takes three weeks of manual work per quarter.
2. Operational Risk: Conflicting and duplicate rules that have caused multi-hour outages, impacting business continuity.
3. Security Gaps: Without centralized visibility, inconsistencies in policy are common and difficult to detect.

PoC Objective Analysis
During the simulation and environment setup, we tested SecureTrack+ against Meridian’s four core objectives.

 1. Centralized Visibility
    Can Tufin provide a single view of all 14 FortiGate devices?
    Findings: Yes. In our simulation, we successfully onboarded the Nairobi firewall (MFG-NAIROBI-FW01). SecureTrack+ acts as a "single pane of glass," pulling data from all sites into one dashboard.
              This eliminates the need for team members to log into individual devices across different time zones to understand current access levels.

 2. Identifying Risky and Redundant Rules
    Can Tufin identify unused, shadowed, or duplicate rules automatically?
    Findings: Yes. Our analysis of the Nairobi configuration immediately flagged **11 rules** that were accepting traffic from 'Any device over the internet' to 'Any device in your network'.
              In a live environment, SecureTrack+ continuously scans for these efficiency killers, highlighting exactly which rules can be deleted or tightened without breaking applications.

 3. Automated Compliance (PCI DSS)
    Can Tufin automate compliance reporting, and how does it compare to the current process?
    Findings: What currently takes Meridian **three weeks** can be completed in **minutes**. Our simulation flagged **Rules 8 and 14** for having logging disabled—a direct violation of PCI DSS requirements.
              Tufin identifies these gaps instantly, allowing the team to fix them before an auditor ever sees them.

 4. Workflow Integration
    Can Tufin integrate with ServiceNow?
    Findings: Yes. Tufin is designed to "speak" to ServiceNow. This means when a change is requested in ServiceNow, Tufin can automatically check if that change is safe and compliant before it is even implemented,
              preventing the "conflicting rules" that caused Meridian's recent outages.
Evidence from Environment Analysis
Our onboarding report of the MFG-NAIROBI-FW01 device revealed critical vulnerabilities that are likely mirrored across other sites:
1. The "Blind Spot" Risk: Rules 8 (NTP) and 14 (Ping) had logging turned off. Without Tufin, these could remain hidden for years, failing audits and hiding attacker movement.
2. The "Wide Open" Risk: Multiple rules allowed broad access to the Internet and DMZ. SecureTrack+ surfaced these immediately, providing a clear roadmap for cleanup.

Conclusion and Recommended Next Steps
The PoC has proven that the primary hurdle to Meridian’s security is not the hardware, but the lack of centralized oversight. Tufin SecureTrack+ effectively bridges this gap.

Recommendation
We recommend moving forward with a full-scale production deployment across all three sites to ensure continuous compliance and prevent future outages caused by manual misconfigurations.

### Proposed Timeline
	Week 1-2: Full deployment of Tufin SecureTrack+ in the production environment.
	Week 3: Onboarding of all 14 FortiGate devices.
	Week 4: Generation of the first automated PCI DSS compliance "Ready-to-Audit" report.

Prepared by:
Albert Chore - Junior Pre-Sales Engineer, Tufin Solutions Engineering Team
