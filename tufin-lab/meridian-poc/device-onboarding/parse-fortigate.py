#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────
# Meridian Financial Group — FortiGate Config Parser
# Simulates how TOS Discovery onboards a Fortinet device
# ─────────────────────────────────────────────────────────

import re

CONFIG_FILE = "fortigate-config.txt"

def load_config(filepath):
    with open(filepath, "r") as f:
        return f.read()

# ─────────────────────────────────────────────────────────
# SECTION 1: Extract Hostname
# ─────────────────────────────────────────────────────────

def get_hostname(config):
    match = re.search(r'set hostname (.+)', config)
    if match:
        return match.group(1).strip()
    return "Unknown"

# ─────────────────────────────────────────────────────────
# SECTION 2: Extract Interfaces
# ─────────────────────────────────────────────────────────

def get_interfaces(config):
    interfaces = []

    # Find the interfaces block
    interface_block = re.search(
        r'config system interface(.*?)^end',
        config,
        re.DOTALL | re.MULTILINE
    )

    if not interface_block:
        return interfaces

    # Split into individual interface entries
    entries = re.split(r'\n\s*edit ', interface_block.group(1))

    for entry in entries:
        if not entry.strip():
            continue

        interface = {}

        # Get interface name
        name_match = re.match(r'"?([^"\n]+)"?', entry.strip())
        if name_match:
            interface["name"] = name_match.group(1).strip('"')

        # Get IP and subnet
        ip_match = re.search(r'set ip (\S+)\s+(\S+)', entry)
        if ip_match:
            interface["ip"] = ip_match.group(1)
            interface["subnet"] = ip_match.group(2)
        else:
            interface["ip"] = "N/A"
            interface["subnet"] = "N/A"

        # Get role
        role_match = re.search(r'set role (\S+)', entry)
        interface["role"] = role_match.group(1) if role_match else "unknown"

        # Get type
        type_match = re.search(r'set type (\S+)', entry)
        interface["type"] = type_match.group(1) if type_match else "physical"

        # If VLAN get VLAN ID and parent interface
        if interface["type"] == "vlan":
            vlanid_match = re.search(r'set vlanid (\S+)', entry)
            parent_match = re.search(r'set interface "?(\S+?)"?\s*\n', entry)
            interface["vlan_id"] = vlanid_match.group(1) if vlanid_match else "N/A"
            interface["parent"] = parent_match.group(1).strip('"') if parent_match else "N/A"

        interfaces.append(interface)

    return interfaces

# ─────────────────────────────────────────────────────────
# SECTION 3: Extract Firewall Rules
# ─────────────────────────────────────────────────────────

def get_firewall_rules(config):
    rules = []

    # Find the firewall policy block
    policy_block = re.search(
        r'config firewall policy(.*?)^end',
        config,
        re.DOTALL | re.MULTILINE
    )

    if not policy_block:
        return rules

    # Split into individual rule entries
    entries = re.split(r'\n\s*edit ', policy_block.group(1))

    for entry in entries:
        if not entry.strip():
            continue

        rule = {}

        # Rule ID
        id_match = re.match(r'(\d+)', entry.strip())
        rule["id"] = id_match.group(1) if id_match else "N/A"

        # Rule name
        name_match = re.search(r'set name "?([^"\n]+)"?', entry)
        rule["name"] = name_match.group(1).strip('"') if name_match else "Unnamed"

        # Source interface
        srcintf_match = re.search(r'set srcintf "?([^"\n]+)"?', entry)
        rule["srcintf"] = srcintf_match.group(1).strip('"') if srcintf_match else "N/A"

        # Destination interface
        dstintf_match = re.search(r'set dstintf "?([^"\n]+)"?', entry)
        rule["dstintf"] = dstintf_match.group(1).strip('"') if dstintf_match else "N/A"

        # Source address
        srcaddr_match = re.search(r'set srcaddr "?([^"\n]+)"?', entry)
        rule["srcaddr"] = srcaddr_match.group(1).strip('"') if srcaddr_match else "N/A"

        # Destination address
        dstaddr_match = re.search(r'set dstaddr "?([^"\n]+)"?', entry)
        rule["dstaddr"] = dstaddr_match.group(1).strip('"') if dstaddr_match else "N/A"

        # Action
        action_match = re.search(r'set action (\S+)', entry)
        rule["action"] = action_match.group(1) if action_match else "N/A"

        # Services
        service_match = re.search(r'set service (.+)', entry)
        rule["services"] = service_match.group(1).strip() if service_match else "N/A"

        # Log traffic
        log_match = re.search(r'set logtraffic (\S+)', entry)
        rule["logtraffic"] = log_match.group(1) if log_match else "N/A"

        rules.append(rule)

    return rules

# ─────────────────────────────────────────────────────────
# SECTION 4: Print Report
# ─────────────────────────────────────────────────────────

def print_report(hostname, interfaces, rules):

    print("=" * 60)
    print("  MERIDIAN FINANCIAL GROUP — FORTIGATE ONBOARDING REPORT")
    print("  Simulated TOS Discovery Output")
    print("=" * 60)

    # Device Info
    print(f"\nDevice Hostname   : {hostname}")
    print(f"Interfaces Found  : {len(interfaces)}")
    print(f"Firewall Rules    : {len(rules)}")

    # Interfaces
    print("\n" + "-" * 60)
    print("INTERFACES")
    print("-" * 60)

    for intf in interfaces:
        print(f"\n  Name      : {intf.get('name')}")
        print(f"  IP        : {intf.get('ip')}")
        print(f"  Subnet    : {intf.get('subnet')}")
        print(f"  Role      : {intf.get('role')}")
        print(f"  Type      : {intf.get('type')}")
        if intf.get("type") == "vlan":
            print(f"  VLAN ID   : {intf.get('vlan_id')}")
            print(f"  Parent    : {intf.get('parent')}")

    # Firewall Rules
    print("\n" + "-" * 60)
    print("FIREWALL RULES")
    print("-" * 60)

    for rule in rules:
        print(f"\n  Rule ID   : {rule.get('id')}")
        print(f"  Name      : {rule.get('name')}")
        print(f"  Src Intf  : {rule.get('srcintf')}")
        print(f"  Dst Intf  : {rule.get('dstintf')}")
        print(f"  Action    : {rule.get('action').upper()}")
        print(f"  Services  : {rule.get('services')}")

    # Deny Rules
    deny_rules = [r for r in rules if r.get("action") == "deny"]
    print("\n" + "-" * 60)
    print("DENY RULES")
    print("-" * 60)
    if deny_rules:
        for rule in deny_rules:
            print(f"\n  [DENY] Rule {rule['id']} — {rule['name']}")
            print(f"         {rule['srcintf']} -> {rule['dstintf']}")
    else:
        print("  None found.")

    # Logging Disabled
    log_disabled = [r for r in rules if r.get("logtraffic") == "disable"]
    print("\n" + "-" * 60)
    print("LOGGING DISABLED — REVIEW REQUIRED")
    print("-" * 60)
    if log_disabled:
        for rule in log_disabled:
            print(f"\n  [WARNING] Rule {rule['id']} — {rule['name']}")
            print(f"            Logging is disabled on this rule")
    else:
        print("  None found.")

    # Broad Accept Rules
    broad_rules = [
        r for r in rules
        if r.get("srcaddr", "").strip('"') == "all"
        and r.get("dstaddr", "").strip('"') == "all"
        and r.get("action") == "accept"
    ]
    print("\n" + "-" * 60)
    print("BROAD ACCEPT RULES — REVIEW REQUIRED")
    print("-" * 60)
    if broad_rules:
        for rule in broad_rules:
            print(f"\n  [WARNING] Rule {rule['id']} — {rule['name']}")
            print(f"            Accepts ALL src and ALL dst — review immediately")
    else:
        print("  None found.")

    print("\n" + "=" * 60)
    print("  END OF REPORT")
    print("=" * 60)

# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    config = load_config(CONFIG_FILE)
    hostname = get_hostname(config)
    interfaces = get_interfaces(config)
    rules = get_firewall_rules(config)
    
    # Write output to both terminal and onboarding-report.txt
    import sys
    
    # Save original stdout
    original_stdout = sys.stdout
    
    # Write to file
    with open("onboarding-report.txt", "w") as f:
        sys.stdout = f
        print_report(hostname, interfaces, rules)
    
    # Restore stdout and print to terminal
    sys.stdout = original_stdout
    print_report(hostname, interfaces, rules)
    print("\nReport saved to onboarding-report.txt")
