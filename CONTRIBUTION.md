# Contribution Guidelines

## Team Members

| Name | Student ERP ID |
|------|----------------|
| Talha Shahid | 26948 |
| Zuhair Farhan | 27100 |
| Ahsanuddin | 27134 |

## Task Distribution

| Member | Primary Responsibilities | Detailed Contributions |
|--------|-------------------------|------------------------|
| **Talha Shahid** | Cloud Infrastructure, API Development, Testing & CI/CD | • Created Azure VMs to host MLflow experiments with Azure Blob Storage for artifact storage<br>• Launched AWS EC2 instances for MLflow deployment<br>• Built FastAPI application with live model integration from Azure Blob Storage<br>• Hosted FastAPI on live VM with frontend integration<br>• Improved test coverage from ~60% to >80% using pytest and mock testing<br>• Fixed linting issues and CI/CD pipeline<br>• API documentation (FastAPI /docs) |
| **Zuhair Farhan** | MLOps Setup, Monitoring, Infrastructure | • Repository initialization and project structure<br>• Dataset preparation and initial model training (Logistic Regression, XGBoost)<br>• MLflow setup with Azure Blob Storage integration for model artifacts and metrics<br>• Prometheus + Grafana monitoring stack setup and configuration<br>• CI/CD pipeline implementation (`.github/workflows/ci.yml`) - 4/5 tests passing<br>• Pre-commit hooks setup and configuration<br>• Initial documentation (README, CONTRIBUTION, CODE_OF_CONDUCT, LICENSE) |
| **Ahsanuddin** | ML Experimentation, Data Drift Monitoring | • MLflow experiment execution and tracking<br>• Evidently AI setup for data drift detection<br>• Model development and hyperparameter tuning<br>• [Additional contributions to be added] |

## Contributions by Deliverable

### D1 - README.md
- **Ahsanuddin**: Elevator pitch, project logo, architecture diagram
- **Talha**: Quick-start guide, Make targets, FAQ section, cloud deployment documentation
- **Zuhair**: Overall project flow explanation, MLflow documentation, monitoring stack setup

### D2 - CONTRIBUTION.md
- **All members**: Individual contribution documentation

### D3 - Dockerfile
- **Talha**: Multi-stage production Dockerfile with health checks
- **Zuhair**: Docker Compose setup for Prometheus and Grafana

### D4 - .github/workflows/ci.yml
- **Zuhair**: CI/CD pipeline implementation (branch: `infra/ci-d4`) - linting, testing, build, canary deploy
- **Talha**: CI/CD fixes and test coverage improvements

### D5 - ML Workflow Monitoring
- **Ahsanuddin**: MLflow experiments, Evidently AI data drift monitoring
- **Talha**: MLflow deployment on AWS EC2
- **Zuhair**: MLflow initialization, Azure Blob Storage backend, Prometheus + Grafana stack

### D6 - Pre-commit Hooks
- **Zuhair**: Pre-commit hook setup (branch: `infra/pre-commit`) - trailing-whitespace, end-of-file-fixer, detect-secrets

### D7 - API Documentation
- **Talha**: FastAPI interactive docs (/docs, /redoc), cURL examples, JSON schemas

### D8 - Security & Compliance
- **Zuhair**: LICENSE, CODE_OF_CONDUCT.md
- **Talha**: Dependency vulnerability scanning setup

### D9 - Cloud Integration
- **Talha**: AWS EC2 (inference API hosting), AWS VM setup for MLflow
- **Zuhair**: Azure Blob Storage (model artifacts, MLflow backend)

## Branch Naming Convention

We follow a structured branch naming convention:

- `feat/` - New features (e.g., `feat/prediction-api`)
- `fix/` - Bug fixes (e.g., `fix/model-loading-error`)
- `infra/` - Infrastructure and DevOps (e.g., `infra/ci-cd-pipeline`, `infra/pre-commit`)
- `docs/` - Documentation updates (e.g., `docs/api-examples`)
- `test/` - Testing improvements (e.g., `test/coverage-improvement`)

**Rules**: lowercase, hyphen-separated, descriptive names

## Development Workflow

1. Create feature branch: `git checkout -b feat/feature-name`
2. Make changes and test locally
3. Run pre-commit hooks: `pre-commit run --all-files`
4. Run tests: `pytest --cov=app --cov-fail-under=80`
5. Commit with descriptive message
6. Create PR and request review
7. Merge after CI passes and approval

## Pre-commit Hooks

```bash
# Install and setup
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

**Enabled hooks**: trailing-whitespace, end-of-file-fixer, detect-secrets, black, ruff
