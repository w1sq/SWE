#!/bin/bash
set -e

total_percent=0
count=0

echo "Testing analysis"
cd analysis
percent=$(go test ./internal/server/... -cover | grep -o '[0-9.]\+% of statements' | grep -o '[0-9.]\+')
echo "Analysis: $percent%"
total_percent=$(awk "BEGIN {print $total_percent + $percent}")
count=$((count + 1))
cd ..

echo "Testing file-storage"
cd file-storage
percent=$(go test ./internal/server/... -cover | grep -o '[0-9.]\+% of statements' | grep -o '[0-9.]\+')
echo "File-storage: $percent%"
total_percent=$(awk "BEGIN {print $total_percent + $percent}")
count=$((count + 1))
cd ..

echo "Testing gateway"
cd gateway
percent=$(go test ./internal/handler/... -cover | grep -o '[0-9.]\+% of statements' | grep -o '[0-9.]\+')
echo "Gateway: $percent%"
total_percent=$(awk "BEGIN {print $total_percent + $percent}")
count=$((count + 1))
cd ..

total=$(awk "BEGIN {printf \"%.1f\", $total_percent/$count}")
echo "Total coverage: $total%"