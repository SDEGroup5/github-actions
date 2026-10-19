#!/bin/sh
yapf --in-place --parallel --recursive $(find . -type f -name "*.py" ! -path "./.venv/*")
