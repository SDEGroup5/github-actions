#!/bin/bash

set -euo pipefail

DEBUG=1

# Linux or macOS
_KERNEL=$(uname -s)
_ARCH=$(uname -m)

WORKFLOW_DIR=".github/workflows"

if [[ "$_KERNEL" == "Linux" ]]; then
    KERNEL="linux"
elif [[ "$_KERNEL" == "Darwin" ]]; then
    KERNEL="macos"
else
    echo "Unsupported OS: $_KERNEL"
    exit 1
fi

if [[ "$_ARCH" == "x86_64" ]]; then
    ARCH="amd64"
elif [[ "$_ARCH" == "arm64" ]]; then
    ARCH="arm64"
else
    echo "Unsupported architecture: $_ARCH"
    exit 1
fi

CONTAINER_ARCH="${KERNEL}/${ARCH}"

WORKFLOW_FILES=$(find "$WORKFLOW_DIR" -name "*.yml" -o -name "*.yaml")

for workflow_file in $WORKFLOW_FILES; do
    act --container-architecture ${CONTAINER_ARCH} \
        -P self-hosted=catthehacker/ubuntu:act-24.04 \
        --actor nektos/act \
        --env ACT=true \
        --workflows "$workflow_file"
done
