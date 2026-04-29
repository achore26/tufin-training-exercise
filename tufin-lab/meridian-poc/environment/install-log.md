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
