#!/bin/bash

# Meridian PoC Environment Validation 

PASS=0

# Check 1:Check if  Docker is running
echo "Checking Docker..."

if docker info > /dev/null 2>&1; then
    echo "PASS - Docker is running"
    PASS=$((PASS + 1))
else
    echo "FAIL - Docker is not running"
fi

echo "finished first check"

# Check 2: Kubernetes cluster is reachable
echo "Checking Kubernetes cluster..."

if kubectl get nodes > /dev/null 2>&1; then
    echo "PASS - Kubernetes cluster is reachable"
    PASS=$((PASS + 1))
else
    echo "FAIL - Kubernetes cluster is not reachable"
fi

echo "finished second check"

# Check 3: Azure VM is reachable
echo "Checking Azure VM..."

AZURE_IP="102.37.17.247"

if ping -c 2 $AZURE_IP > /dev/null 2>&1; then
    echo "PASS - Azure VM is reachable at $AZURE_IP"
    PASS=$((PASS + 1))
else
    echo "FAIL - Azure VM is not reachable at $AZURE_IP"
fi

echo "finished testing.."

echo "-----------------------------------------"
echo "PoC Environment Status: $PASS/3 components ready"
echo "-----------------------------------------"
