#!/bin/bash
set -x

# source venv
# source ../.venv/bin/activate
# source .venv/bin/activate
source .env

# build
uv build

exit

# Test upload to TestPyPI with uv
# uv run twine upload --repository testpypi dist/*

uv run twine upload --repository testpypi dist/* --username __token__ --password $TESTPYPI_TOKEN

exit

# Optional: Test on TestPyPI first
twine upload --repository testpypi dist/*
