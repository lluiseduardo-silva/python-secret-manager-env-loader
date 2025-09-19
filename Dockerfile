# syntax=docker/dockerfile:1.4
# Stage 1: base image com Python
FROM --platform=$BUILDPLATFORM python:3.9.13-slim AS base

WORKDIR /app

# Instala dependências básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl git unzip jq \
    && rm -rf /var/lib/apt/lists/*

# Só instala ferramentas genéricas de build
RUN pip install --upgrade pip setuptools wheel build

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY tests ./tests

# Stage 2: segurança (instala deps + roda análise)
FROM base AS security
RUN pip install -e .[dev]
RUN bandit -r src || true
RUN safety check || true

# Stage 3: testes
FROM base AS test
RUN pip install -e .[dev]
CMD ["pytest", "--cov=aws_secrets_env", "--cov-report=xml", "--cov-report=html"]

# Stage 4: análise SonarQube usando pysonar
FROM base AS sonar
RUN pip install -e .[dev]
RUN pip install pysonar

COPY sonar-project.properties .

# aqui usamos variáveis de ambiente para não hardcodar token
ENV SONAR_HOST_URL=http://sonarqube:9000
ENV SONAR_PROJECT_KEY=aws-secrets-env
ENV SONAR_TOKEN=""

CMD ["pysonar"]

# Stage 5: build do pacote
FROM base AS build
RUN pip install -e .[dev]
RUN python -m build
# artefatos vão para /app/dist
