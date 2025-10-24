# File Organizer - Development Makefile

.PHONY: help install install-dev test test-cov lint format clean build publish docs

# Default target
help: ## Show this help message
	@echo "File Organizer - Development Commands"
	@echo "====================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

install-dev: ## Install with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	python -m pytest tests/ -v

test-cov: ## Run tests with coverage
	python -m pytest tests/ --cov=src/file_organizer --cov-report=term-missing --cov-report=html

test-fast: ## Run fast tests only
	python -m pytest tests/ -v -m "not slow"

lint: ## Run linting
	flake8 src/ tests/
	mypy src/

format: ## Format code
	black src/ tests/
	isort src/ tests/

format-check: ## Check code formatting
	black --check src/ tests/
	isort --check-only src/ tests/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build the package
	python -m build

publish: build ## Publish to PyPI
	twine upload dist/*

docs: ## Generate documentation
	@echo "Documentation is available in the docs/ directory"
	@echo "Open docs/README.md to get started"

# Development workflow
dev-setup: install-dev ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make test' to verify everything is working"

ci: lint test ## Run CI checks (lint + test)

# Quality checks
quality: format lint test ## Run all quality checks

# Release workflow
release-check: clean lint test build ## Check if ready for release
	@echo "✅ Ready for release!"

# Help for specific commands
test-help: ## Show test command options
	@echo "Test Commands:"
	@echo "  make test          - Run all tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make test-fast     - Run fast tests only"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"

# Test categories
test-unit: ## Run unit tests only
	python -m pytest tests/test_file_organizer_unit.py -v

test-integration: ## Run integration tests only
	python -m pytest tests/test_file_organizer_integration.py -v

# Development utilities
run-example: ## Run example script
	python scripts/run_tests.py all

check-deps: ## Check dependencies
	pip check

update-deps: ## Update dependencies
	pip install --upgrade -r requirements.txt
	pip install --upgrade -r requirements-test.txt
