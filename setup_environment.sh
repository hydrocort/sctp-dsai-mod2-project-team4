#!/bin/bash
# Setup script for Olist E-commerce Data Pipeline Project
# Usage: source setup_environment.sh

echo "🚀 Setting up Olist E-commerce Data Pipeline environment..."

# Activate conda environment
echo "📦 Activating mod2proj conda environment..."
conda activate mod2proj

# Set Google Cloud credentials
CREDENTIALS_PATH="$(pwd)/credentials/sctp-dsai-468313-f5bc3e6b4ebe-innergritx.json"

if [ -f "$CREDENTIALS_PATH" ]; then
    export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"
    echo "✅ Google Cloud credentials set: $GOOGLE_APPLICATION_CREDENTIALS"
else
    echo "❌ Warning: Credentials file not found at $CREDENTIALS_PATH"
    echo "   Please ensure your service account key is in the credentials/ directory"
fi

# Set other environment variables
export GCP_PROJECT_ID="sctp-dsai-468313"
export BQ_LOCATION="US"
export DATA_PATH="$(pwd)/data/brazilian-ecommerce/"

# Verify setup
echo "🔍 Verifying environment setup..."
echo "   📁 Working Directory: $(pwd)"
echo "   🐍 Python Environment: $(which python)"
echo "   ☁️  GCP Project: $GCP_PROJECT_ID"
echo "   📊 Data Path: $DATA_PATH"

# Check if data files exist
if [ -d "$DATA_PATH" ]; then
    CSV_COUNT=$(find "$DATA_PATH" -name "*.csv" | wc -l)
    echo "   📄 CSV Files Found: $CSV_COUNT"
else
    echo "   ⚠️  Warning: Data directory not found at $DATA_PATH"
fi

echo "✅ Environment setup complete!"
echo ""
echo "💡 Next steps:"
echo "   1. Verify prerequisites are complete"
echo "   2. Start with Stage 1: Loading into BigQuery (Meltano)"
echo "   3. Follow the implementation plan in plan.md"
echo ""
