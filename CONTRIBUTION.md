# Contribution Guidelines

## Team Members

| Name | Student ERP ID | GitHub Username | Email |
|------|----------------|-----------------|-------|
| Muhammad Ahsanuddin | ERP-XXXXX | @username1 | email1@example.com |
| Talha Saleem Shahid | 26948 | @TalhaShahid004 | talhashahid363@gmail.com |
| Zuhair Farhan | 27100 | @Al-Jurjani | zuhairfarhan@gmail.com |

## Task Distribution

| Member | Tasks | Specific Contributions |
|--------|-------|------------------------|
| Ahsanuddin | - | - |
| Talha | - | - |
| Zuhair | MLFlow Workflow Monitoring, Cloud Setup | - Setup MLFlow experimentations<br>- Setup Azure blob storage to store run artificats and metrics<br>- -<br>- - |

## Detailed Contributions by Phase

### Phase 1: Project Setup
- **Ahsanuddin**: Environment setup
- **Talha**: Branches management, docker configuration, Makefile creation, AWS VM hosting
- **Zuhair**: Repository initialization, project structure design

### Phase 2: Development
- **Ahsanuddin**: Model development, hyperparameter tuning
- **Talha**: API endpoint development, request/response schemas
- **Zuhair**: Dataset preparation, model development, hyperparameter tuning

### Phase 3: Integration & Testing
- **Ahsanuddin**: Used Evidently to track data drift
- **Talha**: API testing, load testing with Prometheus and Grafana experiments, setup AWS VM to host API
- **Zuhair**: Model evaluation with MLflow, setup Azure Blob Storage for storage of artifacts and metrics

### Phase 4: Documentation & Deployment
- **Ahsanuddin**: README sections on overall project
- **Talha**: API documentation, usage examples, AWS VM setup instructions
- **Zuhair**: MLflow documentation, Azure Blob Storage setup instructions


## Detailed Contributions by Deliverable

### Deliverable 1 - README.md
- **Ahsanuddin**: Elevator Pitch, Project Logo, and Project Flow Diagram
- **Talha**: Quick Start, Make Targets
- **Zuhair**: Explanation of Overall Project Flow

### Deliverable 2 - CONTRIBUTION.md
- Each member mentions their contributions.

### Deliverable 3 - Dockerfile
- **Ahsanuddin**:
- **Talha**:
- **Zuhair**: Initial Dockerfile setup for Prometheus and Grafana

### Deliverable 4 - .github/workflows/ci.yml
- **Zuhair**: Setup the workflow on infra/ci-d4 branch - Linting test to be added.

### Deliverable 5 - ML Workflow Monitoring
- **Ahsanuddin**: Ran experiements on MLFlow, Set up Evidently
- **Talha**: Hosted MlFlow on an AWS VM
- **Zuhair**: MLflow Initialization, Prometheus and Grafana Set Up

### Deliverable 6 - Pre-commit Hooks
- **Zuhair**: Set up pre-commit hooks on infra/pre-commit branch

### Deliverable 7 - API Documentation
- **Talha**: what did you do fir this bro

### Deliverable 8 - Security & Compliance
- **Ahsanuddin**:
- **Talha**:
- **Zuhair**:

### Deliverable 9 - Cloud Integration
- **Talha**:
- **Zuhair**:

## Branch Naming Convention

We follow a structured branch naming convention to maintain clarity and organization:

### Branch Prefixes

- `feat/` - New features
  - Example: `feat/data-ingestion-pipeline`
  - Example: `feat/prediction-api`

- `fix/` - Bug fixes
  - Example: `fix/model-loading-error`
  - Example: `fix/api-timeout-issue`

- `infra/` - Infrastructure and DevOps changes
  - Example: `infra/docker-optimization`
  - Example: `infra/ci-cd-pipeline`

- `docs/` - Documentation updates
  - Example: `docs/api-examples`
  - Example: `docs/setup-guide`

- `test/` - Testing additions or modifications
  - Example: `test/integration-tests`
  - Example: `test/coverage-improvement`

- `refactor/` - Code refactoring
  - Example: `refactor/data-processing`
  - Example: `refactor/model-architecture`

- `chore/` - Maintenance tasks
  - Example: `chore/dependency-update`
  - Example: `chore/cleanup-old-code`

### Branch Naming Rules

1. Use lowercase letters
2. Separate words with hyphens
3. Keep names descriptive but concise
4. Include ticket/issue number when applicable: `feat/123-add-authentication`

## Development Workflow

### 1. Creating a New Feature

```bash
# Create and switch to feature branch
git checkout -b feat/your-feature-name

# Make your changes
# ...

# Run pre-commit hooks
pre-commit run --all-files

# Run tests
make test

# Commit with descriptive message
git commit -m "feat: add your feature description"

# Push to remote
git push origin feat/your-feature-name
```

### 2. Pull Request Process

1. Ensure all tests pass locally
2. Update documentation if needed
3. Create PR with descriptive title and description
4. Link related issues
5. Request review from at least one team member
6. Address review comments
7. Squash commits if necessary
8. Merge after approval

### 3. Code Review Guidelines

**For Reviewers:**
- Check code quality and adherence to standards
- Verify tests are comprehensive
- Ensure documentation is updated
- Test functionality locally if needed
- Provide constructive feedback

**For Authors:**
- Respond to all comments
- Make requested changes promptly
- Ask for clarification when needed
- Keep PRs focused and reasonably sized

## Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Maximum line length: 88 characters (Black default)
- Use descriptive variable and function names

### Testing Standards
- Minimum 80% code coverage required
- Write unit tests for all new functions
- Include integration tests for APIs
- Use pytest fixtures for test data

### Documentation Standards
- Docstrings for all public functions/classes (Google style)
- Inline comments for complex logic
- Update README for new features
- Maintain API documentation

## Commit Message Format

We follow conventional commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```
feat(api): add prediction endpoint with caching

Implemented /predict endpoint with Redis caching to improve
response times for repeated requests.

Closes #42
```

```
fix(data): resolve memory leak in data loader

Fixed memory leak caused by unclosed file handles in the
data loading pipeline.

Fixes #38
```

## Git Workflow

### Main Branches
- `main`: Production-ready code
- `develop`: Integration branch for features (if applicable)

### Merge Strategy
- Use pull requests for all changes
- Require passing CI checks before merge
- Squash commits for cleaner history (optional)
- Delete branch after merge

### Conflict Resolution
1. Pull latest changes from target branch
2. Resolve conflicts locally
3. Test thoroughly after resolution
4. Push resolved changes

## Pre-commit Hooks

All contributors must install pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Enabled Hooks
- `trailing-whitespace`: Remove trailing whitespace
- `end-of-file-fixer`: Ensure files end with newline
- `detect-secrets`: Prevent committing secrets
- `black`: Code formatting
- `ruff`: Linting

## Communication

### Regular Meetings
- Weekly sync: Every [Day] at [Time]
- Sprint planning: Bi-weekly
- Code reviews: Ongoing

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- Pull Requests: Code review discussions
- [Slack/Discord/Teams]: Daily communication
- [Email]: Formal communications

## Issue Tracking

### Issue Labels
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority-high`: High priority items

### Issue Template

When creating issues, include:
- Clear description of the problem/feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details
- Relevant logs or screenshots

## Resources for Contributors

- [Python Style Guide](https://pep8.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

## Questions or Problems?

If you have questions or encounter problems:
1. Check existing documentation
2. Search closed issues
3. Create a new issue with detailed description

## Acknowledgments

We appreciate all contributions to this project. Thank you for following these guidelines to maintain code quality and collaboration efficiency.
