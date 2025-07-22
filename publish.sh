#!/bin/bash
# Script to publish to PyPI using tokens from .env file

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Copy .env.example to .env and add your tokens"
    exit 1
fi

# Source the .env file
source .env
# source .venv/bin/activate
# uv pip install twine
# uv build

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "Error: dist/ directory not found!"
    echo "Run 'python -m build' first"
    exit 1
fi

# Function to upload to TestPyPI
upload_test() {
    echo "Uploading to TestPyPI..."
    if [ -z "$TESTPYPI_TOKEN" ]; then
        echo "Error: TESTPYPI_TOKEN not set in .env"
        exit 1
    fi
    
    uv run twine upload --repository testpypi dist/* \
        --username __token__ \
        --password "$TESTPYPI_TOKEN"
}

# Function to upload to PyPI
upload_prod() {
    echo "Uploading to PyPI..."
    if [ -z "$PYPI_TOKEN" ]; then
        echo "Error: PYPI_TOKEN not set in .env"
        exit 1
    fi
    
    uv run twine upload dist/* \
        --username __token__ \
        --password "$PYPI_TOKEN"
}

# Main script
case "${1}" in
    test)
        upload_test
        echo ""
        echo "Test with: pip install --index-url https://test.pypi.org/simple/ pydeptree"
        ;;
    prod)
        upload_prod
        echo ""
        echo "Install with: pip install pydeptree"
        ;;
    *)
        echo "Usage: ./publish.sh [test|prod]"
        echo "  test - Upload to TestPyPI"
        echo "  prod - Upload to PyPI"
        exit 1
        ;;
esac
