
#!/bin/bash

echo demo environment check

PASSED=0

docker ps > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✔ Docker is running"
    PASSED=$((PASSED + 1))
else
    echo "✗ Docker is not running"
fi


kubectl version --client=false > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✔ Kubernetes cluster is reachabl"
    PASSED=$((PASSED + 1))
else
    echo "✗ Kubernetes cluster is unreachable"
fi

lsof -i :80 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✔ Port 80 is ope"n
    PASSED=$((PASSED + 1))
else
    echo "✗ Port 80 is not open"
fi

which curl > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✔ curl is available"
    PASSED=$((PASSED + 1))
else
    echo "✗ curl is not available"
fi

echo "environment check complete. $PASSED/4 checks passed."
