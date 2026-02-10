#!/bin/bash
# Setup script for LLM models with Ollama

set -e

echo "=============================================="
echo "MLIR to QIR Translator - LLM Setup"
echo "=============================================="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama is not installed!"
    echo ""
    echo "Please install Ollama first:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    exit 1
fi

echo "✓ Ollama is installed"
echo ""

# Check if Ollama service is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

echo "✓ Ollama service is running"
echo ""

# Function to pull model with progress
pull_model() {
    local model_name=$1
    local description=$2

    echo "----------------------------------------"
    echo "Pulling: $description"
    echo "Model: $model_name"
    echo "----------------------------------------"

    if ollama list | grep -q "$model_name"; then
        echo "✓ Model already exists: $model_name"
    else
        echo "Downloading model (this may take a while)..."
        ollama pull "$model_name"
        echo "✓ Successfully pulled: $model_name"
    fi

    echo ""
}

# Pull models
echo "[1/3] Pulling Development Model (Fast, 8GB VRAM)..."
pull_model "llama3.1:8b-instruct" "Llama 3.1 8B - Development & Testing"

echo "[2/3] Pulling Production Model (High Quality, 40GB VRAM)..."
pull_model "llama3.1:70b-instruct-q4_K_M" "Llama 3.1 70B 4-bit - Production Quality"

echo "[3/3] Pulling Code-Specialized Model (Optional, 13GB VRAM)..."
pull_model "codellama:13b" "CodeLlama 13B - Code Translation"

echo "=============================================="
echo "Model Setup Complete!"
echo "=============================================="
echo ""

# List installed models
echo "Installed models:"
ollama list
echo ""

echo "=============================================="
echo "Next Steps:"
echo "=============================================="
echo "1. Configure model in .env file:"
echo "   LLM_MODEL=llama3.1:8b-instruct      # Fast"
echo "   LLM_MODEL=llama3.1:70b-instruct-q4_K_M  # Best quality"
echo "   LLM_MODEL=codellama:13b             # Code-focused"
echo ""
echo "2. Run knowledge base setup:"
echo "   python scripts/fetch_knowledge.py"
echo "   python scripts/initialize_db.py"
echo ""
echo "3. Launch the application:"
echo "   streamlit run src/ui/app.py"
echo ""
