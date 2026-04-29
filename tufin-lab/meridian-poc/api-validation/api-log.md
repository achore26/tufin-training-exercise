# Tufin SecureTrack API Validation Log
# Meridian Financial Group — PoC
# Date: 29 April 2026

---

## Call 1: Retrieve All Managed Devices

**Full URL:**
https://192.168.1.1/securetrack/api/devices?start=1&count=10

**HTTP Method:** GET

**Expected Status Code:** 200 OK

**What the response would contain:**
A list of up to 10 managed devices including device ID, hostname,
IP address, vendor, model, and current monitoring status for each
device registered in TOS.

**What this tells us about Meridian:**
This call confirms which devices TOS is currently monitoring. For
Meridian, we would expect to see all 14 FortiGate devices listed
across the Nairobi, London, and Dubai sites. If any device is
missing from this list it means onboarding for that device was not
completed successfully and TOS has no visibility into its policies.

---

## Call 2: Retrieve Firewall Rules for Device ID 1 (Paginated)

**Full URL:**
https://192.168.1.1/securetrack/api/devices/1/rules?start=1&count=15

**HTTP Method:** GET

**Expected Status Code:** 200 OK

**What the response would contain:**
A list of the first 15 firewall rules on device ID 1, including
rule ID, rule name, source interface, destination interface,
source address, destination address, action (accept/deny),
services, and whether logging is enabled.

**What this tells us about Meridian:**
This call mirrors exactly what our Python parser extracted from
the FortiGate config file — the 15 rules on MFG-NAIROBI-FW01.
In a live TOS deployment this call would return real-time rule
data directly from the device, meaning any rule changes made
after onboarding would be reflected here immediately without
needing to re-run a parser script.

---

## Call 3: Search Network Objects Containing "finance"

**Full URL:**
https://192.168.1.1/securetrack/api/network_objects/search?name=finance

**HTTP Method:** GET

**Expected Status Code:** 200 OK

**What the response would contain:**
A list of all network objects whose name contains the word
"finance" — including object ID, name, type (host/network/group),
IP address or range, and which devices the object is used on.

**What this tells us about Meridian:**
This call would surface all policy objects related to Meridian's
finance segment — things like the vlan-finance interface address
object, any finance-specific address groups, and which firewall
rules reference them. This is particularly useful for Meridian
because the finance VLAN was flagged in our onboarding report as
having a broad accept rule allowing unrestricted internet access,
and this call helps identify everywhere that finance-related
objects appear across the policy estate.

---
