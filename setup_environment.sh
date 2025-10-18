#!/bin/bash
# ARXML Editor Environment Setup Script

set -e  # Exit on any error

echo "🚀 Setting up ARXML Editor Environment"
echo "======================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📋 Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.9" | bc -l) -eq 1 ]]; then
    echo "❌ Python 3.9 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv arxml-editor-env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source arxml-editor-env/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo "📦 Installing ARXML Editor..."
pip install -e .

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use ARXML Editor:"
echo "1. Activate the virtual environment: source arxml-editor-env/bin/activate"
echo "2. Run the application: python run_editor.py"
echo "3. Or run tests: python test_complete_application.py"
echo ""
echo "To deactivate the virtual environment later: deactivate"