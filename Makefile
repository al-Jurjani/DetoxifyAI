.PHONY: help rag rag-setup rag-test rag-clean

# Default target
help:
	@echo "DetoxifyAI - RAG Pipeline Makefile"
	@echo "=================================="
	@echo ""
	@echo "Available targets:"
	@echo "  make rag          - Run end-to-end RAG pipeline demo"
	@echo "  make rag-setup    - Install dependencies and verify environment"
	@echo "  make rag-test     - Run comprehensive RAG tests"
	@echo "  make rag-clean    - Clean temporary files and caches"
	@echo ""

# Main RAG demo target - runs end-to-end pipeline
rag: rag-setup
	@echo "=========================================="
	@echo "Running DetoxifyAI RAG Pipeline Demo"
	@echo "=========================================="
	@echo ""
	@python3 scripts/test_rag.py --demo
	@echo ""
	@echo "✅ RAG pipeline demo completed successfully!"

# Setup dependencies
rag-setup:
	@echo "Checking dependencies..."
	@pip list | grep -q "modal" || (echo "Installing modal..." && pip install modal)
	@pip list | grep -q "langchain" || (echo "Installing langchain..." && pip install langchain langchain-community langchain-huggingface langchain-core)
	@pip list | grep -q "faiss" || (echo "Installing faiss..." && pip install faiss-cpu)
	@pip list | grep -q "sentence-transformers" || (echo "Installing sentence-transformers..." && pip install sentence-transformers)
	@pip list | grep -q "azure-storage-blob" || (echo "Installing azure-storage-blob..." && pip install azure-storage-blob)
	@echo "✅ All dependencies installed"
	@echo ""
	@echo "Verifying environment variables..."
	@test -f .env || (echo "❌ ERROR: .env file not found!" && exit 1)
	@grep -q "AZURE_STORAGE_CONNECTION_STRING" .env || (echo "❌ ERROR: AZURE_STORAGE_CONNECTION_STRING not set in .env!" && exit 1)
	@echo "✅ Environment verified"
	@echo ""

# Run comprehensive tests
rag-test: rag-setup
	@echo "=========================================="
	@echo "Running Comprehensive RAG Tests"
	@echo "=========================================="
	@echo ""
	@python3 scripts/test_rag.py --test-all
	@echo ""
	@echo "✅ All RAG tests completed!"

# Clean temporary files
rag-clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf /tmp/faiss_* 2>/dev/null || true
	@echo "✅ Cleanup complete"
