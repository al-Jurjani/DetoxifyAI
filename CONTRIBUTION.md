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
| **Ahsanuddin** | ML Experimentation, Data Drift Monitoring, Load Testing | • MLflow experiment execution for XGBoost and Logistic Regression with hyperparameter tuning (eta, n_estimators, max_depth, solver, penalty, C)<br>• Evidently AI setup for label drift detection with HTML report generation and local serving<br>• Grafana k6 load testing implementation with latency SLO assertions (p95 < 500ms, failure rate < 5%)<br>• pip-audit integration in CI/CD for dependency vulnerability scanning<br>• Docker Compose configuration with separate dev, test, and prod profiles, including isolated setups for each service (app, db, and Prometheus) |

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
## Last Successful Pass:
<img width="1423" height="520" alt="image" src="https://github.com/user-attachments/assets/3c49e6fe-2e98-4b2c-8870-33b63f51edf0" />


### D5 - ML Workflow Monitoring
- **Ahsanuddin**: MLflow experiments with XGBoost and Logistic Regression hyperparameter tuning, Evidently AI data drift detection (`generate_evidently_drift.py`, served on localhost:7000)
- **Talha**: MLflow deployment on AWS EC2
- **Zuhair**: MLflow initialization, Azure Blob Storage backend, Prometheus + Grafana stack

## MLFlow XGBoost Runs:
<img width="1570" height="787" alt="image" src="https://github.com/user-attachments/assets/bff9b009-b308-433a-886f-367194c49077" />

## MLFlow XGBoost Runs:
<img width="1570" height="792" alt="image" src="https://github.com/user-attachments/assets/2b67c217-f7c9-4b30-a184-13ab7291c687" />

## Blob Storage
<img width="851" height="620" alt="image" src="https://github.com/user-attachments/assets/fc925055-df61-4f71-85f0-c7e67fab27dc" />

## Grafana with Metrics from Prometheus
![WhatsApp Image 2025-10-30 at 23 26 41_1f56e74b](https://github.com/user-attachments/assets/08832302-ac2f-4478-bfce-321896ba9698)



### D6 - Pre-commit Hooks
- **Zuhair**: Pre-commit hook setup (branch: `infra/pre-commit`) - trailing-whitespace, end-of-file-fixer, detect-secrets
## Sample Git Commit After Successful Implementation of Pre-Commit Hooks
![WhatsApp Image 2025-10-30 at 19 08 52_03370a0c](https://github.com/user-attachments/assets/a2ee8fe9-393a-45d4-a030-432eb36725a1)


### D7 - API Documentation
- **Talha**: FastAPI interactive docs (/docs, /redoc), cURL examples, JSON schemas

### D8 - Security & Compliance
- **Ahsanuddin**: pip-audit integration in CI/CD for dependency vulnerability scanning
- **Zuhair**: LICENSE, CODE_OF_CONDUCT.md

### D9 - Cloud Integration
- **Talha**: AWS EC2 (inference API hosting), AWS VM setup for MLflow
- **Zuhair**: Azure Blob Storage (model artifacts, MLflow backend)
## Azure Blob storing Model and Vectorizer Pickle Files, and a Metrics CSV File
<img width="1281" height="507" alt="image" src="https://github.com/user-attachments/assets/b8bb6b5c-dca7-42e0-b1b3-5dcf9ba2b5d9" />


### Bonus
- **Muhammad Ahsan**:  
  - End-to-end load testing with Grafana k6 (`tests/load_test.js`) with latency SLO assertions (p95 < 500ms, failure rate < 5%), achieved 0% failures and ~22ms p95 latency
    ![WhatsApp Image 2025-10-31 at 12 19 12_eda16046](https://github.com/user-attachments/assets/83e93e01-30c4-4761-b578-d1bda70f8352)

  - pip-audit integration in CI/CD for dependency vulnerability scanning
    ![WhatsApp Image 2025-10-31 at 16 28 18_c6e3d339](https://github.com/user-attachments/assets/0ae42bc2-b87a-4e09-9c71-af289c05ef50)
    ![WhatsApp Image 2025-10-31 at 16 31 53_c2126511](https://github.com/user-attachments/assets/59728e7a-c979-4598-9f17-ed9bc30942c4)
    ![WhatsApp Image 2025-10-31 at 12 59 45_3957017a](https://github.com/user-attachments/assets/b29f07d7-2fe6-475f-83ff-901304d40351)

  - Docker Compose configuration with separate dev, test, and prod profiles, including isolated setups for each service (app, db, and Prometheus)
  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/fb2a86d9-3043-45d3-bf21-83fb262bda62" alt="Dev Environment" width="1489" height="180">
    <p><em>Docker Compose dev environment up and running</em></p>
  </div>
  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/2f4e66b4-19cb-42db-bd61-9bc5830dc758" alt="Prod Environment" width="1490" height="179">
    <p><em>Docker Compose prod environment up and running</em></p>
  </div>
  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/31567f4b-f5b3-48d1-8d52-9332b10a9fc8" alt="Test Environment" width="1490" height="179">
    <p><em>Docker Compose test environment up and running</em></p>
  </div>
  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/65a908d4-ad1f-4ae8-8b71-78838b438818" alt="Docker Ps" width="1486" height="89">
    <p><em>Docker containers running (docker ps)</em></p>
  </div>


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
