# Variável do token (recomendo usar variável de ambiente segura)
$env:SONAR_TOKEN = $env:SQTOKEN

# 1. Testes com cobertura
pytest --cov=aws_secrets_env --cov-report=xml

# 2. Segurança e linters
bandit -r src -f json -o bandit-report.json
flake8 src --format=json --output-file=flake8-report.json
mypy src --strict --ignore-missing-imports --junit-xml=mypy-report.xml
pylint src --output-format=json:pylint-report.json
ruff check src --output-format=json > ruff-report.json

# 3. Envio para o SonarQube
pysonar `
  --sonar-host-url=http://localhost:9000 `
  --sonar-token=$env:SONAR_TOKEN `
  --sonar-project-key=aws-secrets-env
