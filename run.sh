#!/bin/sh
set -eu

# Use the directory containing this script.
cd "$(dirname "$0")"

echo "Open http://localhost:5000/json/getData"
echo "Press Ctrl+C to stop."

exec docker run --rm -it \
  --platform linux/amd64 \
  -p 5000:5000 \
  -v "$PWD:/work:ro,Z" \
  -w /work \
  alpine:3.24.2 \
  ./app