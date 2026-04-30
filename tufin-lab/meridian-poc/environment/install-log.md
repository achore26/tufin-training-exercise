# Meridian PoC Installation Log

## Today's Date — 28/04/2026

### What I am setting up
I am building the simulated PoC environment for Meridian Financial Group's 30-day SecureTrack+ evaluation to see if it fits them..

### Components and why each one is needed

1.Linux Server (local VM with Docker and Kubernetes installed): This is the application layer that TOS runs on.
 Docker provides the containerised environment and Kubernetes manages the orchestration of those containers.

2.Azure VM: Represents the cloud-side deployment for Meridian's 
Dubai site. This will simulate how TOS would monitor cloud infrastructure alongside on-premise FortiGate devices in a hybrid environment.

3.Simulated FortiGate configuration: Allows us to test device onboarding and rule parsing without needing access to Meridian's 
actual production firewalls during the PoC.

Tufin REST API: Used to validate that TOS can communicate correctly with managed devices and retrieve rule and policy data 
the way it would in a live deployment.

#Second ubernetes task log.
Component: Kubernetes Test Deployment

Status: Running

Confirmation: i conformed that the pods were running successfully and the nginx demo page is live. When killing one of the pods, the deployment
automatically starts a new one ensuring the environment is stable.


#third task working on kubernetes.

component: Azure VM
Public IP: 102.37.17.247
status: Running

This VM in the Meridian context represents the Dubai site.
----------------
## Entry 4 — 29/04/2026 — Environment Hardening Check

### Local Environment

**Kubernetes Pods**
Status: Running
Confirmed all poc-test pods are running successfully on the local 
Kubernetes cluster. No crashed pods found, no intervention required.

**Validation Script (validation-checks.sh)**
Status: 3/3 components ready
Docker: PASS — running locally
Kubernetes: PASS — cluster reachable
Azure VM: PASS — reachable at 102.37.17.247

**Directory Structure Check**
Status: Complete
All files confirmed in place across all four meridian-poc folders:
environment, device-onboarding, api-validation, and deliverables.

**Disk Space Check**
Status: Sufficient space available
No disk space concerns identified. Environment has enough capacity 
to continue the Meridian PoC without issue.

### Azure VM Hardening Check

**VM Status:** Running
**Public IP:** 102.37.17.247

**Docker Status:** Running — confirmed via sudo docker ps

**System Uptime and Memory:** Stable — confirmed via uptime and free -h

**NSG Rules:** Confirmed in place via Azure Portal
Port 22 SSH Allow Priority 100
Port 80 HTTP Allow Priority 110

**Public IP Curl Check:** 102.37.17.247 confirmed via curl -s https://api.ipify.org

**Overall Environment Status: Stable and ready for PoC demonstration**


------------------------
## Entry 5 — 30/04/2026 — Full Environment Validation (Pre-Demo Check)

### Local Environment

**[09:00] Validation Script — validation-checks.sh**
Status: PASS
Result: 3/3 components ready
- Docker: PASS — running locally
- Kubernetes: PASS — cluster reachable
- Azure VM: PASS — reachable at 102.37.17.247

**[09:05] Kubernetes Pods — kubectl get pods**
Status: PASS
Result: All 4 pods confirmed running
- hello-app-554fb57cc7-6rjn7 — Running — Age 6d16h
- hello-app-554fb57cc7-c6tjf — Running — Age 6d16h
- poc-test-5c8b97544f-qqbdm — Running — Age 43h
- poc-test-5c8b97544f-txgh6 — Running — Age 43h

**[09:07] poc-test Service Browser Access**
Status: PASS
Result: nginx demo page confirmed accessible via browser on port 80.
Note: NodePort 30090 does not resolve on Mac with Docker Desktop 
due to known local environment behaviour — service confirmed 
reachable via port 80 which is acceptable for demo purposes.

**[09:10] Directory Structure Check**
Status: PASS
Result: All files confirmed present across all four meridian-poc folders:
- environment/install-log.md
- environment/validation-checks.sh
- environment/poc-test-deployment.yaml
- device-onboarding/fortigate-config.txt
- device-onboarding/parse-fortigate.py
- device-onboarding/onboarding-report.txt
- api-validation/api-log.md
- deliverables/poc-summary.md
- deliverables/follow-up-email.md

**[09:12] GitHub Branch Check**
Status: PASS
Result: TF31-AlbertChore branch confirmed up to date with Day 8 commit
Latest commit: 028d34c — Day 8 device onboarding, API validation, 
environment hardening

---

### Azure VM

**[09:15] SSH Connectivity**
Status: PASS
Result: Successfully SSHed into Azure VM at 102.37.17.247 
as azureuser — VM is running and responsive.

**[09:17] Docker Status — sudo docker ps**
Status: PASS
Result: Docker daemon confirmed running on Azure VM — 
no errors returned.

**[09:19] Public IP Curl Check — curl -s https://api.ipify.org**
Status: PASS
Result: Returned 102.37.17.247 — confirms correct public IP 
and outbound internet connectivity working from inside the VM.

**[09:21] NSG Inbound Rules Check — Azure Portal**
Status: PASS
Result: All inbound rules confirmed in place:
- Port 22 SSH — Allow — Priority 100 — Source: my IP only
- Port 80 HTTP — Allow — Priority 110 — Source: any
- Port 80 open-port-80 — Allow — Priority 200 — Source: any

---

### Overall Environment Status: HEALTHY — Ready for demo
All checks passed. No issues found. Environment stable and 
confirmed ready for Meridian PoC demonstration.

##************Fault Testing **************
## Entry 6 — 30/04/2026 — Fault Testing

### Fault 1 — Kubernetes Pod Failure

**What I did:** Deliberately deleted pod poc-test-5c8b97544f-qqbdm 
using kubectl delete pod to simulate a pod crash.

**What happened:** Kubernetes detected the missing pod immediately 
and automatically spun up a replacement pod 
poc-test-5c8b97544f-bbcpj without any manual intervention.

**Time to recover:** 9 seconds from deletion to Running status.

**What this means for demo reliability:** Even if a pod crashes 
mid-demonstration, Kubernetes self-heals fast enough that the 
disruption would be minimal and largely invisible to the client. 
This gives confidence that the application layer of the PoC 
environment is resilient and does not require manual intervention 
to recover from a single pod failure.


### Fault 2 — NSG Rule Block

**What I did:** Installed nginx on the Azure VM to create a 
web server listening on port 80, confirmed the nginx welcome 
page was accessible at http://102.37.17.247, then deliberately 
removed the allow_http inbound rule from the tufin-poc-nsg 
Network Security Group in the Azure portal.

**What happened:** The moment the NSG rule was removed, the 
browser could no longer reach the nginx page at 
http://102.37.17.247 — the connection timed out completely, 
confirming that the NSG was actively blocking the traffic 
before it even reached the VM.

**How I diagnosed it:** The VM was still running and nginx 
was still active inside it — the block was happening at the 
NSG level, not inside the VM itself. This is the difference 
between a network-level block and an application-level failure.

**How I fixed it:** Restored the allow_http inbound rule on 
port 80 at priority 110 using the Azure Console. The nginx page 
became accessible again immediately after the rule was restored.

**What this tells me about NSG rule order:** NSG rules are 
evaluated in priority order — lower number means higher priority. 
If a deny rule with a lower priority number exists above an allow 
rule, the traffic will be blocked before the allow rule is ever 
reached. This is why rule priority matters and why removing or 
misconfiguring a single rule can silently block access to an 
entire service without touching the VM itself.

### Fault 3 — Script Failure Simulation

**What I did:** Deliberately introduced a syntax error in 
parse-fortigate.py by removing the colon at the end of the 
function definition on line 12, changing:
def load_config(filepath):
to:
def load_config(filepath)

**Error output:**
File "parse-fortigate.py", line 12
    def load_config(filepath)
                             ^
SyntaxError: expected ':'

**What caused it:** Python requires a colon at the end of every 
function definition, class definition, and control flow statement. 
Without it Python cannot understand where the function header ends 
and the function body begins, so it throws a SyntaxError and 
refuses to run the script at all.

**How I fixed it:** Added the colon back to the end of line 12 
restoring it to def load_config(filepath): and reran the script. 
The full onboarding report printed correctly with no errors.

**What this means for demo reliability:** A syntax error like 
this would cause the entire script to fail before it even starts 
running — no partial output, no report, nothing. This is why 
scripts need to be tested and confirmed working before a client 
session, not on the day of the demo. Having the onboarding-report.txt 
already generated and saved means even if the script fails during 
a live demo, the static report is available as a backup to walk 
the client through.
