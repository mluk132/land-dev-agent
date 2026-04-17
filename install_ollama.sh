#!/bin/bash
# Install Ollama and download models - ONE TIME SETUP

echo "🚀 Installing Ollama (Zero-Cost AI)"
echo "===================================="
echo ""

# Install Ollama
echo "📥 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo ""
echo "✅ Ollama installed!"
echo ""

# Download models
echo "📥 Downloading AI models (one-time, ~2GB each)..."
echo ""

echo "1/3 Downloading llama3.2:3b (fast, recommended)..."
ollama pull llama3.2:3b

echo ""
echo "2/3 Downloading mistral:7b (better quality)..."
ollama pull mistral:7b

echo ""
echo "3/3 Downloading deepseek-r1:7b (best reasoning)..."
ollama pull deepseek-r1:7b

echo ""
echo "✅ All models downloaded!"
echo ""
echo "💰 Total Cost: $0"
echo "📊 Models ready for unlimited use"
echo ""
echo "Test it:"
echo "  ollama run llama3.2:3b 'Analyze R-1 zoning'"
echo ""
echo "🎉 Setup complete! Run: python orchestrator_free.py"
