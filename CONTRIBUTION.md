# Contribution Guidelines

## Team Members

| Name | Student ERP ID |
|------|----------------|
| Talha Shahid | 26948 |
| Zuhair Farhan | 27100 |
| Muhammad Ahsan | 27134 |

## Task Distribution - Milestone 1

| Member | Primary Responsibilities | Detailed Contributions |
|--------|-------------------------|------------------------|
| **Talha Shahid** | Cloud Infrastructure, API Development, Testing & CI/CD | • Created Azure VMs to host MLflow experiments with Azure Blob Storage for artifact storage<br>• Launched AWS EC2 instances for MLflow deployment<br>• Built FastAPI application with live model integration from Azure Blob Storage<br>• Hosted FastAPI on live VM with frontend integration<br>• Improved test coverage from ~60% to >80% using pytest and mock testing<br>• Fixed linting issues and CI/CD pipeline<br>• API documentation (FastAPI /docs) |
| **Zuhair Farhan** | MLOps Setup, Monitoring, Infrastructure | • Repository initialization and project structure<br>• Dataset preparation and initial model training (Logistic Regression, XGBoost)<br>• MLflow setup with Azure Blob Storage integration for model artifacts and metrics<br>• Prometheus + Grafana monitoring stack setup and configuration<br>• CI/CD pipeline implementation (`.github/workflows/ci.yml`) - 4/5 tests passing<br>• Pre-commit hooks setup and configuration<br>• Initial documentation (README, CONTRIBUTION, CODE_OF_CONDUCT, LICENSE) |
| **Muhammad Ahsan** | ML Experimentation, Data Drift Monitoring, Bonuses | • MLflow experiment execution for XGBoost and Logistic Regression with hyperparameter tuning (eta, n_estimators, max_depth, solver, penalty, C)<br>• Evidently AI setup for label drift detection with HTML report generation and local serving<br>• Grafana k6 load testing implementation with latency SLO assertions (p95 < 500ms, failure rate < 5%)<br>• pip-audit integration in CI/CD for dependency vulnerability scanning<br>• Docker Compose configuration with separate dev, test, and prod profiles, including isolated setups for each service (app, db, and Prometheus) |

## Contributions by Deliverables - Milestone 1

### D1 - README.md
- **Muhammad Ahsan**: Elevator pitch, project logo, architecture diagram
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
- **Muhammad Ahsan**: MLflow experiments with XGBoost and Logistic Regression hyperparameter tuning, Evidently AI data drift detection (`generate_evidently_drift.py`, served on localhost:7000)
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

## Evidently Dashboard
<img width="1280" height="606" alt="image" src="https://github.com/user-attachments/assets/ab6b483f-7d31-48ce-b29c-9756e8906b35" />
<img width="1280" height="465" alt="image" src="https://github.com/user-attachments/assets/2d0e1a4c-7425-4000-9bb8-aaa8b104ca4b" />

### D6 - Pre-commit Hooks
- **Zuhair**: Pre-commit hook setup (branch: `infra/pre-commit`) - trailing-whitespace, end-of-file-fixer, detect-secrets
## Sample Git Commit After Successful Implementation of Pre-Commit Hooks
![WhatsApp Image 2025-10-30 at 19 08 52_03370a0c](https://github.com/user-attachments/assets/a2ee8fe9-393a-45d4-a030-432eb36725a1)

### D7 - API Documentation
- **Talha**: FastAPI interactive docs (/docs, /redoc), cURL examples, JSON schemas

### D8 - Security & Compliance
- **Muhammad Ahsan**: pip-audit integration in CI/CD for dependency vulnerability scanning
- **Zuhair**: LICENSE, CODE_OF_CONDUCT.md

### D9 - Cloud Integration
- **Talha**: AWS EC2 (inference API hosting), AWS VM setup for MLflow
- **Zuhair**: Azure Blob Storage (model artifacts, MLflow backend)
## Azure Blob storing Model and Vectorizer Pickle Files, and a Metrics CSV File
<img width="1281" height="507" alt="image" src="https://github.com/user-attachments/assets/b8bb6b5c-dca7-42e0-b1b3-5dcf9ba2b5d9" />

# Bonus - Milestone 1
- **Muhammad Ahsan**:
  - **End-to-end load testing with Grafana k6** (`tests/load_test.js`) with latency SLO assertions (p95 < 500ms, failure rate < 5%), achieved 0% failures and ~22ms p95 latency
    ![WhatsApp Image 2025-10-31 at 12 19 12_eda16046](https://github.com/user-attachments/assets/83e93e01-30c4-4761-b578-d1bda70f8352)

  - **pip-audit integration** in CI/CD for dependency vulnerability scanning
    ![WhatsApp Image 2025-10-31 at 16 28 18_c6e3d339](https://github.com/user-attachments/assets/0ae42bc2-b87a-4e09-9c71-af289c05ef50)
    ![WhatsApp Image 2025-10-31 at 16 31 53_c2126511](https://github.com/user-attachments/assets/59728e7a-c979-4598-9f17-ed9bc30942c4)
    ![WhatsApp Image 2025-10-31 at 12 59 45_3957017a](https://github.com/user-attachments/assets/b29f07d7-2fe6-475f-83ff-901304d40351)

  - **Docker Compose configuration with separate dev, test, and prod profiles**, including isolated setups for each service (app, db, and Prometheus)

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


## Branch Naming Convention - Milestone 1

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

---

# Milestone 2 Contributions (LLMOps)

## Task Distribution - Milestone 2

| Member | Primary Responsibilities | Detailed Contributions |
|--------|-------------------------|------------------------|
| **Zuhair Farhan** | LLMOps Pipeline, RAG Implementation, Prompt Engineering, Evaluation | • Complete RAG pipeline implementation with FAISS vector store and LangChain integration<br>• Knowledge base creation (200+ toxic-to-professional examples across multiple categories)<br>• Document ingestion pipeline with Azure Blob Storage integration<br>• Mistral-7B LLM deployment on Modal serverless GPU platform<br>• Prompt engineering: Zero-Shot, Few-Shot (k=3, k=5), Chain-of-Thought, Meta-Prompting strategies<br>• Comprehensive evaluation methodology using ParaDetox dataset (20 samples)<br>• Manual evaluation of 80 outputs (20 per strategy) across 3 dimensions: Tone, Intent, Length<br>• Weights & Biases integration for experiment tracking and comparison<br>• Guardrails implementation: PII detection (Presidio), prompt injection filtering, toxicity thresholds<br>• LLM monitoring metrics: token usage, latency, cost tracking, guardrail violations<br>• CI/CD pipeline updates for M2: prompt evaluation tests, 80% coverage requirement, security scanning<br>• Complete documentation: EVALUATION.md, prompt_report.md, SECURITY.md updates<br>• Multi-cloud architecture coordination: AWS EC2 + Azure Blob + Modal serverless |

## Contributions by Deliverable - Milestone 2

### D1 - Prompt Engineering Workflow
- **Zuhair Farhan**:
  - Implementation of 4 prompt strategies in `src/prompts/`: zero_shot.py, few_shot.py, chain_of_thought.py, meta_prompting.py
  - Few-Shot k=3 vs k=5 comparative analysis
  - Evaluation dataset preparation (ParaDetox English, 20 samples)
  - Quantitative metrics: Cosine similarity calculation using sentence-transformers
  - Qualitative evaluation: Manual scoring across Tone (1-5), Intent (1-5), Length (1-5)
  - Weights & Biases experiment tracking and visualization
  - Results analysis: Few-Shot k=5 (241/300) and Chain-of-Thought (244/300) tied for best performance
  - Comprehensive prompt_report.md documenting methodology, results, and insights

**📸 Weights & Biases Experiment Tracking:**
<img width="1013" height="712" alt="image" src="https://github.com/user-attachments/assets/3a29366c-4ead-463b-933d-11b5afbb9674" />


### D2 - RAG Pipeline
- **Zuhair Farhan**:
  - Knowledge base creation: 200+ toxic-to-professional rephrasing examples, style guides, conflict resolution templates
  - Document ingestion pipeline (`src/ingest.py`): chunking, metadata tagging, embedding generation (all-MiniLM-L6-v2)
  - FAISS vector store implementation with 203 documents indexed
  - LangChain integration: VectorStoreRetriever, PromptTemplate, custom ModalMistralLLM wrapper
  - Azure Blob Storage integration for RAG artifacts (faiss_index.zip, knowledge_base.pkl)
  - Retrieval pipeline: Top-5 semantic search for context injection
  - FastAPI `/rephrase` endpoint with RAG workflow
  - System architecture and data flow diagrams (Mermaid)
  - End-to-end reproducibility via Makefile target: `make rag`

**📸 RAG Pipeline Architecture:**
*(Diagrams included in README.md - System Architecture and Data Flow sections)*

### D3 - Guardrails & Safety Mechanisms
- **Zuhair Farhan**:
  - PII detection using Microsoft Presidio: SSN, email, phone, credit cards
  - Prompt injection filtering: regex patterns, NeMo Guardrails integration
  - Input validation: length checks (5-500 chars), toxicity pre-screening
  - Output moderation: toxicity threshold (toxic-bert score < 0.3), hallucination detection
  - Guardrail event logging to `guardrail_events.json`
  - Comprehensive test coverage in `tests/test_guardrails.py`
  - Integration within RAG pipeline: pre-LLM and post-LLM validation gates
  - Documentation in SECURITY.md: threat model, defense mechanisms, responsible AI guidelines

### D4 - LLM Evaluation & Monitoring
- **Zuhair Farhan**:
  - Prometheus metrics instrumentation for LLM operations:
    - `llm_request_count` by prompt strategy
    - `llm_token_usage_total` (input + output tokens)
    - `llm_request_duration_seconds` histogram
    - `llm_cost_usd` estimated per request
    - `guardrail_violations_total` by type (PII, injection, toxicity)
    - `rag_retrieval_duration_seconds` for vector search latency
    - `rag_documents_retrieved` count per query
  - Grafana dashboard configuration for LLM metrics visualization
  - Evidently integration extended for LLM output drift monitoring
  - Real-time monitoring of Modal serverless GPU usage and cold-start latency
  - Dashboard screenshots and links documented in README.md

<img width="1197" height="504" alt="image" src="https://github.com/user-attachments/assets/2594ee57-e868-435c-9682-667ef466835f" />
<img width="1184" height="325" alt="image" src="https://github.com/user-attachments/assets/97634146-b169-43bc-8695-6ad5e48dac16" />


### D5 - CI/CD for LLMOps
- **Zuhair Farhan**:
  - Extended `.github/workflows/ci.yml` with M2 jobs:
    - Linting for prompt scripts and RAG pipeline code
    - Prompt evaluation tests on sample dataset
    - Unit tests for guardrails, RAG components (80% coverage achieved)
    - Docker build for RAG-enabled API
    - Security scanning: pip-audit for critical CVEs
  - Automated prompt evaluation job: runs all 4 strategies on test data, logs results
  - Integration tests for `/rephrase` endpoint with RAG and guardrails
  - Canary deployment extended to test LLM rephrasing functionality
  - CI coverage increased from 65% (M1) to 82% (M2)

### D6 - Documentation & Reports
- **Zuhair Farhan**:
  - **README.md updates**:
    - LLMOps objectives and project overview
    - Updated architecture diagram with RAG, LLM, guardrails, prompt strategies
    - RAG pipeline deployment guide (step-by-step)
    - `/rephrase` API endpoint documentation with examples
    - Multi-cloud architecture section (AWS + Azure + Modal)
    - LLM monitoring metrics section
    - Updated project structure with M2 additions
  - **EVALUATION.md**:
    - Comprehensive evaluation methodology (dataset, metrics, experimental setup)
    - Quantitative results: cosine similarity analysis, latency breakdown
    - Qualitative analysis: Tone, Intent, Length scores across 80 samples
    - Failure case analysis with concrete examples and mitigations
    - Key insights: Few-Shot k=5 and CoT recommended, cosine similarity is weak predictor
    - Detailed appendices with score breakdowns and sample outputs
  - **prompt_report.md**: Detailed technical report on prompt engineering experiments
  - **SECURITY.md updates**: Prompt injection defenses, PII handling, responsible AI guidelines

### D7 - Cloud Integration (Multi-Cloud)
- **Zuhair Farhan**:
  - **AWS EC2**: FastAPI backend hosting (continued from M1, extended with `/rephrase` endpoint)
  - **Azure Blob Storage**: Extended with new container `detoxifyai-rag-artifacts` for FAISS index, knowledge base, embeddings
  - **Modal Serverless**: Mistral-7B-Instruct-v0.2 deployment with auto-scaling GPU (A10G), 4-bit quantization
  - Multi-cloud coordination: data flow from Azure → EC2 → Modal → EC2 → User
  - Deployment scripts for Modal LLM service
  - Cloud configuration documentation with setup instructions
  - Screenshots and architecture diagrams showing service interaction


### D8 - Security & Compliance
- **Zuhair Farhan**:
  - **SECURITY.md**: Comprehensive security documentation including:
    - Prompt injection defense mechanisms (input sanitization, allowlist patterns)
    - Data privacy: PII detection and redaction (Presidio integration)
    - Responsible AI guidelines: output toxicity filtering, hallucination detection, bias monitoring
    - Dependency scanning: pip-audit in CI pipeline
    - Encryption: Azure Blob Storage at rest, HTTPS for all API communication
  - Guardrails documentation: threat model, defense-in-depth approach
  - Security testing: adversarial prompt tests, PII detection validation
  - Compliance documentation: data handling, user privacy, no storage of toxic inputs

## Evaluation Results Summary - Milestone 2

| Prompt Strategy | Avg Similarity | Avg Latency | Tone | Intent | Length | Total Score | Rank |
|----------------|---------------|-------------|------|--------|--------|-------------|------|
| Zero-Shot | 0.553 | 3.38s | 3.6 | 3.1 | 3.0 | 193/300 | 4th |
| Few-Shot (k=3) | 0.532 | 2.66s | 3.9 | 4.0 | 3.9 | 237/300 | 3rd |
| **Few-Shot (k=5)** ⭐ | 0.539 | 4.17s | 4.2 | 4.0 | 4.0 | **241/300** | **1st (tied)** |
| **Chain-of-Thought** ⭐ | 0.523 | 3.52s | 4.4 | 3.9 | 3.9 | **244/300** | **1st (tied)** |

**Key Findings**:
- Few-Shot (k=5) and Chain-of-Thought achieved best overall performance (~80% quality score)
- Few-Shot (k=5) recommended for production: best balance across tone, intent, and length
- Chain-of-Thought excelled in tone (4.4) but occasionally over-explained
- Cosine similarity proved to be weak predictor of human-perceived quality (r = -0.38)

**Recommendation**: **Few-Shot (k=5)** for production deployment due to consistent, balanced performance

## Bonus Features - Milestone 2
- **Zuhair Farhan**:
  - **LangChain Integration**: Complete RAG toolchain with custom retrievers, document loaders, and LLM wrapper
  - **Multi-Cloud Architecture**: Seamless integration of AWS EC2 + Azure Blob + Modal serverless GPU
  - **Comprehensive Guardrails**: PII detection, prompt injection filtering, toxicity thresholds, hallucination detection
  - **Systematic Evaluation**: 80 manual evaluations across 4 strategies with structured rubric
  - **Weights & Biases**: Experiment tracking and comparison dashboard
