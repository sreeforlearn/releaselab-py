# ReleaseLab 🧪
visit&feedback  - [sreeharinath](https://sreeharinath.com)

### Configurable Flask Application for DevSecOps & Release Validation

ReleaseLab is a Python Flask application designed to demonstrate configuration-driven application behavior, automated testing, CI/CD pipelines, security scanning, containerization, and safe release validation.

The same application code can simulate different release scenarios by changing environment variables, allowing developers and DevOps engineers to test application health, readiness, startup delays, and failed-release behavior without maintaining separate codebases.

# 👨‍💻 About Me
Hi, I'm Sreeharinath Peetla, a DevOps Engineer passionate about automation, cloud-native technologies, reliable deployments, and continuous improvement.
I enjoy learning by building practical projects that connect development, testing, security, and operations. My areas of interest include CI/CD automation, containers, Kubernetes, cloud platforms, Infrastructure as Code, observability, and DevSecOps practices.
# ❤️ My Passion
My passion is to make software delivery more automated, secure, reliable, and repeatable.
I like exploring how a small code change moves through a real-world delivery pipeline—from automated tests and code-quality checks to container image scanning, deployment validation, and recovery from a failed release. ReleaseLab is a practical learning project where I can experiment with these workflows, understand failures safely, and continuously improve my DevOps skills.
## 🎯 Project Objectives

- Demonstrate V1, V2, and V3 release scenarios using configurable behavior.
- Implement unit and endpoint integration tests using Pytest.
- Automate testing through GitHub Actions.
- Build and run the application using Docker.
- Integrate DevSecOps tools into CI/CD pipelines.
- Demonstrate Kubernetes rollout validation and rollback.

## 🏗️ Architecture

```text
Developer Push
      |
      v
GitHub Repository
      |
      v
GitHub Actions / Jenkins
      |
      v
Automated Tests (Pytest)
      |
      v
Code Quality & Security Checks
      |
      v
Docker Build & Image Scan
      |
      v
Container Registry
      |
      v
Kubernetes / OpenShift
      |
      v
Release Validation & Rollback
```

*The architecture represents the planned end-to-end workflow. Security integrations and deployment stages are added progressively.*

## ✨ Features

- **Configuration-driven behavior:** Change application version and readiness behavior through environment variables.
- **Health endpoint:** Check whether the application process is responding.
- **Readiness endpoint:** Verify whether the application is ready to receive traffic.
- **Version endpoint:** Identify the running application version.
- **Automated tests:** Validate normal, delayed-readiness, and failed-readiness scenarios.
- **Docker support:** Build and run the application in a container.
- **CI automation:** Execute tests automatically on GitHub pushes and pull requests.
- **Release engineering practice:** Extend the application to test deployment failures and recovery.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Application | Python, Flask |
| Testing | Pytest |
| CI/CD | GitHub Actions, Jenkins |
| Containerization | Docker, Docker Compose |
| Code quality | SonarQube |
| Security scanning | Gitleaks, Snyk, Trivy |
| Deployment | Kubernetes, Helm, OpenShift / EKS |

*Tools listed in the roadmap are not necessarily configured yet.*

## 📁 Project Structure

```text
releaselab/
├── app.py
├── tests/
│   └── test_app.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or compatible version
- pip
- Git
- Docker (optional, for container execution)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/releaselab.git
cd releaselab
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The application runs at:

`http://localhost:5000`

## 🔌 API Endpoints

| Endpoint | Purpose | Expected response |
|---|---|---|
| `/` | Application information | HTTP 200 |
| `/health` | Liveness check | HTTP 200 |
| `/ready` | Readiness check | HTTP 200 or 503 |
| `/version` | Application version | HTTP 200 |

### Example responses

**Health check**

```json
{
  "status": "UP",
  "version": "v1"
}
```

**Version check**

```json
{
  "application": "ReleaseLab",
  "version": "v1"
}
```

## ⚙️ Configuration-Based Testing

ReleaseLab uses environment variables to simulate different application states.

| Variable | Description | Default |
|---|---|---|
| `APP_VERSION` | Identifies the release version | `v1` |
| `READY_DELAY_SECONDS` | Delays readiness after startup | `0` |
| `NEVER_READY` | Keeps readiness checks failing when enabled | `false` |
| `PORT` | Application listening port | `5000` |

### Scenario 1: Stable release (V1)

```powershell
$env:APP_VERSION="v1"
$env:READY_DELAY_SECONDS="0"
$env:NEVER_READY="false"
python app.py
```

Expected result: `/health` and `/ready` return HTTP 200.

### Scenario 2: Delayed readiness (V2)

Stop the previous application process, then run:

```powershell
$env:APP_VERSION="v2"
$env:READY_DELAY_SECONDS="10"
$env:NEVER_READY="false"
python app.py
```

Expected result: `/ready` initially returns HTTP 503 and returns HTTP 200 after the configured delay.

### Scenario 3: Failed readiness (V3)

Stop the previous process, then run:

```powershell
$env:APP_VERSION="v3"
$env:READY_DELAY_SECONDS="0"
$env:NEVER_READY="true"
python app.py
```

Expected result: `/ready` returns HTTP 503 continuously, while `/health` continues returning HTTP 200 as long as the process responds.

**Important:** These scenarios simulate different release behaviors through configuration. They do not represent three separate application implementations.

## 🧪 Run Automated Tests

Execute the test suite:

```bash
pytest -v
```

The tests validate:

- Application health.
- Version configuration.
- Successful readiness.
- Delayed readiness.
- Failed readiness.

## 🐳 Run with Docker

Build the image:

```bash
docker build -t releaselab:local .
```

Run the container:

```bash
docker run --rm -p 5000:5000 releaselab:local
```

Check the application:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/ready
curl http://localhost:5000/version
```

Alternatively, run with Docker Compose:

```bash
docker compose up --build
```

## 🔄 CI/CD and DevSecOps Roadmap

The project can be extended in the following stages:

1. **Automated testing:** Run Pytest on every push and pull request.
2. **Code quality:** Integrate SonarQube and configure quality gates.
3. **Secret detection:** Scan commits using Gitleaks.
4. **Dependency security:** Scan Python dependencies using Snyk.
5. **Container security:** Scan Docker images using Trivy.
6. **Image publishing:** Tag and publish approved images to a container registry.
7. **Deployment:** Deploy using Helm to Kubernetes, EKS, or OpenShift.
8. **Release validation:** Verify readiness and rollout status.
9. **Recovery:** Demonstrate safe rollback after a failed deployment.
10. **Pipeline comparison:** Implement equivalent CI/CD workflows using GitHub Actions and Jenkins.

Security tools, registry publishing, and Kubernetes deployment require additional configuration before they become executable pipeline stages.

## 🔐 Security Considerations

- Never commit passwords, access tokens, API keys, or cloud credentials.
- Store CI/CD secrets in the appropriate secrets manager.
- Keep failure-simulation settings restricted to development and test environments.
- Pin and review third-party GitHub Actions before using them in production.
- Enforce security and quality gates before publishing or deploying release images.

## 📌 Project Status

**Current scope:** Flask application, configurable health/readiness/version endpoints, Pytest tests, Docker support, and a basic GitHub Actions testing workflow.

**Planned enhancements:** SonarQube, Snyk, Gitleaks, Trivy, Jenkins pipelines, image publishing, Kubernetes deployment, and automated rollback validation.

## 👨‍💻 Purpose

ReleaseLab is a hands-on DevOps learning project for understanding how application configuration, automated testing, CI/CD, security controls, containerization, and deployment validation work together.

---

**ReleaseLab — Build. Test. Secure. Release.**

---

### 🙏 Thank You
Made with ❤️ by **SREE**  
📍 NYC — End of README
